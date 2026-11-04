#!/usr/bin/env python3
"""Translation freshness check for the OpenELIS Confluence docs (part of the docs spine).

For every French page (label `traduction-fr`, or any page carrying a Lango `fr` property) it finds the
English source and the English version the French was translated from:
  - `openelis-translation` content property (written by fr-publish.py): sourceId + sourceVersion
  - otherwise the Lango property `adapps-lango-lang` (originalContentId) + the English version that was
    current when Lango wrote the French page
It then compares with the English page's current version:
  current   English unchanged since translation
  stale     English edited since translation (lists the English version messages since then)
  orphan    English source deleted or archived
Tracked English pages with no French twin are listed as `missing` (scope: fr/scope.json plus any page
labelled doc-verified under the End User Manual / Administrator Guide).
Each row is joined to contracts.json by confluencePageId, so a stale translation names its drift
contract, Jira Epic and Feature Doc.

Writes docs-manual/bench-translations.json (the triage bench loads it into `translations/latest`).
"""
import json, os, sys, datetime, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from frlib import *
import frchecks

DM = os.path.dirname(HERE)
contracts = {s.get('confluencePageId'): s for s in json.load(open(os.path.join(DM, 'contracts.json')))['sections']
             if s.get('confluencePageId') and not s.get('retired')}
scope = {s['en']: s['scope'] for s in json.load(open(lp('scope')))}

def prop(pid, key):
    try: return get('/rest/api/content/%s/property/%s' % (pid, key))
    except RuntimeError as e:
        if '-> 404' in str(e): return None
        raise

# 1. French pages
cands = {}
for q in ['space=OG and type=page and label="%s"' % L['label'],
          'space=OG and type=page and creator="5ec313eb1114700c34e02f1a"'] + (
         ['space=OG and type=page and ancestor=%s' % L['root']] if L.get('root') else []):
    for p in cql(q, expand='version'):
        cands[p['id']] = p
try:
    for fid in json.load(open(lp('state')))[TW].values():
        if fid not in cands:
            try: cands[fid] = get('/rest/api/content/%s?expand=version' % fid)
            except RuntimeError: pass
except FileNotFoundError: pass
pairs = {}
for pid, p in cands.items():
    ot = prop(pid, 'openelis-translation')
    lg = prop(pid, 'adapps-lango-lang')
    if ot and ot['value'].get('lang', 'fr') != LANG_CODE: continue  # another language's twin
    if ot:
        v = ot['value']; src, sv, how, at = v['sourceId'], v['sourceVersion'], v.get('method', 'claude'), v.get('translatedAt')
        ffig, fat = v.get('frenchFigures') or [], v.get('figuresCapturedAt')
    elif lg and lg['value'].get('lang', {}).get('code') == LANG_CODE and lg['value'].get('originalContentId') not in (None, pid):
        src = lg['value']['originalContentId']; how = 'lango'; at = lg['version']['when'][:10]; ffig, fat = [], None
        sv = None
        try:
            vers = get('/api/v2/pages/%s/versions?limit=250' % src)['results']
            older = [x['number'] for x in vers if x['createdAt'][:19] <= lg['version']['when'][:19]]
            sv = max(older) if older else None
        except RuntimeError: pass
    else:
        continue
    pairs.setdefault(src, []).append(dict(tr=pid, trTitle=p['title'], **({'fr': pid, 'frTitle': p['title']} if LANG_CODE == 'fr' else {}), sourceVersion=sv, method=how, translatedAt=at, frenchFigures=ffig, figuresCapturedAt=fat))

# 2. English side
rows = []
for en, frs in pairs.items():
    try:
        e = get('/api/v2/pages/%s' % en); cur = e['version']['number']; title = e['title']; status = e['status']
    except RuntimeError:
        cur, title, status = None, None, 'deleted'
    for f in frs:
        r = dict(en=en, enTitle=title, enVersion=cur, **f)
        if status != 'current': r['status'] = 'orphan'
        elif f['sourceVersion'] is None: r['status'] = 'unknown'
        elif cur > f['sourceVersion']:
            r['status'] = 'stale'
            try:
                vs = get('/api/v2/pages/%s/versions?limit=250' % en)['results']
                r['changes'] = [dict(v=x['number'], when=x['createdAt'][:10], msg=(x.get('message') or '')[:120]) for x in vs if x['number'] > f['sourceVersion']]
            except RuntimeError: pass
        else: r['status'] = 'current'
        # French screenshots: stale when the English figure was re-uploaded after the French capture
        if f.get('frenchFigures') and f.get('figuresCapturedAt') and status == 'current':
            try:
                ea = get('/api/v2/pages/%s/attachments?limit=100' % en)['results']
                r['figuresStale'] = sorted(a['title'] for a in ea if a['title'] in f['frenchFigures'] and (a.get('createdAt') or '')[:10] > f['figuresCapturedAt'])
            except RuntimeError: pass
        c = contracts.get(en)
        if c: r.update(contract=c['id'], jiraEpic=c.get('jiraEpic'), featureDoc=c.get('featureDoc'))
        r['scope'] = scope.get(en, 'other')
        rows.append(r)
    if len(frs) > 1:
        for r in rows[-len(frs):]: r['duplicate'] = True

