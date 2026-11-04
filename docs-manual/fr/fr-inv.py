import os, json, base64, urllib.request, urllib.parse
env = dict(l.strip().split('=',1) for l in open(os.path.expanduser('~/.openelis/confluence.env')) if '=' in l)
env = {k:v.strip().strip('"').strip("'") for k,v in env.items()}
A = base64.b64encode((env['CONFLUENCE_EMAIL']+':'+env['CONFLUENCE_API_TOKEN']).encode()).decode()
B='https://uwdigi.atlassian.net/wiki'
def get(u):
    r=urllib.request.Request(u if u.startswith('http') else B+u, headers={'Authorization':'Basic '+A,'Accept':'application/json'})
    return json.load(urllib.request.urlopen(r))
out=[]
for cql in ['space=OG and type=page and creator="5ec313eb1114700c34e02f1a"', 'space=OG and type=page and (title~"PARTIE" or title~"Manuel")', 'space=OGF and type=page']:
    u='/rest/api/content/search?'+urllib.parse.urlencode({'cql':cql,'limit':100,'expand':'ancestors,version,history,metadata.properties'})
    while u:
        d=get(u)
        for p in d['results']:
            out.append({'id':p['id'],'title':p['title'],'space':p.get('_expandable',{}).get('space','')[-5:],'creator':p['history']['createdBy'].get('displayName'),
               'created':p['history']['createdDate'][:10],'ver':p['version']['number'],'when':p['version']['when'][:10],
               'parent':(p['ancestors'][-1]['id'],p['ancestors'][-1]['title']) if p['ancestors'] else None,
               'anc':' > '.join(a['title'][:25] for a in p['ancestors'][-3:])})
        u=d['_links'].get('next')
seen={}; 
for o in out: seen[o['id']]=o
json.dump(list(seen.values()),open('/tmp/relrev/fr.json','w'),ensure_ascii=False)
for o in sorted(seen.values(), key=lambda x:(x['anc'],x['title'])):
    print(o['id'],'|',o['title'][:55],'|',o['creator'][:12],'|',o['created'],'v',o['ver'],o['when'],'|',o['anc'])
