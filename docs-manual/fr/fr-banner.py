#!/usr/bin/env python3
"""Tell French readers when the English page has changed since the translation (docs spine).
usage: fr-banner.py [--apply]   (default: dry run)
Reads ../bench-translations.json (run translation-freshness.py first). For each stale French page, the
translation notice at the top turns from a blue note into a yellow warning with one extra sentence naming
the newer English version. fr-publish.py writes the normal blue notice again when the page is retranslated;
this script also restores it if a page is current again."""
import json, os, sys, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from frlib import *
D = os.path.dirname(os.path.abspath(__file__))
APPLY = '--apply' in sys.argv
MARK = L['bannerMark']
b = json.load(open(os.path.join(D, '..', L['bench'])))
def is_notice(n):
    if not (isinstance(n, dict) and n.get('type') == 'panel'): return False
    return L['noticeMarker'] in json.dumps(n, ensure_ascii=False)
done = []
for r in b['rows']:
    if r['status'] not in ('stale', 'current'): continue
    tid = r.get('tr') or r['fr']
    pg = get('/api/v2/pages/%s?body-format=atlas_doc_format' % tid)
    adf = json.loads(pg['body']['atlas_doc_format']['value'])
    if not adf.get('content') or not is_notice(adf['content'][0]): 
        if r['status'] == 'stale': done.append((tid, 'no notice panel found, skipped')); 
        continue
    panel = adf['content'][0]
    flagged = MARK in json.dumps(panel, ensure_ascii=False)
    if r['status'] == 'stale' and not flagged:
        when = (r.get('changes') or [{}])[-1].get('when', '')
        panel['attrs']['panelType'] = 'warning'
        panel['content'].append({'type': 'paragraph', 'content': [{'type': 'text', 'text':
            L['bannerText'].format(mark=MARK, v=r['enVersion'], d=when)}]})
        msg, act = L['bannerFlagMsg'], 'flagged'
    elif r['status'] == 'current' and flagged:
        panel['attrs']['panelType'] = 'note'
        panel['content'] = [c for c in panel['content'] if MARK not in json.dumps(c, ensure_ascii=False)]
        msg, act = L['bannerRestoreMsg'], 'restored'
    else: continue
    if APPLY:
        req('PUT', '/api/v2/pages/%s' % tid, {'id': tid, 'status': 'current', 'title': pg['title'],
            'body': {'representation': 'atlas_doc_format', 'value': json.dumps(adf, ensure_ascii=False)},
            'version': {'number': pg['version']['number'] + 1, 'message': msg, 'minorEdit': True}})
    done.append((tid, act + ('' if APPLY else ' (dry run)')))
for x in done: print(*x)
print(len(done), 'pages', 'changed' if APPLY else 'would change')
