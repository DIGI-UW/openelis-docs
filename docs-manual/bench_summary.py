#!/usr/bin/env python3
"""Turn drift-report.json into bench-drift.json: the compact summary the Documentation
triage bench reads (drop it on the bench's "Load drift report" button, or ask Claude to
sync the bench). Also prunes report rows that no contract backs any more."""
import json, os, sys, collections, datetime
from urllib.parse import urlparse
HERE = os.path.dirname(os.path.abspath(__file__))
C = json.load(open(os.path.join(HERE, 'contracts.json')))['sections']
RP = os.path.join(HERE, 'drift-report.json')
R = json.load(open(RP))
host = lambda u: urlparse(u or '').netloc or (u or '')
live = {s['id']: s for s in C if not s.get('retired')}
rows = [r for r in R.get('sections', []) if r['id'] in live and host(r.get('base')) == host(live[r['id']].get('base'))]
if len(rows) != len(R.get('sections', [])):
    R['sections'] = rows; json.dump(R, open(RP, 'w'), indent=2)
by = {r['id']: r for r in rows}
inst = collections.OrderedDict()
for h in sorted({host(s['base']) for s in live.values()}):
    rs = [r for r in rows if host(r['base']) == h]
    cnt = collections.Counter(r['status'] for r in rs)
    inst[h] = dict(contracts=sum(1 for s in live.values() if host(s['base']) == h), checked=len(rs),
                   ok=cnt['ok'], review=cnt['review'], drift=cnt['drift'], error=cnt['error'],
                   version=(rs[0].get('instanceVersion') if rs else None),
                   checkedAt=(max(r.get('checkedAt', '') for r in rs) if rs else None))
tot = collections.Counter(r['status'] for r in rows)
out = dict(
    generatedAt=datetime.datetime.utcnow().isoformat(timespec='seconds') + 'Z',
    reportAt=R.get('generatedAt'),
    sections=len(rows), contracts=len(live), ok=tot['ok'], review=tot['review'], errors=tot['error'],
    stale=sorted(i for i, s in live.items() if s.get('capturedVersion') and s.get('capturedVersion') != (by.get(i) or {}).get('instanceVersion', s.get('capturedVersion'))),
    capturedOld=sum(1 for s in live.values() if s.get('capturedVersion') != '3.2.2.0'),
    unchecked=sorted(i for i in live if i not in by),
    instances=inst,
    drift=[dict(id=r['id'], base=host(r['base']), missing=r.get('missingAnchors', []), page=live[r['id']].get('confluencePageId')) for r in rows if r['status'] == 'drift'],
    errorRoutes=[dict(id=r['id'], base=host(r['base']), routes=r.get('routeErrors', []), page=live[r['id']].get('confluencePageId')) for r in rows if r['status'] == 'error'],
)
out['summary'] = '%d of %d contracts checked: %d ok, %d review, %d drift, %d route errors%s.' % (
    len(rows), len(live), tot['ok'], tot['review'], tot['drift'], tot['error'],
    (', not checked: ' + ', '.join(out['unchecked'])) if out['unchecked'] else '')
dst = os.path.join(HERE, 'bench-drift.json')
json.dump(out, open(dst, 'w'), indent=2)
print(out['summary']); print('wrote', dst)
