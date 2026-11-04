#!/usr/bin/env python3
"""Fork B: create the two new Administrator Guide pages as placeholders (serial, parent-checked)."""
import importlib.util, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('pub', os.path.join(os.path.dirname(HERE), 'confluence-publish.py'))
pub = importlib.util.module_from_spec(spec); spec.loader.exec_module(pub)
b, a = pub.load_creds()
ids_path = os.path.join(HERE, 'ids.json')
ids = json.load(open(ids_path)) if os.path.exists(ids_path) else {}
space_id = pub.api(b, a, 'GET', '/api/v2/pages/1729429517')['spaceId']
PAGES = [('notif', 'Admin: Set up notification triggers, templates, channels and delivery', '1680441357'),
         ('header', 'Admin: Set the patient report header (Printed Report Configuration)', '1680441354')]
for key, title, parent in PAGES:
    if key in ids: print('exists', key, ids[key]); continue
    r = pub.api(b, a, 'POST', '/api/v2/pages', {'spaceId': space_id, 'status': 'current', 'title': title,
          'parentId': parent, 'body': {'representation': 'storage', 'value': '<p>Draft in progress.</p>'}})
    chk = pub.api(b, a, 'GET', f"/api/v2/pages/{r['id']}")
    if str(chk.get('parentId')) != parent: sys.exit(f'{key}: parent mismatch {chk.get("parentId")}')
    ids[key] = r['id']; json.dump(ids, open(ids_path, 'w'), indent=1)
    print('created', key, r['id'], chk['title'], 'parent', chk.get('parentId'))
