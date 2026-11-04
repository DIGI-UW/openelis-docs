import json, shutil
p = 'docs-manual/contracts.json'
shutil.copy(p, p + '.bak-20261013-us')
c = json.load(open(p))
rep = {'Analysers': 'Analyzers', 'Add Analyser': 'Add Analyzer', 'Total analysers': 'Total analyzers',
       'Set up a new analyser': 'Set up a new analyzer', 'Analyser type': 'Analyzer type',
       'Analyser name': 'Analyzer name', 'Analyser Types': 'Analyzer Types',
       'The reusable setups behind your analysers': 'The reusable setups behind your analyzers'}
n = 0
def fix(o):
    global n
    if isinstance(o, dict):
        return {k: fix(v) for k, v in o.items()}
    if isinstance(o, list):
        return [fix(v) for v in o]
    if isinstance(o, str) and o in rep:
        n += 1
        return rep[o]
    return o
for i, s in enumerate(c['sections']):
    if s.get('id') == 'analyzer-setup':
        c['sections'][i] = fix(s)
        c['sections'][i]['note'] = (s.get('note', '') + ' Anchors use en-US spelling (the drift run uses the default locale); the page figures were captured in the en locale (Analyser).').strip()
json.dump(c, open(p, 'w'), indent=2, ensure_ascii=False)
print('replaced', n)
