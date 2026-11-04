#!/usr/bin/env python3
"""Publish the 21 Oct 2026 new-feature pages. Serial, guarded. Writes ids to ids.json."""
import importlib.util, json, os, subprocess, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
PUB = os.path.join(os.path.dirname(HERE), 'confluence-publish.py')
spec = importlib.util.spec_from_file_location('pub', PUB)
pub = importlib.util.module_from_spec(spec); spec.loader.exec_module(pub)
b, a = pub.load_creds()
ids_path = os.path.join(HERE, 'ids.json')
ids = json.load(open(ids_path)) if os.path.exists(ids_path) else {}

space_id = pub.api(b, a, 'GET', '/api/v2/pages/1326972929')['spaceId']

def folder(title, parent):
    if title in ids: return ids[title]
    kids = pub.api(b, a, 'GET', f'/api/v2/folders/{parent}/direct-children?limit=100').get('results', [])
    for k in kids:
        if k['title'] == title and k['type'] == 'folder':
            ids[title] = k['id']; return k['id']
    r = pub.api(b, a, 'POST', '/api/v2/folders', {'spaceId': space_id, 'title': title, 'parentId': parent})
    ids[title] = r['id']; json.dump(ids, open(ids_path, 'w'), indent=1); return r['id']

def page(key, title, parent, xhtml, images, labels):
    if key not in ids:
        r = pub.api(b, a, 'POST', '/api/v2/pages', {'spaceId': space_id, 'status': 'current', 'title': title,
              'parentId': parent, 'body': {'representation': 'storage', 'value': '<p/>'}})
        pid = r['id']
        if str(r.get('parentId')) != str(parent): sys.exit(f'{key}: parent mismatch {r.get("parentId")} != {parent}')
        ids[key] = pid; json.dump(ids, open(ids_path, 'w'), indent=1)
        print('created', key, pid)
    pid = ids[key]
    out = subprocess.run([sys.executable, PUB, '--page', pid, '--xhtml', os.path.join(HERE, xhtml),
                          '--images', os.path.join(HERE, images)], capture_output=True, text=True)
    print(out.stdout.strip()[-200:], out.stderr.strip()[-400:])
    if out.returncode: sys.exit(f'{key}: publish failed')
    chk = pub.api(b, a, 'GET', f'/api/v2/pages/{pid}')
    if str(chk['id']) != str(pid): sys.exit('crossed read')
    for l in labels:
        pub.api(b, a, 'POST', f'/rest/api/content/{pid}/label', [{'prefix': 'global', 'name': l}])
    print('ok', key, pid, chk['title'], 'parent', chk.get('parentId'))
    time.sleep(1)
    return pid

which = sys.argv[1:]
EUM, RVR, ORD, PATH, REVIEW = '1329758211', '1679589479', '1679458388', '1679458391', '1189609473'
plan = [
 ('rpq', 'Report Print Queue: print and reprint patient reports', RVR, 'rpq.xhtml', 'img-rpq', ['doc-in-review']),
 ('sent', 'Sent Messages: check and resend deliveries', RVR, 'sent.xhtml', 'img-sent', ['doc-in-review']),
 ('modify', 'Modify an order and the optional requesting provider', ORD, 'modify.xhtml', 'img-deltas', ['doc-in-review']),
 ('patho', 'Record cassettes and slides on a pathology case', PATH, 'patho.xhtml', 'img-deltas', ['doc-in-review']),
 ('invitems', 'Manage inventory items, lots, counts and reorders', 'INV', 'invitems.xhtml', 'img-inv-board', ['doc-in-review']),
 ('invrecv', 'Receive stock and run inventory reports', 'INV', 'invrecv.xhtml', 'img-inv-receive', ['doc-in-review']),
 ('amradmin', 'Microbiology (pre-release): set up tests and reference data', REVIEW, 'amradmin.xhtml', 'img-amr-admin', ['manual-draft']),
 ('amrcase', 'Microbiology (pre-release): work a case from culture to release', REVIEW, 'amrcase.xhtml', 'img-amr-case', ['manual-draft']),
 ('amrwhonet', 'Microbiology (pre-release): WHONET export', REVIEW, 'amrwhonet.xhtml', 'img-amr-case', ['manual-draft']),
]
for key, title, parent, x, im, labels in plan:
    if which and key not in which: continue
    if parent == 'INV': parent = folder('Inventory', EUM)
    page(key, title, parent, x, im, labels)
json.dump(ids, open(ids_path, 'w'), indent=1)
print(json.dumps(ids))
