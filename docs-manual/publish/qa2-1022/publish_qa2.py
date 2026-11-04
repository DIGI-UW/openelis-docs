#!/usr/bin/env python3
"""Publish the 22 Oct 2026 Quality Assurance pages (Fork A) into the Quality assurance folder. Serial, guarded. ids.json."""
import importlib.util, json, os, subprocess, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
PUB = os.path.join(os.path.dirname(HERE), 'confluence-publish.py')
spec = importlib.util.spec_from_file_location('pub', PUB)
pub = importlib.util.module_from_spec(spec); spec.loader.exec_module(pub)
b, a = pub.load_creds()
ids_path = os.path.join(HERE, 'ids.json')
ids = json.load(open(ids_path)) if os.path.exists(ids_path) else {}
space_id = pub.api(b, a, 'GET', '/api/v2/pages/1326972929')['spaceId']
QA = '1706098877'

def page(key, title, parent, xhtml, images, labels):
    if key not in ids:
        r = pub.api(b, a, 'POST', '/api/v2/pages', {'spaceId': space_id, 'status': 'current', 'title': title,
              'parentId': parent, 'body': {'representation': 'storage', 'value': '<p/>'}})
        pid = r['id']
        if str(r.get('parentId')) != str(parent): sys.exit(f'{key}: parent mismatch {r.get("parentId")} != {parent}')
        ids[key] = pid; json.dump(ids, open(ids_path, 'w'), indent=1)
        print('created', key, pid)
    pid = ids[key]
    body = open(os.path.join(HERE, xhtml)).read()
    if '—' in body: sys.exit(f'{key}: em dash in body')
    out = subprocess.run([sys.executable, PUB, '--page', pid, '--xhtml', os.path.join(HERE, xhtml),
                          '--images', os.path.join(HERE, images)], capture_output=True, text=True)
    print(out.stdout.strip()[-300:], out.stderr.strip()[-400:])
    if out.returncode: sys.exit(f'{key}: publish failed')
    chk = pub.api(b, a, 'GET', f'/api/v2/pages/{pid}')
    if str(chk['id']) != str(pid): sys.exit('crossed read')
    if str(chk.get('parentId')) != QA: sys.exit(f'{key}: parent is {chk.get("parentId")}')
    for l in labels:
        pub.api(b, a, 'POST', f'/rest/api/content/{pid}/label', [{'prefix': 'global', 'name': l}])
    att = pub.api(b, a, 'GET', f'/rest/api/content/{pid}/child/attachment?limit=50')
    print('ok', key, pid, chk['title'], 'parent', chk.get('parentId'), 'attachments', att.get('size'))
    time.sleep(1)
    return pid

which = sys.argv[1:]
plan = [
 ('overview', 'QA Overview and quality indicators', 'qaoverview.xhtml', 'img-overview'),
 ('capa', 'Record corrective and preventive actions and use the CAPA Register', 'capa.xhtml', 'img-capa'),
 ('inhouse', 'Run an in-house blinded EQA panel', 'inhouse.xhtml', 'img-inhouse'),
]
for key, title, x, im in plan:
    if which and key not in which: continue
    page(key, title, QA, x, im, ['doc-in-review'])
json.dump(ids, open(ids_path, 'w'), indent=1)
print(json.dumps(ids))
