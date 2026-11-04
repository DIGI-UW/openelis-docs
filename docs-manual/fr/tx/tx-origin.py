#!/usr/bin/env python3
"""Read-only: download all translations for a language with who/how they were made.
Usage: tx-origin.py <lang>   -> writes origin-<lang>.json"""
import json, os, sys, time, re, urllib.request, urllib.parse, collections
env = dict(l.strip().split('=', 1) for l in open(os.path.expanduser('~/.openelis/transifex.env')) if '=' in l)
T = env['TRANSIFEX_TOKEN'].strip().strip('"').strip("'")
lang = sys.argv[1]
def get(url):
    for i in range(5):
        try:
            r = urllib.request.Request(url if url.startswith('http') else 'https://rest.api.transifex.com' + url, headers={'Authorization': 'Bearer ' + T, 'Accept': 'application/vnd.api+json'})
            return json.load(urllib.request.urlopen(r))
        except urllib.error.HTTPError as e:
            if e.code in (429,) or e.code >= 500: time.sleep(3 * (i + 1)); continue
            raise SystemExit('%s %s' % (e.code, e.read()[:400]))
url = '/resource_translations?' + urllib.parse.urlencode({'filter[resource]': 'o:openmrs:p:openelis-1:r:enjson', 'filter[language]': 'l:' + lang, 'include': 'resource_string', 'limit': 1000})
out = []; first = True
while url:
    d = get(url)
    S = {s['id']: s['attributes'] for s in d.get('included', [])}
    for t in d['data']:
        if first: print(json.dumps(t['attributes'])[:800]); print(json.dumps(t['relationships'])[:800]); first = False
        s = S.get(t['relationships']['resource_string']['data']['id'], {})
        rel = t['relationships']
        tr = (rel.get('translator') or {}).get('data') or {}
        rv = (rel.get('reviewer') or {}).get('data') or {}
        a = t['attributes']
        out.append({'key': re.sub(r'\\(.)', r'\1', s.get('key') or ''), 'en': (s.get('strings') or {}).get('other'), 'tr': (a.get('strings') or {}).get('other') if a.get('strings') else None,
                    'origin': a.get('origin'), 'reviewed': a.get('reviewed'), 'proofread': a.get('proofread'), 'when': a.get('datetime_translated'),
                    'translator': tr.get('id'), 'reviewer': rv.get('id')})
    url = d.get('links', {}).get('next')
json.dump(out, open('origin-%s.json' % lang, 'w'), ensure_ascii=False)
done = [o for o in out if o['tr']]
print(lang, 'strings', len(out), 'translated', len(done))
print('origin', collections.Counter(o['origin'] for o in done).most_common())
print('translator', collections.Counter(o['translator'] for o in done).most_common(12))
print('reviewed', collections.Counter(o['reviewed'] for o in done))
print('year', collections.Counter((o['when'] or '')[:7] for o in done).most_common(15))
