import sys,os,json
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from frlib import *
out={}
for i in sys.argv[1:]:
    for k in ('pages','folders'):
        try: n=get('/api/v2/%s/%s'%(k,i)); out[i]=(k,n['title'],n.get('parentId')); break
        except RuntimeError: pass
json.dump(out,open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'ids.json'),'w'),ensure_ascii=False,indent=1)
