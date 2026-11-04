"""Extra checks for translation-freshness.py (docs spine): English drift gate, what changed in the English,
French tree mirror, and UI labels quoted on French pages. Runs on Casey's Mac (needs frlib credentials)."""
import json, os, re, glob, unicodedata, subprocess, sys
from frlib import *
D = os.path.dirname(os.path.abspath(__file__)); DM = os.path.dirname(D)

# ---- 1. English drift gate -------------------------------------------------------------------
def drift_status():
    try: rep = json.load(open(os.path.join(DM, 'drift-report.json')))
    except FileNotFoundError: return {}, None
    return {s['id']: s.get('status') for s in rep['sections']}, rep.get('generatedAt')

# ---- 2. What changed in the English since the translated version ----------------------------
def _blocks(adf):
    """(kind, text) per top-level-ish block: headings, paragraphs, list items, table cells, media."""
    out = []
    def txt(n):
        if isinstance(n, dict):
            if n.get('type') == 'text': return n.get('text', '')
            return ''.join(txt(c) for c in n.get('content', []))
        return ''
    def walk(n, heading):
        if not isinstance(n, dict): return heading
        t = n.get('type')
        if t == 'heading':
            heading = txt(n).strip(); out.append(('heading', heading, heading)); return heading
        if t in ('paragraph', 'codeBlock'):
            s = ' '.join(txt(n).split())
            if s: out.append(('text', s, heading))
            return heading
        if t in ('mediaSingle', 'mediaGroup', 'media'):
            for c in n.get('content', []) or [n]:
                a = c.get('attrs', {}) if isinstance(c, dict) else {}
                out.append(('media', a.get('id') or a.get('alt') or '', heading))
            return heading
        for c in n.get('content', []) or []: heading = walk(c, heading)
        return heading
    h = ''
    for c in adf.get('content', []): h = walk(c, h)
    return out

def english_change(en, sv, cur):
    """kind: text (retranslate the listed sections), figures (copy figures only), none (format/metadata only)."""
    try:
        a = json.loads(get('/api/v2/pages/%s?version=%s&body-format=atlas_doc_format' % (en, sv))['body']['atlas_doc_format']['value'])
        b = json.loads(get('/api/v2/pages/%s?body-format=atlas_doc_format' % en)['body']['atlas_doc_format']['value'])
    except (RuntimeError, KeyError, TypeError) as e:
        return dict(kind='unknown', error=str(e)[:150])
    A, B = _blocks(a), _blocks(b)
    ta = {(k, s) for k, s, _ in A if k != 'media'}; tb = {(k, s) for k, s, _ in B if k != 'media'}
    ma = [s for k, s, _ in A if k == 'media']; mb = [s for k, s, _ in B if k == 'media']
    changed = [(k, s, h) for k, s, h in B if k != 'media' and (k, s) not in ta]
    removed = [(k, s, h) for k, s, h in A if k != 'media' and (k, s) not in tb]
    sections = sorted({h or '(top)' for _, _, h in changed + removed})
    kind = 'text' if (changed or removed) else ('figures' if ma != mb else 'none')
    return dict(kind=kind, sections=sections, addedOrChanged=len(changed), removed=len(removed),
                figuresChanged=ma != mb)

# ---- 3. French tree mirror ------------------------------------------------------------------
def tree_check():
    """Runs fr-tree.py (dry) and returns its plan: misplaced French pages and English parents with no twin."""
    subprocess.run([sys.executable, os.path.join(D, 'fr-tree.py')], check=False, capture_output=True)
    p = json.load(open(lp('treePlan')))
    return dict(checkedAt=p['generatedAt'], inPlace=p['ok'], misplaced=p['moves'], unmappedParents=p['unmapped'])

# ---- 4. UI labels quoted on French pages ----------------------------------------------------
PROSE = set(L['prose'])   # page furniture words in bold that are not UI labels (per language, langs.json)
def _norm(s):
    s = unicodedata.normalize('NFC', s).replace('’', "'").replace('\xa0', ' ')
    s = re.sub(r'\s+', ' ', s).strip().strip('«»"').strip().rstrip(':…').rstrip('.').strip()
    return s.casefold()

def refresh_fr_live():
    """Download the live French UI strings from Transifex (dry run of tx-push, nothing is written there)."""
    r = subprocess.run([sys.executable, os.path.join(D, 'tx', 'tx-push.py')] + L['liveArgs'], cwd=os.path.join(D, 'tx'), capture_output=True, text=True)
    return r.returncode == 0

def label_check(rows):
    """Bold strings on French pages that look like UI labels and are not (or no longer) French UI strings."""
    try: live = json.load(open(os.path.join(D, 'tx', L['live'])))
    except FileNotFoundError: return None
    # pending Transifex fixes the docs already quote (langs.json "overlay": a tx-push decisions file)
    for f in ([L['overlay']] if L.get('overlay') else []):
        for d in json.load(open(os.path.join(D, 'tx', f))):
            if d.get('status') == 'approved' and d.get('key'): live[d['key']] = d['value']
    vals = set()
    for v in live.values():
        for s in (v.values() if isinstance(v, dict) else [v]):
            if isinstance(s, str): vals.add(_norm(s))
    base_p = lp('baseline')
    base = json.load(open(base_p)) if os.path.exists(base_p) else None
    out, newbase = [], {}
    for r in rows:
        try: adf = json.loads(get('/api/v2/pages/%s?body-format=atlas_doc_format' % r['tr'])['body']['atlas_doc_format']['value'])
        except (RuntimeError, KeyError, TypeError): continue
        strong = []
        def walk(n):
            if isinstance(n, dict):
                if n.get('type') == 'text' and any(m['type'] == 'strong' for m in n.get('marks', [])): strong.append(n['text'])
                for c in n.get('content', []) or []: walk(c)
        walk(adf)
        miss = set()
        for s in strong:
            for part in re.split(r'\s*[→>]\s*', s):
                n = _norm(part)
                if 1 < len(n) <= 60 and n not in PROSE and n not in vals and not re.fullmatch(r'[\d\W]+', n): miss.add(part.strip())
        newbase[r['tr']] = sorted(miss)
        new = sorted(miss - set((base or {}).get(r['tr'], []))) if base is not None else []
        if miss: out.append(dict(fr=r['tr'], frTitle=r['trTitle'], tr=r['tr'], trTitle=r['trTitle'], notInUi=sorted(miss), newSinceBaseline=new))
    if base is None: json.dump(newbase, open(base_p, 'w'), ensure_ascii=False, indent=1)
    return dict(pagesWithUnknownLabels=len(out), pagesWithNewUnknownLabels=sum(1 for x in out if x['newSinceBaseline']),
                baselineCreated=base is None, rows=out)
