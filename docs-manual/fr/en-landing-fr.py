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
PID='1326972929'
s,pg=call('GET','/api/v2/pages/%s?body-format=atlas_doc_format'%PID); assert pg['id']==PID
doc=json.loads(pg['body']['atlas_doc_format']['value'])
C=doc['content']
i=next(k for k,n in enumerate(C) if n['type']=='heading' and 'French' in json.dumps(n))
j=i+1
assert C[j]['type']=='paragraph' and 'Fonctionnalit' in json.dumps(C[j]), json.dumps(C[j])[:300]
def t(x,m=None):
    d={'type':'text','text':x}
    if m: d['marks']=m
    return d
lk=lambda x,h: t(x,[{'type':'link','attrs':{'href':h}},{'type':'strong'}])
C[j]={'type':'paragraph','content':[t('The French manual is at '),lk('📖 Manuel de l\'utilisateur','https://uwdigi.atlassian.net/wiki/spaces/OG/pages/1641447437'),
 t('. It links the pages already translated and falls back to English where a page is not yet translated. Older French pages are kept in '),
 t('Versions précédentes',[{'type':'link','attrs':{'href':'https://uwdigi.atlassian.net/wiki/spaces/OG/folder/1679458382'}}]),
 t('. The French functional requirements are at '),t('Fonctionnalités d\'OpenELIS',[{'type':'link','attrs':{'href':'https://uwdigi.atlassian.net/wiki/spaces/oeg/pages/755728390'}}]),t('.')]}
body={'id':PID,'status':'current','title':pg['title'],'body':{'representation':'atlas_doc_format','value':json.dumps(doc,ensure_ascii=False)},
      'version':{'number':pg['version']['number']+1,'message':'Point the French section at the French manual and its Versions précédentes folder'}}
s,r=call('PUT','/api/v2/pages/%s'%PID,body); print('put',s,str(r)[:300] if s!=200 else r['version']['number'])
