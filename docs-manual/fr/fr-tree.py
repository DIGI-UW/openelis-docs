#!/usr/bin/env python3
"""French tree mirror check and fix (docs spine).
usage: fr-tree.py [--apply]
Builds the English->French map (pages from bench-translations.json, folders from state.json['folders'];
state.json['parentOnly'] maps English parents with no French twin, such as archives, to a French target),
then for every French twin compares its parent with the twin of its English parent.
Writes fr/tree-plan.json (moves, unmapped English parents). With --apply, moves misplaced French pages
(children travel with them) and records a log in state.json['log']."""
import json, os, sys, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from frlib import *
D = os.path.dirname(os.path.abspath(__file__))
st = json.load(open(lp('state')))
BP = os.path.join(D, '..', L['bench'])
# first run for a new language: no bench file yet, so use the twins recorded in the state file
b = json.load(open(BP)) if os.path.exists(BP) else {'rows': [{'en': k, 'tr': v} for k, v in st.get(TW, {}).items()]}
ROOTS = {'EUM': '1329758211', 'ADM': '257458193'}
m = {}
for k, v in st['folders'].items(): m[ROOTS.get(k, k)] = v
for r in b['rows']: m[r['en']] = r.get('tr') or r['fr']
pairs = dict(m)
for k, v in st.get('parentOnly', {}).items(): m.setdefault(k, v)  # used as move targets only, never checked
def node(i):
    for kind in ('pages', 'folders'):
        try: return dict(get('/api/v2/%s/%s' % (kind, i)), kind=kind[:-1])
        except RuntimeError as e:
            if '-> 404' not in str(e): raise
    return None
plan = dict(generatedAt=datetime.datetime.utcnow().isoformat(timespec='seconds') + 'Z', moves=[], unmapped={}, ok=0)
cache = {}
for en, fr in list(pairs.items()):
    e = cache.get(en) or node(en); f = node(fr)
    if not e or not f: continue
    ep, fp = e.get('parentId'), f.get('parentId')
    exp = m.get(ep)
    if exp is None:
        if ep: plan['unmapped'].setdefault(ep, []).append(dict(en=en, title=e['title'], frParent=fp))
        continue
    if exp == fp: plan['ok'] += 1
    else: plan['moves'].append(dict(en=en, fr=fr, kind=f['kind'], title=f['title'], enTitle=e['title'], from_=fp, to=exp))
# describe unmapped parents
for ep in plan['unmapped']:
    n = node(ep); plan['unmapped'][ep] = dict(title=n and n['title'], kind=n and n['kind'], children=plan['unmapped'][ep])
json.dump(plan, open(lp('treePlan'), 'w'), ensure_ascii=False, indent=1)
print('ok', plan['ok'], 'moves', len(plan['moves']), 'unmapped parents', len(plan['unmapped']))
if '--apply' in sys.argv:
    for mv in plan['moves']:
        try:
            req('PUT', '/rest/api/content/%s/move/append/%s' % (mv['fr'], mv['to']))
            mv['result'] = 'moved'
        except RuntimeError as x: mv['result'] = str(x)[:200]
        st['log'].append(dict(at=datetime.datetime.utcnow().isoformat(timespec='seconds'), op='tree-move', fr=mv['fr'], frm=mv['from_'], to=mv['to'], result=mv['result']))
        print(mv['fr'], mv['title'][:50], mv['result'][:80])
    json.dump(st, open(lp('state'), 'w'), ensure_ascii=False, indent=1)
    json.dump(plan, open(lp('treePlan'), 'w'), ensure_ascii=False, indent=1)
