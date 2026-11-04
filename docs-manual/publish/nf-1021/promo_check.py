import importlib.util, os, re, json, urllib.parse
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('pub', os.path.join(os.path.dirname(HERE), 'confluence-publish.py'))
pub = importlib.util.module_from_spec(spec); spec.loader.exec_module(pub)
b, a = pub.load_creds()
def cql(q):
    out, start = [], 0
    while True:
        r = pub.api(b, a, 'GET', '/rest/api/content/search?limit=100&start=%d&expand=metadata.labels,version,ancestors&cql=%s' % (start, urllib.parse.quote(q)))
        out += r['results']
        if r.get('size', 0) < 100: return out
        start += 100
rows = {}
for q in ['space = OG and type = page and label = "doc-in-review"',
          'space = OG and type = page and ancestor = 1189609473',
          'space = OG and type = page and label = "doc-verified" and lastmodified >= "2026-10-14"']:
    for c in cql(q):
        rows[c['id']] = c
res = []
for pid, c in rows.items():
    labels = [l['name'] for l in c['metadata']['labels']['results']]
    body = pub.api(b, a, 'GET', f'/api/v2/pages/{pid}?body-format=storage')['body']['storage']['value']
    wip = 'Work in progress.' in body
    tick = re.findall(r'OGC-\d+', re.sub(r'<[^>]+>', ' ', body)[:2500])
    under_review = any(x['id'] == '1189609473' for x in c.get('ancestors', []))
    parent = c['ancestors'][-1]['id'] if c.get('ancestors') else None
    res.append({'id': pid, 'title': c['title'], 'v': c['version']['number'], 'when': c['version']['when'][:10], 'labels': labels,
                'wip': wip, 'review_area': under_review, 'parent': parent, 'tickets_top': list(dict.fromkeys(tick))[:4],
                'stamp': bool(re.search(r'doc-verified|verified-v?3', re.sub(r'<[^>]+>', ' ', body)[:600]))})
json.dump(res, open(os.path.join(HERE, 'promo_check.json'), 'w'), indent=1)
for r in sorted(res, key=lambda r: (not r['review_area'], r['title'])):
    print(r['id'], '|', r['title'][:60], '| v', r['v'], r['when'], '| RA' if r['review_area'] else '| live', '| WIP' if r['wip'] else '|', '|', ','.join(r['labels']), '|', ','.join(r['tickets_top']), '| stamp' if r['stamp'] else '')
