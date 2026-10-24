"""
Source arm (Table 4, rows 4-6): DenseNet121, two training sources
(source_A + source_C, the 2025 orange leaf HLB/healthy set), seeds 42/1/2.

Row 4: two sources, standard augmentation (config.yaml defaults)
Row 5: two sources, STRONG augmentation (rotation 30, jitter 0.4,
       vertical flip, random resized crop, random greyscale)
Row 6: two sources, trained on background-removed copies

Cross-source eval is always on the ORIGINAL source_B pool, except for
row 6 where it's also evaluated on the background-removed source_B pool
(data/nobg/source_B, generated earlier by run_1_prepare.py).
"""
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from torchvision import transforms

from src.core import (
    PROJECT_ROOT, build_model, compute_metrics, ensure_dir, get_device,
    load_checkpoint, load_config, make_loader, predict, print_metrics,
    save_json, scan_source, set_seed, stratified_split,
)
from src.explain import process_folder

MODEL = "densenet121"
SEEDS = [42, 1, 2]

STRONG_AUG = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomVerticalFlip(),
    transforms.RandomRotation(30),
    transforms.ColorJitter(brightness=0.4, contrast=0.4, saturation=0.4),
    transforms.RandomResizedCrop(224, scale=(0.8, 1.0)),
    transforms.RandomGrayscale(p=0.1),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])


def make_loader_custom(frame, cfg, transform, shuffle):
    from src.core import CitrusDataset
    from torch.utils.data import DataLoader
    dataset = CitrusDataset(frame, transform=transform)
    return DataLoader(dataset, batch_size=cfg["train"]["batch_size"], shuffle=shuffle,
                      num_workers=cfg["train"]["num_workers"], pin_memory=torch.cuda.is_available())


def combine_sources(cfg, classes, source_c_root):
    a_scan = scan_source(cfg["data"]["source_A"], classes, "source_A", cfg["data"]["min_images_per_class"])
    c_scan = scan_source(source_c_root, classes, "source_C", cfg["data"]["min_images_per_class"])
    combined = pd.concat([a_scan.frame, c_scan.frame], ignore_index=True)
    return combined


