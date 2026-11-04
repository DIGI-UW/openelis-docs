"""Fetch English source pages (ADF + version + attachments) listed in fr/scope.json into fr/src/."""
import json, os, sys, tarfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from frlib import *
scope = json.load(open(lp('scope')))
os.makedirs(os.path.join(HERE,'src'), exist_ok=True)
ids = sys.argv[1:] or [s['en'] for s in scope]
for pid in ids:
    p = page(pid)
    att=[]; u='/api/v2/pages/%s/attachments?limit=100' % pid
    while u:
        d=get(u); att+=[dict(id=a['id'],title=a['title'],fileId=a.get('fileId'),mediaType=a.get('mediaType'),size=a.get('fileSize'),dl=a.get('downloadLink')) for a in d['results']]
        u=d.get('_links',{}).get('next')
    rec=dict(id=pid,title=p['title'],version=p['version']['number'],when=p['version']['createdAt'],parentId=p.get('parentId'),parentType=p.get('parentType'),
             adf=json.loads(p['body']['atlas_doc_format']['value']),attachments=att)
    json.dump(rec, open(os.path.join(HERE,'src',pid+'.json'),'w'), ensure_ascii=False)
    print(pid, rec['version'], len(att), rec['title'][:50], flush=True)
with tarfile.open(os.path.join(HERE,'src.tgz'),'w:gz') as t: t.add(os.path.join(HERE,'src'), arcname='src')
print('DONE')
