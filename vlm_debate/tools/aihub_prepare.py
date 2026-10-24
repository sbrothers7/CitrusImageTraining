"""Step 14 - AI Hub dataset 635 (Jeju C. unshiu): overview + experiment specs.

1) Scan every label JSON (Training + Validation): class codes, annotation fields
   (ANTN_TY / ANTN_PT), farms (LCINFO), shooting months.  -> results/aihub_overview.json
2) Make 768px copies of the Validation images (same as the Zenodo set) into
   <data_root>/aihub_768/<folder>/  (originals are untouched).
3) Write experiment specs (paths relative to data_root):
     data/citrusJ_aihub_leaf.json   Healthy / Canker / Citrus Red Mite / Aphid  (leaves)
     data/citrusJ_aihub_fruit.json  Healthy / Canker                            (fruit)
AI Hub images never go to GitHub (see tools/gitignore_vlm.txt).
"""
import json, os, sys, shutil, collections, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'src'))
from vp_core import data_root
from PIL import Image

AIHUB = data_root() / 'aihub'
OUT768 = data_root() / 'aihub_768'
LOG = ROOT / 'logs' / 'aihub_prepare.log'
LEAF = {'잎_정상': 'Healthy', '잎_궤양병': 'Canker', '잎_귤응애': 'Citrus Red Mite', '잎_진딧물': 'Aphid'}
FRUIT = {'열매_정상': 'Healthy', '열매_궤양병': 'Canker'}


def log(s=''):
    print(s, flush=True)
    with open(LOG, 'a', encoding='utf-8') as f: f.write(s + '\n')


def find(kind):
    """kind: 'TL1' 'VL1' 'TS1' 'VS1' -> extracted folder"""
    hits = [p for p in AIHUB.rglob(f'{kind}.*') if p.is_dir()]
    return hits[0] if hits else None


def scan_labels():
    ov = {}
    for kind in ('TL1', 'VL1'):
        d = find(kind)
        if not d: log(f'!! {kind} folder not found'); continue
        st = dict(n=0, folder_class=collections.Counter(), antn_ty=collections.Counter(),
                  antn_pt_nonnull=0, farms=collections.Counter(), months=collections.Counter(),
                  place=collections.Counter(), growth=collections.Counter(), dbyhs=collections.Counter(),
                  mismatch=0, examples_with_pt=[])
        for j in d.rglob('*.json'):
            try: js = json.loads(j.read_text(encoding='utf-8-sig'))
            except Exception as e: log(f'  bad json {j.name}: {e}'); continue
            st['n'] += 1
            info, an = js.get('Info', {}), js.get('Annotations', {}) or {}
            folder = j.parent.name
            code = an.get('OBJECT_CLASS_CODE')
            st['folder_class'][f'{folder} -> {code}'] += 1
            st['antn_ty'][str(an.get('ANTN_TY'))] += 1
            if an.get('ANTN_PT') not in (None, '', [], {}):
                st['antn_pt_nonnull'] += 1
                if len(st['examples_with_pt']) < 3: st['examples_with_pt'].append(str(j))
            st['farms'][info.get('LCINFO')] += 1
            st['months'][str(info.get('IMAGE_POTOGRF_DT', ''))[:7]] += 1
            st['place'][info.get('IMAGE_OBTAIN_PLACE_TY')] += 1
            st['growth'][info.get('GRWH_STEP_CODE')] += 1
            st['dbyhs'][f"{folder}:{info.get('DBYHS')}"] += 1
        ov[kind] = {k: (dict(v.most_common()) if isinstance(v, collections.Counter) else v) for k, v in st.items()}
        log(f'[{kind}] {st["n"]} json | ANTN_PT filled: {st["antn_pt_nonnull"]} | ANTN_TY: {dict(st["antn_ty"])}')
        for k, v in st['folder_class'].most_common(): log(f'    {k}: {v}')
        log(f'    farms: {dict(st["farms"].most_common())}')
        log(f'    months: {dict(sorted(st["months"].items()))}')
        log(f'    place: {dict(st["place"])}  growth: {dict(st["growth"])}')
    smp = ROOT / 'results' / 'aihub_samples'
    for kind in ov:
        for p in ov[kind]['examples_with_pt']:
            smp.mkdir(parents=True, exist_ok=True); shutil.copy2(p, smp / ('PT_' + Path(p).name))
    (ROOT / 'results' / 'aihub_overview.json').write_text(json.dumps(ov, ensure_ascii=False, indent=1), encoding='utf-8')


def resize_validation():
    src = find('VS1')
    if not src: log('!! VS1 not found'); return {}
    made, counts = 0, {}
    for folder in list(LEAF) + list(FRUIT):
        d = src / folder
        if not d.exists(): log(f'!! missing {d}'); continue
        dst = OUT768 / folder; dst.mkdir(parents=True, exist_ok=True)
        files = sorted(f for f in d.iterdir() if f.suffix.lower() in ('.jpg', '.jpeg', '.png'))
        for f in files:
            t = dst / (f.stem + '.jpg')
            if t.exists(): continue
            im = Image.open(f).convert('RGB'); im.thumbnail((768, 768)); im.save(t, quality=92); made += 1
        counts[folder] = len(list(dst.glob('*.jpg')))
    log(f'768px copies: {made} new, per folder {counts}  -> {OUT768}')
    return counts


def write_specs(counts):
    for name, mp, desc in (('citrusJ_aihub_leaf', LEAF, 'leaves'), ('citrusJ_aihub_fruit', FRUIT, 'fruit')):
        spec = {'crop': 'Citrus',
                'source': f'AI Hub 635 (Jeju C. unshiu, Validation split, {desc}), images resized to 768px',
                'counts': {mp[k]: counts.get(k, 0) for k in mp},
                'classes': {mp[k]: [f'aihub_768/{k}'] for k in mp},
                'paths_relative_to': 'CITRUS_DATA (default: ~/citrus-data on macOS/Linux, C:/citrus-data on Windows)'}
        p = ROOT / 'data' / f'{name}.json'
        p.write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding='utf-8')
        log(f'wrote {p.relative_to(ROOT)}: {spec["counts"]}')


if __name__ == '__main__':
    (ROOT / 'logs').mkdir(exist_ok=True)
    log('=' * 60); log(time.strftime('%Y-%m-%d %H:%M:%S') + f'  AI Hub prepare  data={AIHUB}')
    try:
        scan_labels(); write_specs(resize_validation()); log('DONE')
    except Exception:
        import traceback; log(traceback.format_exc()); log('FAILED')
