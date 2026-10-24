"""
Quantity arm + single-source 3-seed baseline (Table 4, rows 2 and 3).

Row 2: DenseNet121 on stratified 25/50/75% subsets of source_A's training
       split, seed 42 only (single-seed exploratory, per the table caption).
Row 3: DenseNet121 on the full source_A training split (100%), seeds 42, 1, 2
       (mean +/- SD baseline for comparison against the two-source arm).

Each run trains fresh (new stratified split + subsample, new init) for its
own seed, evaluates on the source_A test split (same-source) and the full
source_B pool (cross-source), and writes metrics to
results/quantity_arm/seed<S>_pct<P>/.
"""
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np
import pandas as pd
import torch
import torch.nn as nn

from src.core import (
    build_model, build_transforms, compute_metrics, ensure_dir, get_device,
    load_config, make_loader, predict, print_metrics, save_json, scan_source,
    set_seed, stratified_split,
)

MODEL = "densenet121"
RUNS = [
    (42, 0.25), (42, 0.50), (42, 0.75),
    (42, 1.00), (1, 1.00), (2, 1.00),
]


def subsample_train(frame: pd.DataFrame, pct: float, seed: int) -> pd.DataFrame:
    if pct >= 1.0:
        return frame
    rng = np.random.default_rng(seed)
    out = []
    for label, group in frame.groupby("label", sort=True):
        train_rows = group[group["split"] == "train"]
        keep_n = max(1, int(round(len(train_rows) * pct)))
        keep_idx = rng.choice(train_rows.index, size=keep_n, replace=False)
        kept_train = train_rows.loc[keep_idx]
        rest = group[group["split"] != "train"]
        out.append(pd.concat([kept_train, rest], ignore_index=True))
    return pd.concat(out, ignore_index=True)


def train_one(cfg, train_frame, val_frame, classes, device, out_root):
    ckpt_dir = ensure_dir(out_root / "checkpoints")
    train_loader = make_loader(train_frame, cfg, training=True)
    val_loader = make_loader(val_frame, cfg, training=False) if len(val_frame) else None

    model = build_model(cfg, len(classes)).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.AdamW(
        model.parameters(), lr=cfg["train"]["learning_rate"],
        weight_decay=cfg["train"]["weight_decay"],
    )
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
        optimizer, T_max=cfg["train"]["epochs"]
    )

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
    from src.core import load_checkpoint
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

    a_scan = scan_source(cfg["data"]["source_A"], classes, "source_A", cfg["data"]["min_images_per_class"])
    b_scan = scan_source(cfg["data"]["source_B"], classes, "source_B", cfg["data"]["min_images_per_class"])

    all_results = {}
    for seed, pct in RUNS:
        tag = f"seed{seed}_pct{int(pct*100)}"
        print("\n" + "#" * 70)
        print(f"  QUANTITY ARM: {tag}  [{time.strftime('%Y-%m-%d %H:%M:%S')}]")
        print("#" * 70)

        set_seed(seed)
        split_frame = stratified_split(a_scan.frame, cfg["data"]["split"], seed)
        sub_frame = subsample_train(split_frame, pct, seed)
        train_frame = sub_frame[sub_frame["split"] == "train"]
        val_frame = sub_frame[sub_frame["split"] == "val"]
        test_frame = sub_frame[sub_frame["split"] == "test"]
        print(f"  train={len(train_frame)}  val={len(val_frame)}  test={len(test_frame)}")

        out_root = ensure_dir(Path(cfg["output"]["root"]) / "quantity_arm" / tag)
        ckpt_path = train_one(cfg, train_frame, val_frame, classes, device, out_root)

        m_same = evaluate(cfg, ckpt_path, test_frame, classes, device,
                          f"({tag}) same-source test")
        m_cross = evaluate(cfg, ckpt_path, b_scan.frame, classes, device,
                           f"({tag}) cross-source (source_B)")

        run_result = {
            "seed": seed, "pct": pct, "n_train": len(train_frame),
            "same_source": m_same, "cross_source": m_cross,
        }
        all_results[tag] = run_result
        save_json(run_result, out_root / "result.json")

    save_json(all_results, Path(cfg["output"]["root"]) / "quantity_arm" / "all_results.json")
    print("\nQUANTITY ARM COMPLETE  [{}]".format(time.strftime('%Y-%m-%d %H:%M:%S')))


if __name__ == "__main__":
    main()
