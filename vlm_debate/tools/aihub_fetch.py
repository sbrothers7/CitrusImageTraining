r"""
AI Hub "고품질 과수 작물 통합 데이터" (dataset 635): download ONLY the citrus RGB files
  VL1.감귤.zip (labels, validation)   VS1.감귤.zip (images, validation)
  TL1.감귤.zip (labels, training)     TS1.감귤.zip (images, training)
Hyperspectral (TS3/TL3), kiwi and weather files are skipped.

  py tools\aihub_fetch.py                (13_aihub_download.bat runs this)
  python3 tools/aihub_fetch.py --only-val   (validation part only, ~155 MB)

The API key is read from AIHUB_APIKEY in the project .env (or the env var); if absent it is asked for (hidden input).
It is never written to disk. Data goes to <CITRUS_DATA>/aihub  (default C:/citrus-data/aihub).
For Claude: logs/aihub_fetch.log, logs/aihub_tree.txt, results/aihub_samples/ (a few labels + images).
"""
import argparse, getpass, json, os, re, shutil, struct, subprocess, sys, time, zipfile
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'src'))
from vp_core import data_root
LOG = ROOT / 'logs' / 'aihub_fetch.log'; LOG.parent.mkdir(exist_ok=True)
WORK = data_root() / 'aihub'
DATASET = '635'
WANT = ['VL1', 'VS1', 'TL1', 'TS1']
IMG = {'.jpg', '.jpeg', '.png', '.bmp'}


def log(s=''):
    line = f"[{time.strftime('%H:%M:%S')}] {s}"
    try: print(line, flush=True)
    except Exception: print(line.encode('ascii', 'replace').decode(), flush=True)
    with open(LOG, 'a', encoding='utf-8') as f: f.write(line + '\n')


def find_bash():
    for c in (Path(os.environ.get('ProgramFiles', 'C:/Program Files')) / 'Git/bin/bash.exe',
              Path(os.environ.get('ProgramFiles(x86)', 'C:/Program Files (x86)')) / 'Git/bin/bash.exe'):
        if c.exists(): return str(c)
    b = shutil.which('bash')
    if b and 'system32' not in b.lower(): return b      # skip the WSL launcher
    sys.exit('bash not found (install Git for Windows)')


def shell_copy(src):
    """copy aihubshell into WORK with LF line endings"""
    WORK.mkdir(parents=True, exist_ok=True)
    dst = WORK / 'aihubshell'
    dst.write_bytes(src.read_bytes().replace(b'\r\n', b'\n'))
    return dst


