r"""
Reproduce the student's CNN experiment (github.com/sbrothers7/CitrusImageTraining, main)
and repeat it with several seeds.  Works on Windows / macOS / Linux.

  py tools\verify_student_cnn.py            (11_verify_student_cnn.bat runs this)
  python3 tools/verify_student_cnn.py --seeds 42 1 2

What it does
  1) clone / update the student's repo into  <home>/citrus-git/student_main   (never pushes)
  2) .venv there with PyTorch (CUDA if available) + requirements + kagglehub
  3) build_data.py  (reuses our CitrusUAT zip if we already have it)
  4) densenet121, for each seed:  ONE source (Citrus Leaves only)  vs  TWO sources (+ Orange Leaves HLB 2025)
  5) table -> results/verify_student_cnn.md, full log -> logs/verify_student.log
Claims being checked (docs/03_research_notebook.md, experiment #2, seed 42):
  one source : A test 100.0%, B balanced acc 0.556, B MCC 0.067, 294 train images
  two sources: A test  98.2%, B balanced acc 0.623, B MCC 0.095, 521 train images
"""
import argparse, json, os, re, shutil, subprocess, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'src'))
from vp_core import data_root
LOG = ROOT / 'logs' / 'verify_student.log'; LOG.parent.mkdir(exist_ok=True)
REPO_URL = 'https://github.com/sbrothers7/CitrusImageTraining.git'
STU = (Path('C:/citrus-git') if os.name == 'nt' else Path.home() / 'citrus-git') / 'student_main'
VPY = STU / ('.venv/Scripts/python.exe' if os.name == 'nt' else '.venv/bin/python')
CLAIM = {'one': (1.000, 0.556, 0.067, 294), 'two': (0.982, 0.623, 0.095, 521)}
_f = open(LOG, 'a', encoding='utf-8')


def log(s=''):
    line = f"[{time.strftime('%H:%M:%S')}] {s}"
    try: print(line, flush=True)
    except Exception: print(line.encode('ascii', 'replace').decode(), flush=True)
    _f.write(line + '\n'); _f.flush()


def git_exe():
    g = shutil.which('git')
    if g: return g
    for c in (Path(os.environ.get('ProgramFiles', 'C:/Program Files')) / 'Git/cmd/git.exe',):
        if c.exists(): return str(c)
    sys.exit('git not found')


ENV = dict(os.environ, PYTHONUTF8='1', PYTHONIOENCODING='utf-8', PYTHONUNBUFFERED='1')


def sh(cmd, cwd=STU, check=True, quiet_progress=True):
    log('$ ' + ' '.join(map(str, cmd)))
    p = subprocess.Popen([str(c) for c in cmd], cwd=cwd, env=ENV, stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL)
    last = 0.0
    for raw in iter(p.stdout.readline, b''):
        s = raw.decode('utf-8', 'replace').rstrip()
        if not s: continue
        # thin out progress bars
        if quiet_progress and ('%|' in s or 'it/s' in s or 's/it' in s) and time.time() - last < 20:
            continue
        last = time.time()
        _f.write('    ' + s[-500:] + '\n'); _f.flush()
        print('    ' + s[-200:], flush=True)
    rc = p.wait()
    if check and rc != 0:
        raise RuntimeError(f'command failed (rc={rc}): {cmd[:3]}')
    return rc


