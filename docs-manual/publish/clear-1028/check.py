import importlib.util, os, re, json, urllib.parse, html
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('pub', os.path.join(os.path.dirname(HERE), 'confluence-publish.py'))
pub = importlib.util.module_from_spec(spec); spec.loader.exec_module(pub)
b, a = pub.load_creds()
meta = json.load(open(os.path.join(HERE, 'meta.json')))
for pid, m in meta.items():
    p = pub.api(b, a, 'GET', f'/api/v2/pages/{pid}?body-format=storage')
    s = p['body']['storage']['value']
    att = pub.api(b, a, 'GET', f'/rest/api/content/{pid}/child/attachment?limit=200')
    names = {x['title'] for x in att['results']}
    refs = [html.unescape(x) for x in re.findall(r'<ri:attachment ri:filename="([^"]*)"', s)]
    missing = [r for r in refs if r not in names]
    print(pid, 'v', p['version']['number'], 'meta v', m['version'], 'SAME' if p['version']['number']==m['version'] else 'CHANGED', 'refs', len(refs), 'missing', missing)
    if missing: print('   attachments:', sorted(names))
