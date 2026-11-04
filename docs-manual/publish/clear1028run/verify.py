import importlib.util, os, re, json, html
HERE = os.path.dirname(os.path.abspath(__file__)); PUB = os.path.dirname(HERE)
spec = importlib.util.spec_from_file_location('pub', os.path.join(PUB, 'confluence-publish.py'))
pub = importlib.util.module_from_spec(spec); spec.loader.exec_module(pub)
b, a = pub.load_creds()
for pid in json.load(open(os.path.join(HERE, 'plan.json'))):
    p = pub.api(b, a, 'GET', f'/api/v2/pages/{pid}?body-format=storage')
    s = p['body']['storage']['value']; txt = re.sub(r'<[^>]+>', '', s)
    names = {x['title'] for x in pub.api(b, a, 'GET', f'/rest/api/content/{pid}/child/attachment?limit=200')['results']}
    refs = [html.unescape(x) for x in re.findall(r'<ri:attachment ri:filename="([^"]*)"', s)]
    print(pid, 'v', p['version']['number'], 'parent', p.get('parentId'), 'em', txt.count('—') + txt.count('&mdash;'), 'wip', 'Work in progress' in s,
          'imgs', len(refs), 'missing', [r for r in refs if r not in names], 'inreview', txt.count('In review'))