def setup():
    g = git_exe()
    ENV['PATH'] = str(Path(g).parent) + os.pathsep + ENV.get('PATH', '')
    STU.parent.mkdir(parents=True, exist_ok=True)
    if not (STU / '.git').exists():
        sh([g, 'clone', REPO_URL, STU], cwd=STU.parent)
    sh([g, 'fetch', 'origin'])
    sh([g, 'checkout', '-f', 'main'])
    sh([g, 'reset', '--hard', 'origin/main'])      # local clone only; nothing is pushed
    sh([g, 'log', '--oneline', '-3'])
    if not VPY.exists():
        sh([sys.executable, '-m', 'venv', '.venv'])
    sh([VPY, '-m', 'pip', 'install', '-q', '--upgrade', 'pip'])
    has_nvidia = shutil.which('nvidia-smi') is not None
    code = "import torch,sys;print(torch.__version__,torch.cuda.is_available());sys.exit(0)"
    have = subprocess.run([str(VPY), '-c', code], capture_output=True, text=True)
    if have.returncode != 0 or (has_nvidia and 'True' not in have.stdout):
        ok = False
        if has_nvidia:
            for idx in ('cu124', 'cu126', 'cu121'):
                if sh([VPY, '-m', 'pip', 'install', '-q', '--upgrade', 'torch', 'torchvision',
                       '--index-url', f'https://download.pytorch.org/whl/{idx}'], check=False) == 0:
                    ok = True; break
        if not ok:
            sh([VPY, '-m', 'pip', 'install', '-q', 'torch', 'torchvision'])
    sh([VPY, '-m', 'pip', 'install', '-q', '-r', 'requirements.txt', 'kagglehub'])
    sh([VPY, '-c', "import torch;print('torch',torch.__version__,'cuda',torch.cuda.is_available(),"
                   "torch.cuda.get_device_name(0) if torch.cuda.is_available() else '')"])


def build_data():
    dl = STU / 'data' / 'datasets' / '_downloads'
    dl.mkdir(parents=True, exist_ok=True)
    ours = data_root() / 'zenodo_8294078' / '_download' / 'CitrusUAT_dataset.zip'
    tgt = dl / 'CitrusUAT_dataset.zip'
    if ours.exists() and not tgt.exists():
        try: os.link(ours, tgt); log(f'linked our CitrusUAT zip -> {tgt}')
        except OSError: shutil.copy2(ours, tgt); log(f'copied our CitrusUAT zip -> {tgt}')
    sh([VPY, 'build_data.py'])


HELD = lambda: STU / 'data' / '_held_out_second_source'


def set_arm(arm):
    """one: move source_A/<cls>/orange_leaves_hlb_2025 aside; two: put it back"""
    A = STU / 'data' / 'raw' / 'source_A'
    if arm == 'one':
        for sub in A.glob('*/orange_leaves_hlb_2025'):
            dst = HELD() / sub.parent.name
            dst.parent.mkdir(parents=True, exist_ok=True)
            if dst.exists(): shutil.rmtree(dst)
            shutil.move(str(sub), str(dst))
    else:
        if HELD().exists():
            for d in HELD().iterdir():
                dst = A / d.name / 'orange_leaves_hlb_2025'
                if not dst.exists(): shutil.move(str(d), str(dst))
            shutil.rmtree(HELD(), ignore_errors=True)
    n = {c.name: sum(1 for f in c.rglob('*') if f.is_file()) for c in sorted(A.iterdir()) if c.is_dir()}
    log(f'arm={arm}  source_A images per class: {n}')


def set_seed_cfg(seed):
    cfg = STU / 'config.yaml'
    t = cfg.read_text(encoding='utf-8')
    t = re.sub(r'(?m)^seed:\s*\d+', f'seed: {seed}', t)
    cfg.write_text(t, encoding='utf-8')


def one_run(arm, seed):
    tag = f'verify_{arm}_s{seed}'
    rd = STU / 'results' / f'densenet121_{tag}'
    out, nt = rd / 'metrics' / '03_all_metrics.json', rd / 'n_train.txt'
    if out.exists() and nt.exists():
        log(f'--- {tag}: already done, reusing')
        return json.loads(out.read_text(encoding='utf-8')), int(nt.read_text())
    log(f'=== {tag} ===')
    set_arm(arm); set_seed_cfg(seed)
    sh([VPY, 'run_1_prepare.py'])
    n = n_train_images()
    sh([VPY, 'run_2_train.py', '--model', 'densenet121', '--tag', tag])
    sh([VPY, 'run_3_evaluate.py', '--model', 'densenet121', '--tag', tag])
    nt.write_text(str(n))
    return json.loads(out.read_text(encoding='utf-8')), n


def row(arm, seed, m, n_train):
    A, B = m.get('A_test', {}), m.get('B', {})
    return {'arm': arm, 'seed': seed, 'n_train': n_train, 'A_acc': A.get('accuracy'),
            'B_bal': B.get('recall_macro'), 'B_mcc': B.get('mcc'), 'B_n': B.get('n_samples'),
            'by_origin': {k: v['accuracy'] for k, v in m.get('B_by_origin', {}).items()}}


