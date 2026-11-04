#!/usr/bin/env python3
"""Segment-level refresh of stale French pages: prepare translation batches.

usage: python3 prep.py ROOT EN_ID [EN_ID ...]
ROOT holds (all staged from the Mac, docs-manual/fr):
  old/<en>.json     English page at the version the French was translated from ({"adf": ...}; fr-fetch-old.py)
  src/<en>.json     English page now (fr-fetch.py)
  build/<en>.json   French ADF last published for that page ({"title", "adf"}; fr/build/)
  en.json           English UI strings (tests/docs/i18n/en.json or develop)
  fr-live.json      live French UI strings from Transifex (tx/fr-live.json)
Old English and old French are aligned segment by segment (same skeleton, since the French was rebuilt
from that English). New English segments whose text matches an old one keep its French; the rest go to
work/batchNN.json for translators. If old English and French do not align, the whole page is retranslated.
Writes ROOT/work/sk-<en>.json, ROOT/work/batchNN.json and ROOT/report.json."""
import json, os, re, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from adfseg import extract
R = sys.argv[1]; ids = sys.argv[2:]
os.makedirs(os.path.join(R, 'work'), exist_ok=True)
J = lambda *p: json.load(open(os.path.join(R, *p)))
en, live = J('en.json'), J('fr-live.json')
by_en = collections.defaultdict(collections.Counter)
for k, v in en.items():
    f = live.get(k)
    if isinstance(v, str) and isinstance(f, str) and f.strip() and f != v: by_en[v.strip()][f] += 1
def ui_map(segs):
    m = {}
    for s in segs:
        for lab in re.findall(r'<b>(.*?)</b>', s['text']):
            for part in re.split(r'\s*(?:→|&gt;)\s*', re.sub(r'<[^>]+>', '', lab)):
                p = part.strip().rstrip(':').strip()
                if p and p in by_en: m[p] = [x for x, _ in by_en[p].most_common(3)]
    return m
batch, report = [], {}
for pid in ids:
    old, new, frb = J('old', pid + '.json'), J('src', pid + '.json'), J('build', pid + '.json')
    _, osegs = extract(old['adf']); sk, nsegs = extract(new['adf']); _, fsegs = extract(frb['adf'])
    aligned = len(osegs) == len(fsegs) and all(a['kind'] == b['kind'] for a, b in zip(osegs, fsegs))
    tm = {}
    if aligned:
        for a, b in zip(osegs, fsegs): tm.setdefault((a['kind'], a['text']), b['text'])
    reuse, todo = {}, []
    for s in nsegs:
        hit = tm.get((s['kind'], s['text']))
        if hit is not None: reuse[s['id']] = hit
        else: todo.append(s)
    order = [s['id'] for s in nsegs]; ctx = {}
    for s in todo:
        i = order.index(s['id'])
        prev = next((reuse[order[j]] for j in range(i - 1, -1, -1) if order[j] in reuse), None)
        if prev: ctx[s['id']] = prev[:300]
    title_changed = new['title'] != old.get('title', new['title'])
    json.dump(dict(skeleton=sk, segs=nsegs, reuse=reuse, newTitle=new['title'], oldFrTitle=frb['title'], version=new['version']),
              open(os.path.join(R, 'work', 'sk-%s.json' % pid), 'w'), ensure_ascii=False)
    batch.append(dict(page=pid, title=new['title'], frTitle=frb['title'], titleChanged=title_changed, segs=todo, context=ctx, ui=ui_map(todo)))
    report[pid] = dict(title=new['title'], aligned=aligned, segments=len(nsegs), reused=len(reuse), toTranslate=len(todo),
                       chars=sum(len(s['text']) for s in todo), titleChanged=title_changed)
json.dump(report, open(os.path.join(R, 'report.json'), 'w'), ensure_ascii=False, indent=1)
bs, cur, n = [], [], 0
for p in sorted(batch, key=lambda p: -sum(len(s['text']) for s in p['segs'])):
    c = sum(len(s['text']) for s in p['segs'])
    if cur and n + c > 12000: bs.append(cur); cur, n = [], 0
    cur.append(p); n += c
if cur: bs.append(cur)
for i, b in enumerate(bs): json.dump(b, open(os.path.join(R, 'work', 'batch%02d.json' % i), 'w'), ensure_ascii=False, indent=1)
for k, v in report.items(): print(k, v)
print(len(bs), 'batches in', os.path.join(R, 'work'))
