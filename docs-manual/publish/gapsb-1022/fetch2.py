#!/usr/bin/env python3
"""Fork B: dump current storage of pages to update, plus Administrator Guide tree."""
import importlib.util, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('pub', os.path.join(os.path.dirname(HERE), 'confluence-publish.py'))
pub = importlib.util.module_from_spec(spec); spec.loader.exec_module(pub)
b, a = pub.load_creds()
os.makedirs(os.path.join(HERE, 'cur'), exist_ok=True)
for pid in sys.argv[1:]:
    p = pub.api(b, a, 'GET', f'/api/v2/pages/{pid}?body-format=storage')
    open(os.path.join(HERE, 'cur', f'{pid}.xhtml'), 'w').write(p['body']['storage']['value'])
    print(pid, p['title'], 'v', p['version']['number'], 'parent', p.get('parentId'), p.get('parentType'))
def kids(pid, depth=0, kind='pages'):
    r = pub.api(b, a, 'GET', f'/api/v2/{kind}/{pid}/direct-children?limit=100').get('results', [])
    for k in r:
        print('  ' * depth + f"- {k['type']} {k['id']} {k['title']}")
        if depth < 2: kids(k['id'], depth + 1, 'folders' if k['type'] == 'folder' else 'pages')
print('== Administrator Guide 257458193')
kids('257458193', 0, 'folders')
