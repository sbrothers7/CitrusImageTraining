r"""
Step 17 - CNN trained on Jeju data (AI Hub 635 Training leaves) vs. the VLM debate.

  py tools\jeju_cnn.py                (17_jeju_cnn.bat runs this)
  python3 tools/jeju_cnn.py --seeds 42 1 2 --epochs 10

1) environment : a separate venv with PyTorch (CUDA when an NVIDIA GPU is present)
                 Windows: C:\citrus-git\jeju_cnn_venv   macOS/Linux: ~/citrus-git/jeju_cnn_venv
2) data        : AI Hub Training leaves (정상/궤양병/귤응애/진딧물, 12,593) -> 256px copies in
                 <data_root>/aihub_256/  ;  test = Validation leaves (1,573, never used in training)
3) model       : densenet121 (ImageNet weights, same backbone as the student's repo),
                 class-weighted loss, 10% of Training held out for picking the best epoch
4) evaluate    : (a) all 1,573 Validation leaves  (b) the SAME 190 images the VLM debate used
5) report      : results/jeju_cnn.md, results/jeju_cnn.json   (no images are written to results/)
"""
import argparse, csv, json, os, random, shutil, subprocess, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'src'))
from vp_core import data_root

FOLDERS = {'잎_정상': 'Healthy', '잎_궤양병': 'Canker', '잎_귤응애': 'Citrus Red Mite', '잎_진딧물': 'Aphid'}
CLASSES = ['Healthy', 'Canker', 'Citrus Red Mite', 'Aphid']
KO = {'Healthy': '정상', 'Canker': '궤양병', 'Citrus Red Mite': '귤응애', 'Aphid': '진딧물'}
VENV = (Path('C:/citrus-git') if os.name == 'nt' else Path.home() / 'citrus-git') / 'jeju_cnn_venv'
VPY = VENV / ('Scripts/python.exe' if os.name == 'nt' else 'bin/python')
LOG = ROOT / 'logs' / 'jeju_cnn.log'
OUT256 = data_root() / 'aihub_256'


def log(s=''):
    line = f"[{time.strftime('%H:%M:%S')}] {s}"
    try: print(line, flush=True)
    except Exception: print(line.encode('ascii', 'replace').decode(), flush=True)
    LOG.parent.mkdir(exist_ok=True)
    with open(LOG, 'a', encoding='utf-8') as f: f.write(line + '\n')


# ───────────────────────── 1) environment (runs with the normal Python) ─────────────────────────
def sh(cmd, check=True):
    log('$ ' + ' '.join(map(str, cmd)))
    p = subprocess.Popen([str(c) for c in cmd], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         env=dict(os.environ, PYTHONUTF8='1', PYTHONIOENCODING='utf-8', PYTHONUNBUFFERED='1'))
    for raw in iter(p.stdout.readline, b''):
        s = raw.decode('utf-8', 'replace').rstrip()
        if s: log('    ' + s[-300:])
    rc = p.wait()
    if check and rc: raise RuntimeError(f'failed rc={rc}: {cmd[:3]}')
    return rc


def ensure_env():
    if not VPY.exists():
        VENV.parent.mkdir(parents=True, exist_ok=True)
        sh([sys.executable, '-m', 'venv', VENV])
    sh([VPY, '-m', 'pip', 'install', '-q', '--upgrade', 'pip'])
    code = "import torch,torchvision,PIL;print(torch.cuda.is_available())"
    r = subprocess.run([str(VPY), '-c', code], capture_output=True, text=True)
    gpu = shutil.which('nvidia-smi') is not None
    if r.returncode != 0 or (gpu and 'True' not in r.stdout):
        ok = False
        if gpu:
            for idx in ('cu124', 'cu126', 'cu121'):
                if sh([VPY, '-m', 'pip', 'install', '-q', '--upgrade', 'torch', 'torchvision',
                       '--index-url', f'https://download.pytorch.org/whl/{idx}'], check=False) == 0:
                    ok = True; break
        if not ok: sh([VPY, '-m', 'pip', 'install', '-q', 'torch', 'torchvision'])
        sh([VPY, '-m', 'pip', 'install', '-q', 'pillow'])
    sh([VPY, '-c', "import torch;print('torch',torch.__version__,'cuda',torch.cuda.is_available(),"
                   "torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU')"])


# ───────────────────────── 2) data ─────────────────────────
def find(kind):
    hits = [p for p in (data_root() / 'aihub').rglob(f'{kind}.*') if p.is_dir()]
    return hits[0] if hits else None


