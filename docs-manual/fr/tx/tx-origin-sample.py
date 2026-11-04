#!/usr/bin/env python3
"""Read-only: show attributes/relationships of a few live translations for a language."""
import json, os, sys, urllib.request, urllib.parse
env = dict(l.strip().split('=', 1) for l in open(os.path.expanduser('~/.openelis/transifex.env')) if '=' in l)
T = env['TRANSIFEX_TOKEN'].strip().strip('"').strip("'")
lang = sys.argv[1]
url = 'https://rest.api.transifex.com/resource_translations?' + urllib.parse.urlencode({'filter[resource]': 'o:openmrs:p:openelis-1:r:enjson', 'filter[language]': 'l:' + lang, 'limit': 3})
r = urllib.request.Request(url, headers={'Authorization': 'Bearer ' + T, 'Accept': 'application/vnd.api+json'})
d = json.load(urllib.request.urlopen(r))
for t in d['data']:
    print(json.dumps(t['attributes'], ensure_ascii=False)[:600]); print(json.dumps(t['relationships'])[:600]); print('--')
