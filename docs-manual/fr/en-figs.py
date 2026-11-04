"""Download the English figures (image attachments used on the page) for given English page ids into fr/en-figs/<id>/."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from frlib import *
for pid in sys.argv[1:]:
    src = json.load(open(os.path.join(HERE, 'src', pid + '.json')))
    d = os.path.join(HERE, 'en-figs', pid); os.makedirs(d, exist_ok=True)
    n = 0
    for a in src['attachments']:
        if not (a.get('mediaType') or '').startswith('image'): continue
        fn = os.path.join(d, a['title'])
        if os.path.exists(fn) and os.path.getsize(fn) == a.get('size'): continue
        data = req('GET', B + a['dl'] if not a['dl'].startswith('http') else a['dl'], raw=True)
        open(fn, 'wb').write(data); n += 1
    print(pid, 'downloaded', n, flush=True)
print('DONE')