def resize_all():
    from PIL import Image
    made = 0
    for split, kind in (('train', 'TS1'), ('val', 'VS1')):
        src = find(kind)
        if not src: raise SystemExit(f'{kind} folder not found under {data_root()/"aihub"} - run step 13 first')
        for folder in FOLDERS:
            dst = OUT256 / split / folder; dst.mkdir(parents=True, exist_ok=True)
            for f in sorted((src / folder).iterdir()):
                if f.suffix.lower() not in ('.jpg', '.jpeg', '.png'): continue
                t = dst / (f.stem + '.jpg')
                if t.exists(): continue
                im = Image.open(f).convert('RGB'); im.thumbnail((256, 256)); im.save(t, quality=92); made += 1
                if made % 2000 == 0: log(f'  resized {made} ...')
    counts = {s: {FOLDERS[k]: len(list((OUT256 / s / k).glob('*.jpg'))) for k in FOLDERS} for s in ('train', 'val')}
    log(f'256px copies: {made} new  {counts}')
    return counts


def vlm_190():
    """image names + truth of the 190 images in the Jeju VLM runs, and the VLM answers per condition"""
    out = {}
    for tag in ('ev-on', 'ev-hard', 'ev-off'):
        runs = sorted((ROOT / 'results').glob(f'*_main200_jeju_{tag}'))
        if not runs: continue
        rows = list(csv.DictReader(open(runs[-1] / 'panda_results.csv', encoding='utf-8-sig')))
        out[tag] = {r['image_name']: (r['gt_disease'], r['r1_consensus_disease'], r['r3_consensus_disease']) for r in rows}
    return out


