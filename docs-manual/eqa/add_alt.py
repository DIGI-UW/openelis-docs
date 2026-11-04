import os,base64,json,re,html,urllib.request,sys
env={}
for l in open(os.path.expanduser('~/.openelis/confluence.env')):
    if '=' in l: k,v=l.strip().split('=',1); env[k]=v
auth='Basic '+base64.b64encode((env['CONFLUENCE_EMAIL']+':'+env['CONFLUENCE_API_TOKEN']).encode()).decode()
B=env['CONFLUENCE_BASE']
def req(url,data=None,method='GET'):
    r=urllib.request.Request(B+url,data=json.dumps(data).encode() if data else None,method=method,headers={'Authorization':auth,'Content-Type':'application/json'})
    return json.load(urllib.request.urlopen(r))
for pid in sys.argv[1:]:
    d=req(f'/rest/api/content/{pid}?expand=body.storage,version')
    s=d['body']['storage']['value']
    pat=re.compile(r'<ac:image((?: [^>]*)?)>(<ri:attachment [^>]*/>)</ac:image>(</p>\s*<p><em>Figure \d+\.\s*)([^<]+)(</em>)')
    n=[0]
    def rep(m):
        attrs=m.group(1)
        if 'ac:alt' in attrs: return m.group(0)
        alt=html.unescape(m.group(4)).replace(': ',' - ').replace(':',' - ').replace('"','').strip()
        n[0]+=1
        return f'<ac:image{attrs} ac:alt="{html.escape(alt,quote=True)}">{m.group(2)}</ac:image>{m.group(3)}{m.group(4)}{m.group(5)}'
    s2=pat.sub(rep,s)
    print(pid,'images',s.count('<ac:image'),'alt added',n[0])
    if n[0]:
        req(f'/rest/api/content/{pid}',{'id':pid,'type':'page','title':d['title'],'version':{'number':d['version']['number']+1,'message':'figure alt text from captions'},'body':{'storage':{'value':s2,'representation':'storage'}}},'PUT')
        print('updated to v',d['version']['number']+1)
