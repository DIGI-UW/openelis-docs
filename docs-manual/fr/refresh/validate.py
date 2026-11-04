"""Validate translated page files: python3 validate.py ROOT/work/batchNN.json  (checks ROOT/out/<page>.json for each page)"""
import json, sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from adfseg import check
HERE = os.path.dirname(os.path.abspath(__file__))
batch = json.load(open(sys.argv[1]))
bad = 0
for p in batch:
    fn = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[1]))), 'out', p['page'] + '.json')
    if not os.path.exists(fn):
        print('MISSING FILE', p['page']); bad += 1; continue
    try:
        d = json.load(open(fn))
    except Exception as e:
        print('BAD JSON', p['page'], e); bad += 1; continue
    tr = d.get('segs', {})
    if not d.get('title'): print(p['page'], 'no title'); bad += 1
    for s in p['segs']:
        if s['id'] not in tr:
            print(p['page'], s['id'], 'missing'); bad += 1; continue
        errs = check(s['text'], tr[s['id']])
        if errs:
            print(p['page'], s['id'], '; '.join(errs)); bad += 1
    extra = set(tr) - {s['id'] for s in p['segs']}
    if extra: print(p['page'], 'unknown ids', sorted(extra)[:5]); bad += 1
print('OK' if not bad else '%d problems' % bad)
