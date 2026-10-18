r"""
Lesion localisation with the grounding ability of Qwen2.5-VL (via Ollama).
The debate itself only returns labels; this asks the model WHERE on the leaf it sees
the abnormality, as bounding boxes, so the result can be drawn on the image.

  py tools\localize_lesions.py            (12_localize.bat runs this)

Output (inside the project, so Claude can read it):
  results/figures/inputs/<id>.png      resized input image (coordinates refer to this)
  results/figures/localize.json        boxes + raw answers for each model
  results/figures/case/                original of the debate case-study image
"""
import base64, json, os, re, shutil, sys, time, urllib.request, random
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'src'))
import vp_core as C
from PIL import Image

OUT = ROOT / 'results' / 'figures'
(OUT / 'inputs').mkdir(parents=True, exist_ok=True); (OUT / 'case').mkdir(exist_ok=True)
HOST = os.environ.get('OLLAMA_HOST', 'http://localhost:11434')
MODELS = ['qwen2.5vl:7b', 'qwen2.5vl:3b']
CASES = ['Black spot/b (86).png', 'greening/g (96).png']      # debate case-study images (Dataset A)


def log(*a):
    s = ' '.join(map(str, a))
    try: print(s, flush=True)
    except Exception: print(s.encode('ascii', 'replace').decode(), flush=True)
    with open(ROOT / 'logs' / 'localize.log', 'a', encoding='utf-8') as f: f.write(s + '\n')


def resize28(im, target=448):
    w, h = im.size; s = target / max(w, h)
    W, H = max(28, round(w * s / 28) * 28), max(28, round(h * s / 28) * 28)
    return im.convert('RGB').resize((W, H), Image.BICUBIC)


PROMPT = ("You are a plant pathologist. Look at this citrus leaf image ({W}x{H} pixels). "
          "Locate every diseased lesion, spot, discoloured or abnormal region on the leaf. "
          "Answer ONLY with a JSON list like "
          '[{{"bbox_2d": [x1, y1, x2, y2], "label": "short description"}}] '
          "using pixel coordinates of this image. If the leaf looks healthy, answer [].")


def ask(model, img_path, W, H):
    b64 = base64.b64encode(open(img_path, 'rb').read()).decode()
    body = {'model': model, 'stream': False, 'options': {'temperature': 0, 'num_predict': 600},
            'messages': [{'role': 'user', 'content': PROMPT.format(W=W, H=H), 'images': [b64]}]}
    req = urllib.request.Request(HOST + '/api/chat', data=json.dumps(body).encode(),
                                 headers={'Content-Type': 'application/json'})
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=600) as r:
        txt = json.loads(r.read()).get('message', {}).get('content', '')
    return txt, time.time() - t0


def parse_boxes(txt, W, H):
    m = re.search(r'\[.*\]', txt, re.S)
    if not m: return None
    try: items = json.loads(m.group(0))
    except Exception:
        items = [{'bbox_2d': [float(v) for v in b]} for b in
                 re.findall(r'\[\s*([\d.]+)\s*,\s*([\d.]+)\s*,\s*([\d.]+)\s*,\s*([\d.]+)\s*\]', m.group(0))]
    boxes = []
    for it in items if isinstance(items, list) else []:
        b = it.get('bbox_2d') or it.get('bbox') if isinstance(it, dict) else None
        if not b or len(b) != 4: continue
        b = [float(v) for v in b]
        mx = max(b)
        if mx <= 1.0: b = [b[0] * W, b[1] * H, b[2] * W, b[3] * H]            # normalised 0-1
        elif mx > max(W, H) * 1.05 and mx <= 1000: b = [b[0] * W / 1000, b[1] * H / 1000, b[2] * W / 1000, b[3] * H / 1000]
        x1, y1, x2, y2 = min(b[0], b[2]), min(b[1], b[3]), max(b[0], b[2]), max(b[1], b[3])
        boxes.append({'box': [max(0, x1), max(0, y1), min(W, x2), min(H, y2)],
                      'label': str(it.get('label', ''))[:60] if isinstance(it, dict) else ''})
    return boxes


def pick_images():
    sel = []
    specA = ROOT / 'data' / 'citrusA_mendeley_4cls.json'
    spec = json.loads(specA.read_text(encoding='utf-8'))
    leaves = C.resolve_data_path(spec['classes']['Black Spot'][0]).parent
    for c in CASES:
        p = leaves / c
        if p.exists():
            sel.append(('A-case', c.split('/')[0], p)); shutil.copy2(p, OUT / 'case' / p.name)
    rng = random.Random(7)
    for cls, dirs in spec['classes'].items():
        fs = sorted(f for f in C.resolve_data_path(dirs[0]).glob('*') if f.suffix.lower() in ('.png', '.jpg', '.jpeg'))
        for f in rng.sample(fs, min(4, len(fs))): sel.append(('A', cls, f))
    specB = ROOT / 'data' / 'citrus_zenodo.json'
    if specB.exists():
        sb = json.loads(specB.read_text(encoding='utf-8'))
        for cls in ('Greening', 'Greasy Spot', 'Leaf Miner', 'Healthy'):
            if cls in sb['classes']:
                fs = sorted(C.resolve_data_path(sb['classes'][cls][0]).glob('*.jpg'))
                for f in rng.sample(fs, min(2, len(fs))): sel.append(('B', cls, f))
    return sel


def main():
    (ROOT / 'logs').mkdir(exist_ok=True)
    sel = pick_images(); log(f'{len(sel)} images')
    res = []
    for i, (ds, cls, p) in enumerate(sel):
        im = resize28(Image.open(p)); W, H = im.size
        iid = f'{i:02d}_{ds}_{cls.replace(" ", "")}'
        ip = OUT / 'inputs' / f'{iid}.png'; im.save(ip)
        rec = {'id': iid, 'dataset': ds, 'gt': cls, 'source': p.name, 'W': W, 'H': H, 'models': {}}
        for m in MODELS:
            try:
                txt, dt = ask(m, ip, W, H)
            except Exception as ex:
                txt, dt = f'ERROR {ex}', 0
            boxes = parse_boxes(txt, W, H)
            rec['models'][m] = {'boxes': boxes, 'raw': txt[:1500], 'sec': round(dt, 1)}
            log(f'{iid:<28} {m:<13} {dt:5.1f}s  boxes={None if boxes is None else len(boxes)}')
        res.append(rec)
        (OUT / 'localize.json').write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding='utf-8')
    log('DONE')


if __name__ == '__main__':
    main()
