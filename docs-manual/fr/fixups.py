"""One-off fixes after the 2026-10-09 French pass."""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from frlib import *
# 1. French landing: drop the self-referencing "Lire en français" bullet
pid = '1641447437'
p = page(pid); adf = json.loads(p['body']['atlas_doc_format']['value'])
def txt(n): return ''.join(x.get('text', '') for x in json.dumps(n) and [n] for x in walk(n))
def walk(n):
    yield n
    for c in n.get('content', []) or []: yield from walk(c)
removed = 0
for n in walk(adf):
    if n.get('type') in ('bulletList', 'orderedList'):
        keep = [li for li in n['content'] if not ''.join(x.get('text', '') for x in walk(li)).strip().startswith('Lire en français')]
        removed += len(n['content']) - len(keep); n['content'] = keep
if removed:
    req('PUT', '/api/v2/pages/%s' % pid, {'id': pid, 'status': 'current', 'title': p['title'],
        'body': {'representation': 'atlas_doc_format', 'value': json.dumps(adf, ensure_ascii=False)},
        'version': {'number': p['version']['number'] + 1, 'message': 'Retrait du lien vers la page elle-même'}})
print('landing bullets removed', removed)
# 2. French home page title
st = json.load(open(os.path.join(HERE, 'state.json')))
hid = st['fr']['52560162']; h = page(hid)
if h['title'] != 'Accueil OpenELIS Global (français)':
    req('PUT', '/api/v2/pages/%s' % hid, {'id': hid, 'status': 'current', 'title': 'Accueil OpenELIS Global (français)',
        'body': {'representation': 'atlas_doc_format', 'value': h['body']['atlas_doc_format']['value']},
        'version': {'number': h['version']['number'] + 1, 'message': 'Titre'}})
print('home', hid)