def n_train_images():
    import csv
    f = STU / 'results' / 'manifests' / 'source_A.csv'
    rows = list(csv.DictReader(open(f, encoding='utf-8')))
    return sum(1 for r in rows if r['split'] == 'train')


def report(rows):
    import statistics as st
    L = ['# Verification of the student CNN experiment', '',
         f'{time.strftime("%Y-%m-%d %H:%M")} · densenet121 · repo {REPO_URL} (main)', '',
         '| arm | seed | train imgs | A test acc | B balanced acc | B MCC | B imgs |',
         '|---|---|---|---|---|---|---|']
    for r in rows:
        L.append(f"| {r['arm']} | {r['seed']} | {r['n_train']} | {r['A_acc']:.3f} | {r['B_bal']:.3f} | "
                 f"{r['B_mcc']:.3f} | {r['B_n']} |")
    L += ['', '## Student claims (seed 42) vs reproduction', '',
          '| arm | claimed A / B bal / MCC / train | reproduced (seed 42) |', '|---|---|---|']
    for arm in ('one', 'two'):
        c = CLAIM[arm]; r = [x for x in rows if x['arm'] == arm and x['seed'] == 42]
        rep = (f"{r[0]['A_acc']:.3f} / {r[0]['B_bal']:.3f} / {r[0]['B_mcc']:.3f} / {r[0]['n_train']}" if r else '-')
        L.append(f"| {arm} | {c[0]:.3f} / {c[1]:.3f} / {c[2]:.3f} / {c[3]} | {rep} |")
    L += ['', '## Across seeds (mean ± sd of B balanced accuracy)', '']
    for arm in ('one', 'two'):
        v = [x['B_bal'] for x in rows if x['arm'] == arm]
        if len(v) > 1: L.append(f"- {arm}: {st.mean(v):.3f} ± {st.stdev(v):.3f}  (n={len(v)}: {', '.join(f'{x:.3f}' for x in v)})")
    seeds = sorted({x['seed'] for x in rows})
    diffs = []
    for s in seeds:
        a = [x for x in rows if x['seed'] == s and x['arm'] == 'one']; b = [x for x in rows if x['seed'] == s and x['arm'] == 'two']
        if a and b: diffs.append(b[0]['B_bal'] - a[0]['B_bal'])
    if diffs:
        L.append(f"- two − one, per seed: {', '.join(f'{d:+.3f}' for d in diffs)}  "
                 f"(positive in {sum(d > 0 for d in diffs)}/{len(diffs)} seeds)")
    L += ['', '## B accuracy by origin', '']
    origins = sorted({k for r in rows for k in r['by_origin']})
    L.append('| origin | ' + ' | '.join(f"{r['arm']} s{r['seed']}" for r in rows) + ' |')
    L.append('|---|' + '---|' * len(rows))
    for o in origins:
        L.append(f'| {o} | ' + ' | '.join(f"{r['by_origin'].get(o, float('nan')):.3f}" for r in rows) + ' |')
    (ROOT / 'results').mkdir(exist_ok=True)
    out = ROOT / 'results' / 'verify_student_cnn.md'
    out.write_text('\n'.join(L), encoding='utf-8')
    (ROOT / 'results' / 'verify_student_cnn.json').write_text(json.dumps(rows, indent=1), encoding='utf-8')
    log('\n'.join(L))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--seeds', type=int, nargs='+', default=[42, 1, 2])
    ap.add_argument('--skip-setup', action='store_true')
    a = ap.parse_args()
    log('=' * 70); log(f'VERIFY START  python={sys.version.split()[0]}  target={STU}')
    if not a.skip_setup:
        setup(); build_data()
    rows = []
    try:
        for seed in a.seeds:
            for arm in ('one', 'two'):
                m, n = one_run(arm, seed)
                rows.append(row(arm, seed, m, n))
                report(rows)
    finally:
        set_arm('two')                                   # always restore the data
        subprocess.run([git_exe(), 'checkout', '--', 'config.yaml'], cwd=STU)
    log('VERIFY DONE')


if __name__ == '__main__':
    try: main()
    except Exception:
        import traceback; log(traceback.format_exc()); sys.exit(1)
