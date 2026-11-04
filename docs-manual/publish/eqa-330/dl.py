import importlib.util, os, subprocess, sys
s=importlib.util.spec_from_file_location('pub','confluence-publish.py');p=importlib.util.module_from_spec(s);s.loader.exec_module(p)
b,a=p.load_creds()
for pid in sys.argv[1:]:
  r=p.api(b,a,'GET','/rest/api/content/'+pid+'?expand=ancestors')
  print(pid, [x['id']+':'+x['title'] for x in r['ancestors']][-2:], flush=True)
  d='eqa-330/img-'+pid; os.makedirs(d, exist_ok=True)
  atts=p.api(b,a,'GET','/rest/api/content/'+pid+'/child/attachment?limit=250')['results']
  n=0
  for at in atts:
    if not at['title'].endswith('.png'): continue
    f=os.path.join(d,at['title'])
    if os.path.exists(f) and os.path.getsize(f)>1000: continue
    subprocess.run(['curl','-s','-L','-H','Authorization: Basic '+a,'-o',f, b+at['_links']['download']]); n+=1
  print(pid,'downloaded',n, flush=True)
