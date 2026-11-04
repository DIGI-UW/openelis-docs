"""Match published English figures to the capture that produced them, then cut the same region
from the French capture.

usage: figmatch.py <en_figs_dir> <en_capture_dir> <fr_capture_dir> <out_dir> [--report r.json]

For each image in en_figs_dir:
  1. find the English capture in en_capture_dir (recursive) it came from: identical bytes, same pixels,
     or the published figure is a crop (possibly downscaled) of the capture (template matching);
  2. take the French capture at the same relative path in fr_capture_dir and apply the same crop/scale;
  3. write it to out_dir/<published file name>.
Figures with no confident match are listed in the report and left alone (the English figure stays).
"""
import cv2, numpy as np, os, sys, json, hashlib

def load(p):
    im = cv2.imread(p, cv2.IMREAD_COLOR)
    return im

def md5(p):
    return hashlib.md5(open(p, 'rb').read()).hexdigest()

def walk(d):
    out = []
    for r, ds, fs in os.walk(d):
        for f in fs:
            if f.lower().endswith('.png'): out.append(os.path.join(r, f))
    return out

def match(fig, cap):
    """return (score, x, y, scale) of fig inside cap (cap pixels), or None"""
    fh, fw = fig.shape[:2]; ch, cw = cap.shape[:2]
    best = None
    # published figures are either captures at the same scale or downscaled; try scales so fig fits cap
    for s in [1.0, 2.0, 0.5, 1.5, 4/3, 0.75, 2.5, 3.0]:
        tw, th = int(round(fw * s)), int(round(fh * s))
        if tw > cw or th > ch or tw < 40 or th < 40: continue
        t = cv2.resize(fig, (tw, th), interpolation=cv2.INTER_AREA if s < 1 else cv2.INTER_CUBIC)
        # speed: match on downsampled grayscale first
        k = max(1, int(min(cw, ch) / 700))
        cg = cv2.cvtColor(cap, cv2.COLOR_BGR2GRAY)[::k, ::k]; tg = cv2.cvtColor(t, cv2.COLOR_BGR2GRAY)[::k, ::k]
        if tg.shape[0] > cg.shape[0] or tg.shape[1] > cg.shape[1]: continue
        r = cv2.matchTemplate(cg, tg, cv2.TM_CCOEFF_NORMED)
        _, mx, _, loc = cv2.minMaxLoc(r)
        if best is None or mx > best[0]: best = (mx, loc[0] * k, loc[1] * k, s, tw, th)
    return best

def main():
    a = sys.argv[1:]
    figs_dir, en_dir, fr_dir, out_dir = a[:4]
    rep_path = a[a.index('--report') + 1] if '--report' in a else None
    os.makedirs(out_dir, exist_ok=True)
    caps = walk(en_dir)
    capmd5 = {}
    for c in caps: capmd5.setdefault(md5(c), c)
    capims = {}
    report = []
    for f in sorted(os.listdir(figs_dir)):
        fp = os.path.join(figs_dir, f)
        if not f.lower().endswith(('.png', '.jpg', '.jpeg')): continue
        fig = load(fp)
        if fig is None: continue
        hit = capmd5.get(md5(fp)); how = 'bytes'; box = None
        if not hit:
            # full-frame match: the figure is the whole capture, possibly downscaled (fast, thumbnail correlation)
            fh, fw = fig.shape[:2]; ft = cv2.cvtColor(cv2.resize(fig, (240, max(1, int(240 * fh / fw))), interpolation=cv2.INTER_AREA), cv2.COLOR_BGR2GRAY).astype(np.float32)
            bestf = None
            for c in caps:
                if c not in capims: capims[c] = load(c)
                ci = capims[c]
                if ci is None: continue
                ch, cw = ci.shape[:2]
                if abs(ch / cw - fh / fw) > 0.01: continue
                ct = cv2.cvtColor(cv2.resize(ci, (ft.shape[1], ft.shape[0]), interpolation=cv2.INTER_AREA), cv2.COLOR_BGR2GRAY).astype(np.float32)
                a1 = ft - ft.mean(); b1 = ct - ct.mean()
                corr = float((a1 * b1).sum() / (np.sqrt((a1 * a1).sum() * (b1 * b1).sum()) + 1e-6))
                if bestf is None or corr > bestf[0]: bestf = (corr, c)
            if bestf and bestf[0] >= 0.9995:  # lower scores are usually the same capture with hand-drawn annotations: keep English
                hit = bestf[1]; how = 'frame %.3f' % bestf[0]
                ch, cw = capims[hit].shape[:2]; box = (0, 0, cw, ch, cw / fw)
        if not hit and '--crop' in a:
            # same name first, then everything
            cands = sorted(caps, key=lambda c: (os.path.basename(c) != f, c))
            best = None
            for c in cands:
                if c not in capims: capims[c] = load(c)
                ci = capims[c]
                if ci is None: continue
                m = match(fig, ci)
                if m and (best is None or m[0] > best[0][0]): best = (m, c)
                if best and best[0][0] > 0.985: break
            if best and best[0][0] >= 0.93:
                (score, x, y, s, tw, th), hit = best; how = 'crop %.3f' % score; box = (x, y, tw, th, s)
        rel = os.path.relpath(hit, en_dir) if hit else None
        frp = os.path.join(fr_dir, rel) if rel else None
        rec = {'figure': f, 'capture': rel, 'how': how if hit else 'no match'}
        if hit and frp and os.path.exists(frp):
            fr = load(frp)
            if box:
                x, y, tw, th, s = box
                H, W = fr.shape[:2]
                crop = fr[y:min(H, y + th), x:min(W, x + tw)]
                if crop.shape[:2] != fig.shape[:2]: crop = cv2.resize(crop, (fig.shape[1], fig.shape[0]), interpolation=cv2.INTER_AREA if crop.shape[1] > fig.shape[1] else cv2.INTER_CUBIC)
                fr = crop
            cv2.imwrite(os.path.join(out_dir, f), fr)
            rec['french'] = True
        else:
            rec['french'] = False
            if hit: rec['note'] = 'French capture missing'
        report.append(rec); print(json.dumps(rec), flush=True)
    if rep_path: json.dump(report, open(rep_path, 'w'), indent=1)

if __name__ == '__main__':
    main()
