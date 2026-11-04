import importlib.util, os, json, sys, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); PUB = os.path.dirname(HERE)
spec = importlib.util.spec_from_file_location('pub', os.path.join(PUB, 'confluence-publish.py'))
pub = importlib.util.module_from_spec(spec); spec.loader.exec_module(pub)
b, a = pub.load_creds()
plan = json.load(open(os.path.join(HERE, 'plan.json')))
LEGACY = '1657864193'
def labels(pid):
    return [l['name'] for l in pub.api(b, a, 'GET', f'/rest/api/content/{pid}/label?limit=200').get('results', [])]
for pid, m in plan.items():
    p = pub.api(b, a, 'GET', f'/api/v2/pages/{pid}?body-format=storage')
    if str(p['id']) != pid: sys.exit('crossed read ' + pid)
    if p['version']['number'] != m['version']: print(pid, 'SKIP changed since dump', p['version']['number']); continue
    body = open(os.path.join(HERE, f'{pid}.final.xhtml')).read()
    msg = 'Cleared from review: work-in-progress note removed, labels set' if 'label' in m else ('Landing: In review removed for 12 cleared pages' if m.get('landing') else 'Retired: superseded by Register a New Patient')
    req = {'id': pid, 'status': 'current', 'title': p['title'], 'body': {'representation': 'storage', 'value': body},
           'version': {'number': p['version']['number'] + 1, 'message': msg}}
    if m.get('retire'): req['parentId'] = LEGACY
    r = pub.api(b, a, 'PUT', f'/api/v2/pages/{pid}', req)
    print(pid, 'v', r['version']['number'], 'parent', r.get('parentId'))
    if 'label' in m:
        args = ['-doc-in-review', '+doc-verified', '+' + m['label']]
        out = subprocess.run([sys.executable, os.path.join(PUB, 'labels.py'), pid] + args, capture_output=True, text=True)
        print('  labels.py', out.returncode, (out.stdout + out.stderr).strip()[-200:])
        print('  now', labels(pid))
    if m.get('retire'):
        out = subprocess.run([sys.executable, os.path.join(PUB, 'labels.py'), pid, '-doc-in-review', '-manual-draft'], capture_output=True, text=True)
        print('  retire labels', labels(pid))
