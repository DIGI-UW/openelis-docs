import os, json, base64, urllib.request
env = dict(l.strip().split('=',1) for l in open(os.path.expanduser('~/.openelis/confluence.env')) if '=' in l)
env = {k:v.strip().strip('"').strip("'") for k,v in env.items()}
A = base64.b64encode((env['CONFLUENCE_EMAIL']+':'+env['CONFLUENCE_API_TOKEN']).encode()).decode()
B='https://uwdigi.atlassian.net/wiki'
def call(method,path,data=None):
    req=urllib.request.Request(B+path,data=None if data is None else json.dumps(data).encode(),method=method,
        headers={'Authorization':'Basic '+A,'Content-Type':'application/json','Accept':'application/json'})
    try:
        r=urllib.request.urlopen(req); t=r.read().decode(); return r.status,(json.loads(t) if t else {})
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:400]
MANUEL='1641447437'
s,p=call('GET','/api/v2/pages/%s'%MANUEL); space=p['spaceId']; print('space',space)
# find or create folder
s,kids=call('GET','/api/v2/pages/%s/direct-children?limit=100'%MANUEL)
fid=None
for k in kids.get('results',[]):
    if k.get('type')=='folder' and k['title']=='Versions précédentes': fid=k['id']
if not fid:
    s,f=call('POST','/api/v2/folders',{'spaceId':space,'title':'Versions précédentes','parentId':MANUEL}); print('create folder',s,str(f)[:200]); fid=f.get('id')
print('folder',fid)
LEG=['1643053071','1642135634','1643511890','1641873425','1643773993','1643806771','1643577360','1643675716','1643937818','1643347979','1643380838','1643773978','1643642895','1643348000','1643675738','1643937869','1643806796','1643774066']
for pid in LEG:
    s,r=call('PUT','/rest/api/content/%s/move/append/%s'%(pid,fid)); print('move',pid,s,str(r)[:120])
s,kids=call('GET','/api/v2/folders/%s/direct-children?limit=100'%fid)
print('in folder',len(kids.get('results',[])),[k['title'][:25] for k in kids.get('results',[])])
json.dump({'folder':fid},open('/tmp/relrev/fr-folder.json','w'))
