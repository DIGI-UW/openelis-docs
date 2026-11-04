#!/usr/bin/env python3
"""Fetch each English page at the version its French was translated from, into fr/refresh/old/<en>.json.
usage (on the Mac, via Control-your-Mac): python3 fr/refresh/fr-fetch-old.py EN_ID [EN_ID ...]
The version comes from the French page's openelis-translation property (sourceVersion), found through
fr/state.json. Needs frlib credentials (~/.openelis/confluence.env)."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); FR = os.path.dirname(HERE)
sys.path.insert(0, FR)
from frlib import *
st = json.load(open(os.path.join(FR, 'state.json')))
os.makedirs(os.path.join(HERE, 'old'), exist_ok=True)
for en in sys.argv[1:]:
    fr = st['fr'][en]
    sv = get('/rest/api/content/%s/property/openelis-translation' % fr)['value']['sourceVersion']
    p = get('/api/v2/pages/%s?version=%s&body-format=atlas_doc_format' % (en, sv))
    json.dump(dict(id=en, title=p['title'], version=sv, adf=json.loads(p['body']['atlas_doc_format']['value'])),
              open(os.path.join(HERE, 'old', en + '.json'), 'w'), ensure_ascii=False)
    print(en, 'v%s' % sv, p['title'][:50])