# 3. Missing
tracked = set(scope)
for root in ('1329758211', '257458193'):
    for p in cql('ancestor=%s and type=page and label="doc-verified"' % root, expand='version'):
        tracked.add(p['id'])
missing = []
for en in sorted(tracked - set(pairs)):
    try:
        e = get('/api/v2/pages/%s' % en)
        if e['status'] != 'current': continue
        missing.append(dict(en=en, enTitle=e['title'], enVersion=e['version']['number'], scope=scope.get(en, 'manual'),
                            contract=(contracts.get(en) or {}).get('id')))
    except RuntimeError: pass

# 4. Spine extras: English drift gate, what changed in the English, tree mirror, UI labels
dstat, dat = frchecks.drift_status()
for r in rows:
    r['englishDrift'] = dstat.get(r.get('contract'))
    if r['status'] == 'stale':
        r['change'] = frchecks.english_change(r['en'], r['sourceVersion'], r['enVersion'])
        r['action'] = ('wait for English' if r['englishDrift'] in ('drift', 'error') else
                       {'text': 'retranslate changed sections', 'figures': 'copy figures', 'none': 'bump version only'}.get(r['change']['kind'], 'check'))
tree = frchecks.tree_check()
labels = frchecks.label_check(rows) if (frchecks.refresh_fr_live() or True) else None
cnt = collections.Counter(r['status'] for r in rows)
out = dict(generatedAt=datetime.datetime.utcnow().isoformat(timespec='seconds') + 'Z', lang=LANG_CODE,
           pairs=len(rows), current=cnt['current'], stale=cnt['stale'], orphan=cnt['orphan'], unknown=cnt['unknown'],
           missing=len(missing), duplicates=sum(1 for r in rows if r.get('duplicate')),
           staleRows=[r for r in rows if r['status'] == 'stale'],
           orphanRows=[r for r in rows if r['status'] in ('orphan', 'unknown')],
           missingRows=missing, rows=rows)
out['summary'] = ('{0}: %d pairs, %d current, %d stale, %d orphan/unknown, %d tracked pages with no {0}.'.format(L['name'])) % (
    len(rows), cnt['current'], cnt['stale'], cnt['orphan'] + cnt['unknown'], len(missing))
out['frenchFigurePages'] = sum(1 for r in rows if r.get('frenchFigures'))
out['figuresStaleRows'] = [dict(en=r['en'], fr=r['tr'], tr=r['tr'], enTitle=r['enTitle'], figures=r['figuresStale']) for r in rows if r.get('figuresStale')]
out['summary'] += ' %d pages with {0} screenshots, %d with {0} screenshots older than the English.'.format(L['name']) % (out['frenchFigurePages'], len(out['figuresStaleRows']))
out['driftReportAt'] = dat
out['tree'] = tree
out['labels'] = labels
out['actions'] = dict(collections.Counter(r.get('action') for r in rows if r['status'] == 'stale'))
out['summary'] += ' Tree: %d in place, %d misplaced, %d English parents with no {0} twin.'.format(L['name']) % (tree['inPlace'], len(tree['misplaced']), len(tree['unmappedParents']))
if labels: out['summary'] += ' Labels: %d pages quote bold text that is not a {0} UI string (%d new since baseline).'.format(L['name']) % (labels['pagesWithUnknownLabels'], labels['pagesWithNewUnknownLabels'])
json.dump(out, open(os.path.join(DM, L['bench']), 'w'), ensure_ascii=False, indent=1)
print(out['summary']); print('wrote', os.path.join(DM, L['bench']))
