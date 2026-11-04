import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from frlib import *
st = json.load(open(os.path.join(HERE, 'state.json')))
for en in sys.argv[1:]:
    fr = st['fr'][en]
    p = page(fr)
    adf = json.loads(p['body']['atlas_doc_format']['value'])
    meds = []
    def w(n):
        if isinstance(n, dict):
            if n.get('type') == 'media': meds.append(n['attrs'])
            [w(v) for v in n.values()]
        elif isinstance(n, list): [w(v) for v in n]
    w(adf)
    att = {a['fileId']: a for a in get('/api/v2/pages/%s/attachments?limit=100' % fr)['results']}
    ok = sum(1 for m in meds if m.get('id') in att and m.get('collection') == 'contentId-%s' % fr)
    print(en, fr, p['title'][:45], 'v%s' % p['version']['number'], 'media', len(meds), 'resolved', ok, 'parent', p.get('parentId'))