# ───────────────────────── 3-4) train + evaluate (runs inside the venv) ─────────────────────────
def train_eval(seed, epochs, bs, subset_names):
    import torch, torch.nn as nn
    from torch.utils.data import Dataset, DataLoader
    from torchvision import models, transforms as T
    from PIL import Image
    random.seed(seed); torch.manual_seed(seed)
    dev = 'cuda' if torch.cuda.is_available() else 'cpu'
    ci = {c: i for i, c in enumerate(CLASSES)}

    def items(split):
        L = []
        for folder, c in FOLDERS.items():
            L += [(p, ci[c]) for p in sorted((OUT256 / split / folder).glob('*.jpg'))]
        return L
    tr_all, test = items('train'), items('val')
    rng = random.Random(seed); hold = []
    by = {}
    for it in tr_all: by.setdefault(it[1], []).append(it)
    tr = []
    for k, v in by.items():
        rng.shuffle(v); n = max(1, len(v) // 10); hold += v[:n]; tr += v[n:]
    norm = T.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    aug = T.Compose([T.RandomResizedCrop(224, scale=(0.6, 1.0)), T.RandomHorizontalFlip(), T.RandomVerticalFlip(),
                     T.RandomRotation(20), T.ColorJitter(0.2, 0.2, 0.2), T.ToTensor(), norm])
    plain = T.Compose([T.Resize(224), T.CenterCrop(224), T.ToTensor(), norm])

    class DS(Dataset):
        def __init__(s, L, tf): s.L, s.tf = L, tf
        def __len__(s): return len(s.L)
        def __getitem__(s, i):
            p, y = s.L[i]; return s.tf(Image.open(p).convert('RGB')), y

    nw = 4 if os.name == 'nt' else 6
    dl_tr = DataLoader(DS(tr, aug), bs, shuffle=True, num_workers=nw, pin_memory=dev == 'cuda', drop_last=True,
                       persistent_workers=True)
    def loader(L): return DataLoader(DS(L, plain), 64, shuffle=False, num_workers=nw, pin_memory=dev == 'cuda')
    cnt = [sum(1 for _, y in tr if y == k) for k in range(len(CLASSES))]
    w = torch.tensor([sum(cnt) / (len(cnt) * c) for c in cnt], dtype=torch.float32, device=dev)
    init = 'ImageNet'
    try: m = models.densenet121(weights=models.DenseNet121_Weights.IMAGENET1K_V1)
    except Exception as e: log(f'  ImageNet weights unavailable ({e}) - training from scratch'); m = models.densenet121(); init = 'scratch'
    m.classifier = nn.Linear(m.classifier.in_features, len(CLASSES)); m.to(dev)
    opt = torch.optim.AdamW(m.parameters(), lr=1e-4, weight_decay=1e-4)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, epochs)
    lossf = nn.CrossEntropyLoss(weight=w)
    scaler = torch.amp.GradScaler('cuda', enabled=dev == 'cuda')

    def predict(L):
        m.eval(); P = []
        with torch.no_grad(), torch.autocast(dev, enabled=dev == 'cuda'):
            for x, _ in loader(L): P += m(x.to(dev)).argmax(1).tolist()
        return P

    def bal(y, p):
        r = [sum(1 for a, b in zip(y, p) if a == k and b == k) / max(1, sum(1 for a in y if a == k)) for k in range(len(CLASSES))]
        return sum(r) / len(r), r

    best, best_state = -1, None
    log(f'seed {seed}: train {len(tr)} / hold-out {len(hold)} / test {len(test)}  class counts {cnt}  device {dev}')
    for ep in range(epochs):
        m.train(); t0 = time.time(); tot = 0
        for x, y in dl_tr:
            x, y = x.to(dev, non_blocking=True), y.to(dev, non_blocking=True)
            opt.zero_grad(set_to_none=True)
            with torch.autocast(dev, enabled=dev == 'cuda'):
                loss = lossf(m(x), y)
            scaler.scale(loss).backward(); scaler.step(opt); scaler.update(); tot += loss.item()
        sched.step()
        hb, _ = bal([y for _, y in hold], predict(hold))
        log(f'  epoch {ep+1}/{epochs}  loss {tot/len(dl_tr):.3f}  hold-out bal.acc {hb:.3f}  ({time.time()-t0:.0f}s)')
        if hb > best: best, best_state = hb, {k: v.detach().cpu().clone() for k, v in m.state_dict().items()}
    m.load_state_dict(best_state)
    yt = [y for _, y in test]; pt = predict(test)
    names = [p.name for p, _ in test]
    conf = [[sum(1 for a, b in zip(yt, pt) if a == i and b == j) for j in range(len(CLASSES))] for i in range(len(CLASSES))]
    b_all, r_all = bal(yt, pt)
    res = {'seed': seed, 'init': init, 'hold_bal': best, 'all': {'n': len(yt), 'acc': sum(a == b for a, b in zip(yt, pt)) / len(yt),
           'bal_acc': b_all, 'recall': dict(zip(CLASSES, r_all)), 'confusion': conf}}
    sub = [(y, p) for n, y, p in zip(names, yt, pt) if n in subset_names]
    if sub:
        ys, ps = zip(*sub); b_s, r_s = bal(list(ys), list(ps))
        res['vlm190'] = {'n': len(sub), 'acc': sum(a == b for a, b in sub) / len(sub), 'bal_acc': b_s,
                         'recall': dict(zip(CLASSES, r_s)),
                         'pred': {n: CLASSES[p] for n, y, p in zip(names, yt, pt) if n in subset_names}}
    log(f'  seed {seed}: all-val acc {res["all"]["acc"]:.3f} bal {b_all:.3f}'
        + (f' | 190-subset acc {res["vlm190"]["acc"]:.3f} bal {res["vlm190"]["bal_acc"]:.3f}' if sub else ''))
    return res


def vlm_metrics(vlm):
    out = {}
    for tag, d in vlm.items():
        for stage, idx in (('R1', 1), ('R3', 2)):
            y = [v[0] for v in d.values()]; p = [v[idx] for v in d.values()]
            rec = {c: sum(1 for a, b in zip(y, p) if a == c and b == c) / max(1, sum(1 for a in y if a == c)) for c in CLASSES}
            out[f'{tag} {stage}'] = {'acc': sum(a == b for a, b in zip(y, p)) / len(y), 'bal_acc': sum(rec.values()) / 4, 'recall': rec}
    return out


