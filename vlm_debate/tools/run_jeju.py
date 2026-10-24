r"""
Step 15 - Jeju (AI Hub 635, C. unshiu leaves) main experiment, overnight.

  0) polygon check (1 min): what do the AI Hub polygons outline?  -> results/aihub_samples/PT_overlay_*.jpg
  1) ev-ON   n=200, seed 42             (full run, R1 computed)
  2) ev-HARD same images, R1 reused, changes without new evidence reverted
  3) ev-OFF  same images, R1 reused, anti-sycophancy OFF
  4) analysis of the jeju runs -> results/ANALYSIS_jeju.md  (results/ANALYSIS.md is kept)
Finished runs are skipped, so the step can simply be started again if it was interrupted.
Log: logs\main.log
"""
import json, re, shutil, subprocess, sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'tools')); sys.path.insert(0, str(ROOT / 'src'))
from run_main import run, log
from vp_core import data_root

DS = 'data/citrusJ_aihub_leaf.json'
BASE = ['--dataset', DS, '--n', '200', '--seed', '42']


def done(tag):
    hits = [d for d in sorted((ROOT / 'results').glob(f'*_{tag}')) if (d / 'summary.json').exists()]
    return hits[-1] if hits else None


def step(tag, extra):
    d = done(tag)
    if d: log(f'skip {tag} (already finished: {d.name})'); return d
    rc, out = run(BASE + extra + ['--tag', tag])
    return Path(out) if (rc == 0 and out) else done(tag)


def polygon_check():
    try:
        from PIL import Image, ImageDraw
        aihub = data_root() / 'aihub'
        rows = []
        for j in aihub.rglob('*.json'):
            if 'L1.' not in j.parent.parent.name: continue
            try: js = json.loads(j.read_text(encoding='utf-8-sig'))
            except Exception: continue
            an = js.get('Annotations') or {}
            if an.get('ANTN_TY') != 'polygon' or not an.get('ANTN_PT'): continue
            parts = re.findall(r'\[([^\]]*)\]', an['ANTN_PT'])
            if len(parts) < 2: continue
            xs = [float(v) for v in parts[0].split('|') if v.strip()]
            ys = [float(v) for v in parts[1].split('|') if v.strip()]
            n = min(len(xs), len(ys)); xs, ys = xs[:n], ys[:n]
            area = abs(sum(xs[i] * ys[(i + 1) % n] - xs[(i + 1) % n] * ys[i] for i in range(n))) / 2
            rows.append(dict(file=j.stem, folder=j.parent.name, n_pts=n, n_polys=len(parts) // 2,
                             area_frac=area / (1920 * 1080),
                             bbox=[min(xs), min(ys), max(xs), max(ys)], path=str(j)))
        if not rows: log('polygon check: none found'); return
        from collections import Counter
        fr = sorted(r['area_frac'] for r in rows)
        stat = dict(n=len(rows), by_folder=dict(Counter(r['folder'] for r in rows)),
                    n_polys=dict(Counter(r['n_polys'] for r in rows)),
                    area_frac_min=fr[0], area_frac_median=fr[len(fr) // 2], area_frac_max=fr[-1])
        log(f'polygon check: {stat}')
        (ROOT / 'results' / 'aihub_polygons.json').write_text(
            json.dumps(dict(stat=stat, rows=rows[:50]), ensure_ascii=False, indent=1), encoding='utf-8')
        smp = ROOT / 'results' / 'aihub_samples'; smp.mkdir(parents=True, exist_ok=True)
        for r in rows[:: max(1, len(rows) // 4)][:4]:
            jp = Path(r['path'])
            # label  .../라벨링데이터/TL1.감귤/<folder>/x.json -> image .../원천데이터/TS1.감귤/<folder>/x.jpg
            kind = jp.parent.parent.name.replace('L1.', 'S1.')
            img = jp.parent.parent.parent.parent / '원천데이터' / kind / jp.parent.name / (jp.stem + '.jpg')
            if not img.exists(): log(f'  image not found: {img}'); continue
            im = Image.open(img).convert('RGB')
            js = json.loads(jp.read_text(encoding='utf-8-sig'))
            parts = re.findall(r'\[([^\]]*)\]', js['Annotations']['ANTN_PT'])
            dr = ImageDraw.Draw(im)
            for k in range(0, len(parts) - 1, 2):
                xs = [float(v) for v in parts[k].split('|') if v.strip()]
                ys = [float(v) for v in parts[k + 1].split('|') if v.strip()]
                dr.line(list(zip(xs, ys)) + [(xs[0], ys[0])], fill=(255, 0, 255), width=6)
            im.thumbnail((1024, 1024)); im.save(smp / f'PT_overlay_{jp.stem}.jpg', quality=90)
        log('polygon overlays saved to results/aihub_samples/')
    except Exception as e:
        log(f'polygon check failed: {e}')


def analyze():
    res = ROOT / 'results'; main_md = res / 'ANALYSIS.md'; bak = res / '_ANALYSIS_main.bak'
    if main_md.exists(): shutil.copy2(main_md, bak)
    subprocess.run([sys.executable, 'tools/analyze.py', str(res), 'jeju'], cwd=ROOT)
    if main_md.exists(): shutil.move(str(main_md), str(res / 'ANALYSIS_jeju.md'))
    if bak.exists(): shutil.move(str(bak), str(main_md))
    log('analysis -> results/ANALYSIS_jeju.md')


def main():
    log('=' * 70); log(f'JEJU START {time.strftime("%Y-%m-%d %H:%M:%S")}')
    polygon_check()
    on = step('main200_jeju_ev-on', [])
    if not on: log('ev-ON failed - stopping'); return
    cache = str(on / 'vida_raw_bank.json')
    step('main200_jeju_ev-hard', ['--enforce', '--reuse-r1', cache])
    step('main200_jeju_ev-off', ['--no-evidence', '--reuse-r1', cache])
    analyze()
    log(f'JEJU END {time.strftime("%Y-%m-%d %H:%M:%S")}')


if __name__ == '__main__':
    main()