def train_one(cfg, train_frame, val_frame, classes, device, out_root, train_transform=None):
    ckpt_dir = ensure_dir(out_root / "checkpoints")
    if train_transform is None:
        train_loader = make_loader(train_frame, cfg, training=True)
    else:
        train_loader = make_loader_custom(train_frame, cfg, train_transform, shuffle=True)
    val_loader = make_loader(val_frame, cfg, training=False) if len(val_frame) else None

    model = build_model(cfg, len(classes)).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.AdamW(model.parameters(), lr=cfg["train"]["learning_rate"],
                                  weight_decay=cfg["train"]["weight_decay"])
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=cfg["train"]["epochs"])

    best_score, best_epoch, stale = -1.0, -1, 0
    patience = cfg["train"]["early_stop_patience"]
    history = []
    started = time.time()

    for epoch in range(1, cfg["train"]["epochs"] + 1):
        model.train()
        running_loss, seen, correct = 0.0, 0, 0
        for images, labels, _ in train_loader:
            images, labels = images.to(device), labels.to(device)
            optimizer.zero_grad(set_to_none=True)
            logits = model(images)
            loss = criterion(logits, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item() * labels.size(0)
            correct += (logits.argmax(1) == labels).sum().item()
            seen += labels.size(0)
        train_loss = running_loss / max(seen, 1)
        train_acc = correct / max(seen, 1)

        if val_loader is not None:
            y_true, y_pred, _, _ = predict(model, val_loader, device)
            val_metrics = compute_metrics(y_true, y_pred, classes)
            val_acc, val_f1, score = val_metrics["accuracy"], val_metrics["f1_macro"], val_metrics["f1_macro"]
        else:
            val_acc, val_f1, score = float("nan"), float("nan"), train_acc

        scheduler.step()
        history.append({"epoch": epoch, "train_loss": train_loss, "train_acc": train_acc,
                        "val_acc": val_acc, "val_f1": val_f1})

        marker = ""
        if score > best_score:
            best_score, best_epoch, stale = score, epoch, 0
            torch.save({"model_state": model.state_dict(), "epoch": epoch,
                       "classes": classes, "model_name": cfg["model"]["name"]},
                      ckpt_dir / "best.pt")
            marker = "  <- best"
        else:
            stale += 1

        print(f"  epoch {epoch:>3}/{cfg['train']['epochs']}  loss {train_loss:.4f}  "
              f"train_acc {train_acc*100:5.1f}%  val_acc {val_acc*100:5.1f}%  "
              f"val_f1 {val_f1:.3f}{marker}")

        if stale >= patience:
            print(f"  early stop (no improvement for {patience} epochs)")
            break

    elapsed = time.time() - started
    pd.DataFrame(history).to_csv(out_root / "train_history.csv", index=False)
    print(f"  training done in {elapsed/60:.1f} min, best epoch {best_epoch}, best val_f1 {best_score:.4f}")
    return ckpt_dir / "best.pt"


def evaluate(cfg, ckpt_path, frame, classes, device, title):
    model = load_checkpoint(ckpt_path, cfg, len(classes), device)
    loader = make_loader(frame, cfg, training=False, shuffle=False)
    y_true, y_pred, _, _ = predict(model, loader, device)
    metrics = compute_metrics(y_true, y_pred, classes)
    print_metrics(title, metrics)
    return metrics


def main():
    cfg = load_config()
    cfg["model"]["name"] = MODEL
    classes = cfg["classes"]
    device = get_device()

    source_c_root = str(PROJECT_ROOT / "data" / "raw" / "source_C")
    b_scan = scan_source(cfg["data"]["source_B"], classes, "source_B", cfg["data"]["min_images_per_class"])

    # background-removed source_C (for row 6), reusing the nobg machinery
    nobg_c_root = PROJECT_ROOT / "data" / "nobg" / "source_C"
    nobg_b_root = PROJECT_ROOT / "data" / "nobg" / "source_B"
    if not nobg_c_root.exists():
        print("Generating background-removed copies of source_C ...")
        n = process_folder(source_c_root, nobg_c_root)
        print(f"  source_C: {n} processed -> {nobg_c_root}")

    all_results = {}
    for condition in ["two_source", "strong_aug", "bg_removed"]:
        for seed in SEEDS:
            tag = f"{condition}_seed{seed}"
            print("\n" + "#" * 70)
            print(f"  SOURCE ARM: {tag}  [{time.strftime('%Y-%m-%d %H:%M:%S')}]")
            print("#" * 70)

            set_seed(seed)
            if condition == "bg_removed":
                combined = combine_sources(cfg, classes, str(nobg_c_root))
                # also swap in nobg source_A rows (already generated by run_1_prepare.py)
                nobg_a_root = PROJECT_ROOT / "data" / "nobg" / "source_A"
                a_nobg_scan = scan_source(str(nobg_a_root), classes, "source_A_nobg", cfg["data"]["min_images_per_class"])
                c_nobg_scan = scan_source(str(nobg_c_root), classes, "source_C_nobg", cfg["data"]["min_images_per_class"])
                combined = pd.concat([a_nobg_scan.frame, c_nobg_scan.frame], ignore_index=True)
            else:
                combined = combine_sources(cfg, classes, source_c_root)

            split_frame = stratified_split(combined, cfg["data"]["split"], seed)
            train_frame = split_frame[split_frame["split"] == "train"]
            val_frame = split_frame[split_frame["split"] == "val"]
            test_frame = split_frame[split_frame["split"] == "test"]
            print(f"  train={len(train_frame)}  val={len(val_frame)}  test={len(test_frame)}")

            out_root = ensure_dir(Path(cfg["output"]["root"]) / "source_arm" / tag)
            train_transform = STRONG_AUG if condition == "strong_aug" else None
            ckpt_path = train_one(cfg, train_frame, val_frame, classes, device, out_root, train_transform)

            m_same = evaluate(cfg, ckpt_path, test_frame, classes, device, f"({tag}) same-source test")

            if condition == "bg_removed":
                nobg_b_scan = scan_source(str(nobg_b_root), classes, "source_B_nobg", cfg["data"]["min_images_per_class"])
                m_cross = evaluate(cfg, ckpt_path, nobg_b_scan.frame, classes, device, f"({tag}) cross-source (nobg source_B)")
            else:
                m_cross = evaluate(cfg, ckpt_path, b_scan.frame, classes, device, f"({tag}) cross-source (source_B)")

            run_result = {"condition": condition, "seed": seed, "n_train": len(train_frame),
                         "same_source": m_same, "cross_source": m_cross}
            all_results[tag] = run_result
            save_json(run_result, out_root / "result.json")

    save_json(all_results, Path(cfg["output"]["root"]) / "source_arm" / "all_results.json")
    print("\nSOURCE ARM COMPLETE  [{}]".format(time.strftime('%Y-%m-%d %H:%M:%S')))


if __name__ == "__main__":
    main()
