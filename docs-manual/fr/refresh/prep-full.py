#!/usr/bin/env python3
"""Full-page translation batches for a new language (no earlier translation to reuse).

usage: python3 prep-full.py ROOT LIVE_JSON EN_ID [EN_ID ...]
ROOT holds src/<en>.json (fr-fetch.py), en.json (English UI strings) and LIVE_JSON (for example
id-live.json from tx-push.py --lang=id --live-json). Writes ROOT/work/sk-<en>.json (reuse empty, so
merge.py works unchanged), ROOT/work/batchNN.json (about 12k characters each) and ROOT/report.json.
The French refresh keeps using prep.py; this script never reads or writes French files."""
import json, os, re, sys, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from adfseg import extract
R, LIVE = sys.argv[1], sys.argv[2]; ids = sys.argv[3:]
os.makedirs(os.path.join(R, 'work'), exist_ok=True)
J = lambda *p: json.load(open(os.path.join(R, *p)))
en, live = J('en.json'), J(LIVE)
by_en = collections.defaultdict(collections.Counter)
same = set()
for k, v in en.items():
    f = live.get(k)
    if not (isinstance(v, str) and isinstance(f, str) and f.strip()): continue
    if f != v: by_en[v.strip()][f] += 1
    else: same.add(v.strip())
def ui_map(segs):
    m = {}
    for s in segs:
        for lab in re.findall(r'<b>(.*?)</b>', s['text']):
            for part in re.split(r'\s*(?:→|&gt;)\s*', re.sub(r'<[^>]+>', '', lab)):
                p = part.strip().rstrip(':').strip()
                if not p: continue
                if p in by_en: m[p] = [x for x, _ in by_en[p].most_common(3)]
                elif p in same: m[p] = ['(same as English in the UI: keep "%s")' % p]
    return m
batch, report = [], {}
for pid in ids:
    new = J('src', pid + '.json')
    sk, segs = extract(new['adf'])
    json.dump(dict(skeleton=sk, segs=segs, reuse={}, newTitle=new['title'], oldFrTitle=None, version=new['version']),
              open(os.path.join(R, 'work', 'sk-%s.json' % pid), 'w'), ensure_ascii=False)
    batch.append(dict(page=pid, title=new['title'], segs=segs, context={}, ui=ui_map(segs)))
    report[pid] = dict(title=new['title'], segments=len(segs), chars=sum(len(s['text']) for s in segs), version=new['version'])
json.dump(report, open(os.path.join(R, 'report.json'), 'w'), ensure_ascii=False, indent=1)
bs, cur, n = [], [], 0
for p in sorted(batch, key=lambda p: -sum(len(s['text']) for s in p['segs'])):
    c = sum(len(s['text']) for s in p['segs'])
    if cur and n + c > 12000: bs.append(cur); cur, n = [], 0
    cur.append(p); n += c
if cur: bs.append(cur)
for i, b in enumerate(bs): json.dump(b, open(os.path.join(R, 'work', 'batch%02d.json' % i), 'w'), ensure_ascii=False, indent=1)
print(sum(r['chars'] for r in report.values()), 'characters,', len(bs), 'batches in', os.path.join(R, 'work'))