def run(bash, args, env, keep=True):
    log('$ aihubshell ' + ' '.join(a if not a.isdigit() or len(a) < 30 else '***' for a in args))
    p = subprocess.Popen([bash, './aihubshell'] + args, cwd=WORK, env=env,
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out, last = [], 0
    for raw in iter(p.stdout.readline, b''):
        s = raw.decode('utf-8', 'replace').rstrip()
        if env.get('AIHUB_APIKEY'): s = s.replace(env['AIHUB_APIKEY'], '***')   # never log the key
        out.append(s)
        if keep and (('%' not in s) or time.time() - last > 15):   # thin curl progress
            last = time.time(); log('    ' + s[-300:])
    p.wait()
    return '\n'.join(out), p.returncode


BAD = '<>:"\\|?*'


def unicode_extra(info):
    """Info-ZIP Unicode Path extra field (0x7075): the real UTF-8 name."""
    ex, i = info.extra, 0
    while i + 4 <= len(ex):
        hid, size = struct.unpack('<HH', ex[i:i + 4])
        if hid == 0x7075 and size >= 5:
            try: return ex[i + 9:i + 4 + size].decode('utf-8')
            except UnicodeDecodeError: return None
        i += 4 + size
    return None


def extra_ids(info):
    ex, i, ids = info.extra, 0, []
    while i + 4 <= len(ex):
        hid, size = struct.unpack('<HH', ex[i:i + 4]); ids.append(hex(hid)); i += 4 + size
    return ids


def fix_name(info):
    u = unicode_extra(info)
    if u: return u
    if info.flag_bits & 0x800: return info.filename
    raw = info.filename.encode('cp437', 'replace')
    for enc in ('utf-8', 'cp949'):            # Korean zips: UTF-8 without the flag, or CP949
        try: return raw.decode(enc)
        except UnicodeDecodeError: pass
    return info.filename


def safe(name):
    """Windows-safe relative path; characters the zip lost become '_'."""
    parts = [p for p in name.replace('\\', '/').split('/') if p not in ('', '.', '..')]
    return '/'.join(''.join('_' if c in BAD or ord(c) < 32 else c for c in p).rstrip(' .') or '_'
                    for p in parts)


def extract_all():
    for z in sorted(WORK.rglob('*.zip')):
        dst = z.with_suffix('')
        if (dst / '.extracted').exists(): continue
        log(f'unzip {z.relative_to(WORK)}')
        if dst.exists(): shutil.rmtree(dst)   # half-finished earlier attempt
        dst.mkdir()
        lost = 0
        with zipfile.ZipFile(z) as zf:
            infos = zf.infolist()
            for info in infos[:3]:            # diagnosis for Claude
                log(f'    entry: flag={info.flag_bits:#x} extra={extra_ids(info)} '
                    f'raw={info.filename.encode("cp437", "replace")[:60].hex()} -> {fix_name(info)!r}')
            for info in infos:
                name = fix_name(info)
                if '?' in name: lost += 1
                rel = safe(name)
                if not rel: continue
                target = dst / rel
                if info.is_dir() or name.endswith('/'):
                    target.mkdir(parents=True, exist_ok=True); continue
                target.parent.mkdir(parents=True, exist_ok=True)
                if target.exists():           # two lost names collapsed to the same one
                    k = 1
                    while target.with_name(f'{target.stem}__{k}{target.suffix}').exists(): k += 1
                    target = target.with_name(f'{target.stem}__{k}{target.suffix}')
                with zf.open(info) as s, open(target, 'wb') as d: shutil.copyfileobj(s, d)
        if lost: log(f'    !! {lost} names had unrecoverable characters (saved with _)')
        (dst / '.extracted').write_text('ok')


def summarize():
    log('\n=== summary ===')
    for top in sorted(p for p in WORK.rglob('*') if p.is_dir() and (p / '.extracted').exists()):
        imgs = [f for f in top.rglob('*') if f.suffix.lower() in IMG]
        jsons = [f for f in top.rglob('*.json')]
        log(f'{top.relative_to(WORK)}: {len(imgs)} images, {len(jsons)} json')
        dirs = sorted({f.parent.relative_to(top).as_posix() for f in imgs + jsons})
        for d in dirs[:40]:
            n = sum(1 for f in (top / d).iterdir() if f.is_file())
            log(f'    {d}/  ({n} files)')
        if imgs:
            from PIL import Image
            sizes = {}
            for f in imgs[:200]:
                try: sizes[Image.open(f).size] = sizes.get(Image.open(f).size, 0) + 1
                except Exception: pass
            log(f'    image sizes (first 200): {sizes}')
    # samples for Claude: 4 label files from different folders + matching images
    S = ROOT / 'results' / 'aihub_samples'; S.mkdir(parents=True, exist_ok=True)
    labels = sorted(WORK.rglob('*.json'))
    by_dir = {}
    for j in labels: by_dir.setdefault(j.parent, []).append(j)
    picked = [v[0] for v in list(by_dir.values())[:6]]
    allimgs = {f.stem: f for f in WORK.rglob('*') if f.suffix.lower() in IMG}
    for j in picked:
        shutil.copy2(j, S / j.name)
        im = allimgs.get(j.stem)
        if im:
            from PIL import Image
            x = Image.open(im); x.thumbnail((1024, 1024)); x.convert('RGB').save(S / (j.stem + '.jpg'), quality=90)
            log(f'sample: {j.name} + image {im.name} {Image.open(im).size}')
        else:
            log(f'sample: {j.name} (no image with the same name)')


def env_key(name='AIHUB_APIKEY'):
    """Read one value from the project .env without printing or storing it."""
    if os.environ.get(name): return os.environ[name].strip()
    f = ROOT / '.env'
    if not f.exists(): return ''
    for line in f.read_text(encoding='utf-8-sig', errors='replace').splitlines():
        line = line.strip()
        if line.startswith('export '): line = line[7:].strip()
        if line.startswith('#') or '=' not in line: continue
        k, v = line.split('=', 1)
        if k.strip() == name:
            v = v.split(' #')[0].strip().strip('"').strip("'")
            return v
    return ''


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--shell', default=str(Path.home() / 'Downloads' / 'aihubshell'))
    ap.add_argument('--only-val', action='store_true')
    a = ap.parse_args()
    log('=' * 60); log(f'AI Hub fetch → {WORK}')
    bash = find_bash(); log(f'bash: {bash}')
    shell_copy(Path(a.shell))
    env = dict(os.environ)
    tree, _ = run(bash, ['-mode', 'l', '-datasetkey', DATASET], env, keep=False)
    (ROOT / 'logs' / 'aihub_tree.txt').write_text(tree, encoding='utf-8')
    keys = {}
    for line in tree.splitlines():
        m = re.search(r'((?:VL1|VS1|TL1|TS1))\.감귤\.zip\s*\|\s*([^|]+?)\s*\|\s*(\d+)', line)
        if m: keys[m.group(1)] = (m.group(3), m.group(2))
    log(f'file keys: {keys}')
    want = ['VL1', 'VS1'] if a.only_val else WANT
    missing = [w for w in want if w not in keys]
    if missing:
        log(f'!! could not find {missing} in the file tree (see logs/aihub_tree.txt). Stopping.'); return
    key = env_key()
    log('API key: from .env' if key else 'API key: not in .env, asking')
    key = key or getpass.getpass('AI Hub API key (input is hidden): ').strip()
    if not key: log('no API key'); return
    env['AIHUB_APIKEY'] = key
    done = [w for w in want if any(WORK.rglob(f'{w}.*.zip')) or any(WORK.rglob(f'{w}.*'))]
    todo = [w for w in want if w not in done]
    log(f'already present: {done}  to download: {todo}')
    for group in (['VL1', 'VS1'], ['TL1', 'TS1']):
        g = [w for w in group if w in todo]
        if not g: continue
        log(f'downloading {g} ({", ".join(keys[w][1] for w in g)})')
        out, rc = run(bash, ['-mode', 'd', '-datasetkey', DATASET, '-filekey', ','.join(keys[w][0] for w in g)], env)
        if 'Download failed' in out or 'Error' in out:
            log('!! download failed - see messages above'); return
    extract_all()
    summarize()
    log('DONE')


if __name__ == '__main__':
    try: main()
    except Exception:
        import traceback; log(traceback.format_exc())