def report(runs, vlm, counts, epochs):
    import statistics as st
    def ms(v): return f'{st.mean(v):.3f} ± {st.stdev(v):.3f}' if len(v) > 1 else f'{v[0]:.3f}'
    vm = vlm_metrics(vlm)
    L = ['# Jeju CNN (AI Hub 635) vs VLM debate', '',
         f'{time.strftime("%Y-%m-%d %H:%M")} · densenet121 (init: {", ".join(sorted({r.get("init", "?") for r in runs}))}) · {epochs} epochs · seeds {", ".join(str(r["seed"]) for r in runs)}', '',
         f'- Training: AI Hub Training leaves {sum(counts["train"].values())} (90% train / 10% hold-out for epoch selection): {counts["train"]}',
         f'- Test: AI Hub Validation leaves {sum(counts["val"].values())} (not used in training): {counts["val"]}',
         '- Same farms and season appear in both AI Hub splits, so this is an in-distribution test.', '',
         '## Same 190 images as the VLM debate', '',
         '| model | acc | balanced acc | Healthy | Canker | Citrus Red Mite | Aphid |', '|---|---|---|---|---|---|---|']
    s190 = [r['vlm190'] for r in runs if 'vlm190' in r]
    if s190:
        L.append(f"| **CNN (mean ± sd)** | {ms([r['acc'] for r in s190])} | {ms([r['bal_acc'] for r in s190])} | "
                 + ' | '.join(ms([r['recall'][c] for r in s190]) for c in CLASSES) + ' |')
    for k in ('ev-on R1', 'ev-off R3', 'ev-on R3', 'ev-hard R3'):
        if k in vm:
            v = vm[k]; name = {'ev-on R1': 'VLM before debate (R1 vote)', 'ev-off R3': 'VLM after debate, OFF',
                               'ev-on R3': 'VLM after debate, ON', 'ev-hard R3': 'VLM after debate, HARD'}[k]
            L.append(f"| {name} | {v['acc']:.3f} | {v['bal_acc']:.3f} | " + ' | '.join(f"{v['recall'][c]:.2f}" for c in CLASSES) + ' |')
    L += ['', f'## All {runs[0]["all"]["n"]} Validation leaves', '', '| seed | acc | balanced acc | ' + ' | '.join(CLASSES) + ' |',
          '|---|---|---|' + '---|' * len(CLASSES)]
    for r in runs:
        a = r['all']; L.append(f"| {r['seed']} | {a['acc']:.3f} | {a['bal_acc']:.3f} | " + ' | '.join(f"{a['recall'][c]:.3f}" for c in CLASSES) + ' |')
    L.append(f"| mean ± sd | {ms([r['all']['acc'] for r in runs])} | {ms([r['all']['bal_acc'] for r in runs])} | "
             + ' | '.join(ms([r['all']['recall'][c] for r in runs]) for c in CLASSES) + ' |')
    L += ['', f'## Confusion matrix (seed {runs[0]["seed"]}, all Validation leaves; rows = truth, cols = prediction)', '',
          '| truth \\ pred | ' + ' | '.join(CLASSES) + ' |', '|---|' + '---|' * len(CLASSES)]
    for c, row in zip(CLASSES, runs[0]['all']['confusion']): L.append(f'| {c} | ' + ' | '.join(map(str, row)) + ' |')
    (ROOT / 'results' / 'jeju_cnn.md').write_text('\n'.join(L) + '\n', encoding='utf-8')
    (ROOT / 'results' / 'jeju_cnn.json').write_text(json.dumps({'runs': runs, 'vlm': vm, 'counts': counts}, ensure_ascii=False, indent=1), encoding='utf-8')
    log('report -> results/jeju_cnn.md')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--seeds', type=int, nargs='+', default=[42, 1, 2])
    ap.add_argument('--epochs', type=int, default=10)
    ap.add_argument('--bs', type=int, default=32)
    ap.add_argument('--inner', action='store_true', help=argparse.SUPPRESS)
    a = ap.parse_args()
    if not a.inner:                       # normal Python: set up, then re-run inside the venv
        log('=' * 60); log('JEJU CNN START')
        ensure_env()
        rc = subprocess.call([str(VPY), '-u', __file__, '--inner', '--epochs', str(a.epochs), '--bs', str(a.bs),
                              '--seeds'] + [str(s) for s in a.seeds])
        log('JEJU CNN END rc=%d' % rc); sys.exit(rc)
    counts = resize_all()
    vlm = vlm_190()
    names = set(next(iter(vlm.values())).keys()) if vlm else set()
    log(f'VLM 190-image list: {len(names)} images')
    done = ROOT / 'results' / 'jeju_cnn_runs.json'
    runs = json.loads(done.read_text(encoding='utf-8')) if done.exists() else []
    for s in a.seeds:
        if any(r['seed'] == s for r in runs): log(f'seed {s}: already done'); continue
        runs.append(train_eval(s, a.epochs, a.bs, names))
        done.write_text(json.dumps(runs, ensure_ascii=False), encoding='utf-8')
        report(runs, vlm, counts, a.epochs)
    report(runs, vlm, counts, a.epochs)
    log('DONE')


if __name__ == '__main__':
    main()
