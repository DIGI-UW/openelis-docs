#!/usr/bin/env python3
"""Merge translated segments into publishable French pages.
usage: python3 merge.py ROOT EN_ID [EN_ID ...]
Reads ROOT/work/sk-<en>.json (from prep.py), ROOT/out/<en>.json (translators: {page, title, segs}) and
ROOT/plan.json (fr/build/plan.json). Writes ROOT/publish/<en>.json ({en, title, adf}) and ROOT/publish/plan.json
with enVersion, title and enTitle updated. Copy publish/* to docs-manual/fr/build/ on the Mac, then run
fr-publish.py content --only <ids>."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from adfseg import rebuild
R = sys.argv[1]; ids = sys.argv[2:]
os.makedirs(os.path.join(R, 'publish'), exist_ok=True)
plan = json.load(open(os.path.join(R, 'plan.json'))); by = {p['en']: p for p in plan['pages']}
for pid in ids:
    sk = json.load(open(os.path.join(R, 'work', 'sk-%s.json' % pid))); o = json.load(open(os.path.join(R, 'out', '%s.json' % pid)))
    tr = dict(sk['reuse']); tr.update(o['segs'])
    adf, miss = rebuild(sk['skeleton'], tr)
    if miss: sys.exit('%s: missing segments %s' % (pid, miss[:5]))
    s = json.dumps(adf, ensure_ascii=False)
    if '—' in ''.join(o['segs'].values()): print('WARN', pid, 'em dash in new French')
    json.dump(dict(en=pid, title=o['title'], adf=adf), open(os.path.join(R, 'publish', pid + '.json'), 'w'), ensure_ascii=False)
    p = by.get(pid)
    if p is None: sys.exit('%s not in plan.json: add it first (see the skill)' % pid)
    p['enVersion'] = sk['version']; p['title'] = o['title']; p['enTitle'] = sk['newTitle']
    print(pid, 'v%s' % sk['version'], o['title'][:60])
json.dump(plan, open(os.path.join(R, 'publish', 'plan.json'), 'w'), ensure_ascii=False, indent=1)
