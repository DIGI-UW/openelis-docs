import sys, os, re, importlib.util, html
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('pub', os.path.join(os.path.dirname(HERE), 'confluence-publish.py'))
pub = importlib.util.module_from_spec(spec); spec.loader.exec_module(pub)
base, auth = pub.load_creds()
PID = '1326972929'; DRY = '--dry-run' in sys.argv
p = pub.api(base, auth, 'GET', f'/api/v2/pages/{PID}?body-format=storage')
if str(p['id']) != PID: sys.exit('crossed read')
s = p['body']['storage']['value']
print('headings:', re.findall(r'<h3>(.*?)</h3>', s))
def row(title, text, desc):
    t = html.escape(title, quote=True)
    return (f'<tr><td><p><ac:link><ri:page ri:content-title="{t}" /><ac:link-body>{html.escape(text)}</ac:link-body></ac:link></p></td>'
            f'<td><p>{html.escape(desc)} In review.</p></td></tr>')
ADD = {
 'Orders and samples': [('Modify an order and the optional requesting provider', 'Modify an order and the optional requesting provider', 'Add tests to a saved order by search, tag or panel, and see when the requesting provider must be entered.')],
 'Results, validation and reports': [
   ('Report Print Queue: print and reprint patient reports', 'Report Print Queue: print and reprint patient reports', 'Print released patient reports, and reprint them when results are added or corrected.'),
   ('Sent Messages: check and resend deliveries', 'Sent Messages: check and resend deliveries', 'See every message the laboratory sent or tried to send, why one failed, and send it again.')],
 'PATHO': [('Record cassettes and slides on a pathology case', 'Record cassettes and slides on a pathology case', 'Give each cassette and slide of a pathology case its own identifier, with each slide linked to its block.')],
}
INV = [('Manage inventory items, lots, counts and reorders', 'Manage inventory items, lots, counts and reorders', 'See what is in stock and what to reorder, and keep items, lots, counts and usage up to date.'),
       ('Receive stock and run inventory reports', 'Receive stock and run inventory reports', 'Record a delivery lot by lot, and report on stock received, used, held or expiring.')]
heads = re.findall(r'<h3>(.*?)</h3>', s)
patho = next((h for h in heads if h.lower().startswith('pathology')), None)
if not patho: sys.exit('no pathology heading')
ADD[patho] = ADD.pop('PATHO')
changes = []
for h, rows in ADD.items():
    for (title, text, desc) in rows:
        if f'ri:content-title="{html.escape(title, quote=True)}"' in s: continue
        i = s.find(f'<h3>{h}</h3>')
        if i < 0: sys.exit('heading not found: ' + h)
        j = s.find('</tbody></table>', i)
        s = s[:j] + row(title, text, desc) + s[j:]; changes.append(f'{h}: + {title}')
if '<h3>Inventory</h3>' not in s:
    sec = ('<h3>Inventory</h3><p>Reagents and consumables: what is in stock, what to reorder, deliveries and reports. '
           '<a href="https://uwdigi.atlassian.net/wiki/spaces/oeg/folder/1729363970">Open the folder</a>.</p>'
           '<table data-layout="default"><tbody><tr><th><p>Page</p></th><th><p>What it helps you do</p></th></tr>'
           + ''.join(row(*r) for r in INV) + '</tbody></table>')
    i = s.find('<h3>Laboratory notebooks</h3>')
    if i < 0: sys.exit('no notebooks heading')
    s = s[:i] + sec + s[i:]; changes.append('Inventory section added')
if '—' in ''.join(changes): sys.exit('em dash')
print('\n'.join(changes))
if DRY or not changes: sys.exit(0)
r = pub.api(base, auth, 'PUT', f'/api/v2/pages/{PID}', {'id': PID, 'status': 'current', 'title': p['title'], 'parentId': p['parentId'],
    'body': {'representation': 'storage', 'value': s}, 'version': {'number': p['version']['number'] + 1, 'message': 'New 3.3.0 pages added (in review)'}})
print('landing v%d' % r['version']['number'])
