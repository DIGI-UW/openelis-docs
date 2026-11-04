#!/usr/bin/env python3
"""Push approved French UI strings to Transifex (OpenMRS / openelis-1 / enjson, language fr).

Inputs (same folder):
  decisions.json   approved/rejected decisions exported from the French UI Crosswalk artifact
Token: ~/.openelis/transifex.env with TRANSIFEX_TOKEN=...

Default is a DRY RUN: it downloads the live French, compares each approved string with the French that
was reviewed, and writes tx-push-report.json. Nothing is changed in Transifex.
  --apply      actually PATCH the approved strings (only those whose live value still equals the
               reviewed value; anything edited in Transifex since is reported as a conflict and skipped)
  --live-json  also save the live French as fr-live.json
"""
import json, os, sys, time, urllib.request, urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
env = dict(l.strip().split('=', 1) for l in open(os.path.expanduser('~/.openelis/transifex.env')) if '=' in l)
TOKEN = env['TRANSIFEX_TOKEN'].strip().strip('"').strip("'")
API = 'https://rest.api.transifex.com'
RES = 'o:openmrs:p:openelis-1:r:enjson'
LANG = 'l:' + next((a.split('=',1)[1] for a in sys.argv if a.startswith('--lang=')), 'fr')
DEC = next((a.split('=',1)[1] for a in sys.argv if a.startswith('--decisions=')), 'decisions.json')
PLURAL = {'l:id': ('other',), 'l:zh': ('other',), 'l:zh_CN': ('other',), 'l:fr': ('one', 'many', 'other'), 'l:es': ('one', 'many', 'other')}.get(LANG, ('one', 'many', 'other'))
APPLY = '--apply' in sys.argv

def call(method, path, body=None, ctype='application/vnd.api+json'):
    h = {'Authorization': 'Bearer ' + TOKEN, 'Accept': 'application/vnd.api+json'}
    data = None
    if body is not None:
        data = json.dumps(body).encode(); h['Content-Type'] = ctype
    url = path if path.startswith('http') else API + path
    for i in range(5):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, data=data, method=method, headers=h)) as r:
                b = r.read(); return json.loads(b) if b else {}
        except urllib.error.HTTPError as e:
            if e.code == 429 or e.code >= 500:
                time.sleep(int(e.headers.get('Retry-After', 3 * (i + 1)))); continue
            raise RuntimeError('%s %s -> %s %s' % (method, url, e.code, e.read()[:400].decode('utf8', 'replace')))

# 1. live French, keyed by string key (Transifex escapes "." in KEYVALUEJSON keys as "\\.")
import re
unesc = lambda k: re.sub(r'\\(.)', r'\1', k)
live = {}
url = '/resource_translations?' + urllib.parse.urlencode({'filter[resource]': RES, 'filter[language]': LANG, 'include': 'resource_string', 'limit': 1000})
while url:
    d = call('GET', url)
    strings = {s['id']: s for s in d.get('included', [])}
    for t in d['data']:
        sid = t['relationships']['resource_string']['data']['id']
        s = strings.get(sid, {}).get('attributes', {})
        key = s.get('key')
        if key is None: continue
        forms = t['attributes'].get('strings') or None
        live[unesc(key)] = {'id': t['id'], 'forms': forms, 'fr': (forms or {}).get('other'),
                            'pluralized': bool(s.get('pluralized')), 'source': (s.get('strings') or {}).get('other'),
                            'reviewed': t['attributes'].get('reviewed')}
    url = d.get('links', {}).get('next')
print('live French strings:', len(live), 'translated:', sum(1 for v in live.values() if v['forms']))
if '--live-json' in sys.argv:
    json.dump({k: v['fr'] for k, v in live.items() if v['fr'] is not None}, open(os.path.join(HERE, LANG[2:] + '-live.json'), 'w'), ensure_ascii=False, indent=1)

ICU = re.compile(r'^\{(\w+),\s*plural,\s*(.*)\}$', re.S)
def plural_forms(value):
    """'{count, plural, one {# x} other {# y}}' -> {'one': '# x', 'many': '# y', 'other': '# y'} for French; None if not a single plural."""
    m = ICU.match(value.strip())
    if not m: return None
    body, forms, i = m.group(2), {}, 0
    while i < len(body):
        mm = re.match(r'\s*(=?\w+)\s*\{', body[i:])
        if not mm: break
        name = mm.group(1); j = i + mm.end(); depth = 1; k = j
        while k < len(body) and depth:
            depth += {'{': 1, '}': -1}.get(body[k], 0); k += 1
        forms[name] = body[j:k - 1]; i = k
    if 'other' not in forms: return None
    forms.setdefault('one', forms['other']); forms.setdefault('many', forms['other'])
    return {k: v for k, v in forms.items() if k in PLURAL}

# 2. compare with approved decisions
dec = json.load(open(os.path.join(HERE, DEC)))
ok, conflict, missing, same, plural_skip = [], [], [], [], []
for d in dec:
    if d.get('status') != 'approved': continue
    k, new, orig = d['key'], d['value'], d.get('original') or None
    L = live.get(k)
    if not L: missing.append(k); continue
    # GitHub fr.json shows English for strings untranslated in Transifex, so "reviewed = English" matches an empty live value
    live_val = L['fr'] if L['forms'] else L['source']
    if L['pluralized']:
        if orig is not None and L['forms'] and L['forms'].get('other') != orig and LANG != 'l:fr':
            conflict.append({'key': k, 'reviewed': orig, 'live': L['fr'], 'approved': new}); continue
        pf = plural_forms(new)
        if pf is None: plural_skip.append({'key': k, 'approved': new}); continue
        if L['forms'] == pf: same.append(k); continue
        ok.append({'id': L['id'], 'key': k, 'from': L['forms'], 'to': pf, 'plural': True}); continue
    if L['forms'] and live_val == new: same.append(k); continue
    if (live_val or None) != orig and not (L['forms'] is None and orig is None):
        conflict.append({'key': k, 'reviewed': orig, 'live': L['fr'], 'approved': new}); continue
    ok.append({'id': L['id'], 'key': k, 'from': L['fr'], 'to': {'other': new}})

report = {'at': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), 'apply': APPLY, 'toPush': len(ok), 'alreadyLive': len(same),
          'conflicts': conflict, 'notInTransifex': missing, 'pluralNotParsed': plural_skip, 'pushed': 0, 'errors': []}

# 3. push
if APPLY:
    for i in range(0, len(ok), 150):
        chunk = ok[i:i + 150]
        body = {'data': [{'id': x['id'], 'type': 'resource_translations', 'attributes': {'strings': x['to']}} for x in chunk]}
        try:
            call('PATCH', '/resource_translations', body, 'application/vnd.api+json;profile="bulk"')
            report['pushed'] += len(chunk)
        except RuntimeError as e:
            report['errors'].append(str(e)[:400])
        print('pushed', report['pushed'], 'of', len(ok), flush=True)
report['changes'] = ok
json.dump(report, open(os.path.join(HERE, 'tx-push-report%s.json' % ('' if LANG == 'l:fr' else '-' + LANG[2:])), 'w'), ensure_ascii=False, indent=1)
print(('APPLIED' if APPLY else 'DRY RUN') + ': %d to push (%d plural), %d already live, %d conflicts, %d not in Transifex, %d plural not parsed, %d pushed, %d errors'
      % (len(ok), sum(1 for x in ok if x.get('plural')), len(same), len(conflict), len(missing), len(plural_skip), report['pushed'], len(report['errors'])))
