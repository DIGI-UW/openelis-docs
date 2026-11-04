import json,sys,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from frlib import *
b=json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','bench-translations.json')))
rows=b['rows']; en2fr={r['en']:r['fr'] for r in rows}
out=dict(tot=0,mis=0,ex=[],stale=[(r['enTitle'],r['en'],r['fr'],r.get('contract')) for r in b['staleRows']])
for r in rows:
    try: e=get('/api/v2/pages/%s'%r['en']);f=get('/api/v2/pages/%s'%r['fr'])
    except Exception: continue
    out['tot']+=1
    if en2fr.get(e.get('parentId'))!=f.get('parentId'):
        out['mis']+=1; out['ex'].append((r['enTitle'],e.get('parentId'),f.get('parentId'),en2fr.get(e.get('parentId'))))
f=rows[0]['fr']
out['labels']=[l['name'] for l in get('/rest/api/content/%s/label'%f)['results']]
try: out['prop']=get('/rest/api/content/%s/property/openelis-translation'%f)['value']
except Exception as x: out['prop']=str(x)
out['body']=get('/api/v2/pages/%s?body-format=storage'%f)['body']['storage']['value'][:900]
json.dump(out,open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'mirror-check.json'),'w'),ensure_ascii=False,indent=1)
