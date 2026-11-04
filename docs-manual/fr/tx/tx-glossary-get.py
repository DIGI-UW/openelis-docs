#!/usr/bin/env python3
"""Download a Transifex glossary as CSV (read-only). Usage: tx-glossary-get.py [glossary_id] [out.csv]"""
import json, os, sys, time, urllib.request
env = dict(l.strip().split('=', 1) for l in open(os.path.expanduser('~/.openelis/transifex.env')) if '=' in l)
T = env['TRANSIFEX_TOKEN'].strip().strip('"').strip("'")
GID = sys.argv[1] if len(sys.argv) > 1 else 'o:openmrs:g:openelis-glossary'
OUT = sys.argv[2] if len(sys.argv) > 2 else 'openelis-glossary-live.csv'
H = {'Authorization': 'Bearer ' + T, 'Accept': 'application/vnd.api+json', 'Content-Type': 'application/vnd.api+json'}
class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k): return None
op = urllib.request.build_opener(NoRedirect)
def call(method, url, body=None):
    r = urllib.request.Request(url if url.startswith('http') else 'https://rest.api.transifex.com' + url, data=json.dumps(body).encode() if body else None, method=method, headers=H)
    try:
        with op.open(r) as resp: return resp.status, resp.headers, resp.read()
    except urllib.error.HTTPError as e: return e.code, e.headers, e.read()
st, h, b = call('POST', '/glossaries_async_downloads', {'data': {'type': 'glossaries_async_downloads', 'relationships': {'glossary': {'data': {'type': 'glossaries', 'id': GID}}}}})
print('create', st, b[:300])
jid = json.loads(b)['data']['id']
for i in range(30):
    time.sleep(2)
    st, h, b = call('GET', '/glossaries_async_downloads/' + jid)
    if st == 303:
        url = h['Location']; data = urllib.request.urlopen(url).read(); open(OUT, 'wb').write(data); print('saved', OUT, len(data)); break
    print('status', st, b[:200])
p = json.loads(call('GET', '/projects/o:openmrs:p:openelis-1')[2])
print('project glossary relationship:', json.dumps(p['data']['relationships'].get('glossary') or {k: v for k, v in p['data']['relationships'].items() if 'gloss' in k}))
print('project attrs with gloss:', {k: v for k, v in p['data']['attributes'].items() if 'gloss' in k.lower()})
