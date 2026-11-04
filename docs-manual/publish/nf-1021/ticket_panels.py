import importlib.util, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('pub', os.path.join(os.path.dirname(HERE), 'confluence-publish.py'))
pub = importlib.util.module_from_spec(spec); spec.loader.exec_module(pub)
b, a = pub.load_creds()
OLD = 'It is waiting for review, so details may still change.'
MAP = {'1729429517': 'OGC-1536', '1729724423': 'OGC-1537', '1729134594': 'OGC-1538',
       '1729167388': 'OGC-1539', '1729462279': 'OGC-1540', '1729560592': 'OGC-1541'}
for pid, t in MAP.items():
    p = pub.api(b, a, 'GET', f'/api/v2/pages/{pid}?body-format=storage')
    if str(p['id']) != pid: sys.exit('crossed read ' + pid)
    body = p['body']['storage']['value']
    if t in body: print(pid, 'already'); continue
    if body.count(OLD) != 1: sys.exit(f'{pid}: panel text count {body.count(OLD)}')
    body = body.replace(OLD, f'It is being reviewed under <a href="https://uwdigi.atlassian.net/browse/{t}">{t}</a>, so details may still change.')
    r = pub.api(b, a, 'PUT', f'/api/v2/pages/{pid}', {'id': pid, 'status': 'current', 'title': p['title'],
        'body': {'representation': 'storage', 'value': body},
        'version': {'number': p['version']['number'] + 1, 'message': f'Review ticket {t}'}})
    print(pid, t, 'v', r['version']['number'])
