"""Inventory: every English page in scope + its French twin (via Lango property). Writes fr/inventory.json"""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from frlib import *
roots = {'eum':'1329758211','admin':'257458193','about':'239337475','install':'239632402','modules':'1325727762','impl':'1160511506','home':'52560162','fr':'1641447437','legacy':'1657864193'}
pages = {}
for k, r in roots.items():
    for p in cql('ancestor=%s and type=page' % r, expand='version,ancestors,metadata.labels'):
        pages.setdefault(p['id'], dict(id=p['id'], title=p['title'], ver=p['version']['number'], when=p['version']['when'][:10],
            by=p['version'].get('by',{}).get('displayName'), roots=[], anc=' > '.join(a['title'][:28] for a in p['ancestors'][-3:]),
            labels=[l['name'] for l in p['metadata']['labels']['results']]))['roots'].append(k)
    try:
        p = get('/rest/api/content/%s?expand=version,ancestors,metadata.labels' % r)
        pages.setdefault(p['id'], dict(id=p['id'], title=p['title'], ver=p['version']['number'], when=p['version']['when'][:10], by=None, roots=[k+'-root'], anc=' > '.join(a['title'][:28] for a in p['ancestors'][-3:]), labels=[l['name'] for l in p['metadata']['labels']['results']]))
    except Exception as e: pass
# Lango-created pages anywhere in OG
for p in cql('space=OG and type=page and creator="5ec313eb1114700c34e02f1a"', expand='version,ancestors,metadata.labels'):
    pages.setdefault(p['id'], dict(id=p['id'], title=p['title'], ver=p['version']['number'], when=p['version']['when'][:10], by=None, roots=['lango'], anc=' > '.join(a['title'][:28] for a in p['ancestors'][-3:]), labels=[l['name'] for l in p['metadata']['labels']['results']]))
for pid, d in pages.items():
    pr = lango(pid)
    if pr: d['lango'] = dict(lang=pr['value']['lang']['code'], status=pr['value'].get('langStatus'), orig=pr['value'].get('originalContentId'), pv=pr['version']['number'], pwhen=pr['version']['when'][:19])
json.dump(pages, open(os.path.join(HERE,'inventory.json'),'w'), ensure_ascii=False, indent=1)
print(len(pages), 'pages')
