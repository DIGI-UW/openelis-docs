import json, os, shutil, sys, re, html, importlib.util
ROOT = os.path.expanduser('~/Documents/OpenELIS QA/docs-manual')
P = os.path.join(ROOT, 'contracts.json')
shutil.copy(P, P + '.bak-20261022')
d = json.load(open(P)); S = d['sections']; byid = {s['id']: s for s in S}
T = 'https://testing.openelis-global.org'
new = [
 {"id":"qa-overview-qi","title":"QA Overview and quality indicators","confluencePageId":"1732739133","manualDoc":"Confluence 1732739133","captureSpec":"tests/docs/qa2-capture.docs.spec.ts","jiraEpic":"OGC-683; OGC-685","featureDoc":"OGC-1566; OGC-1567","base":T,"capturedVersion":"3.3.0","capturedDate":"2026-10-22","routes":[{"path":"/qa/overview","anchors":["QA Overview","ATTENTION REQUIRED","TODAY","THIS WEEK","PILLAR STATUS","RECENT ACTIVITY"]},{"path":"/qa/qi/dashboard","anchors":["QI Dashboard","Reporting window","Average TAT","Rejection Rate","Amendment Rate","NCE Pulse"]},{"path":"/qa/qi/config","anchors":["QI Configuration","Indicator","Enabled","Target","Action threshold","Overrides"]}]},
 {"id":"capa-register","title":"Record corrective and preventive actions and use the CAPA Register","confluencePageId":"1733001264","manualDoc":"Confluence 1733001264","captureSpec":"tests/docs/qa2-capture.docs.spec.ts; tests/docs/qa2-fix.docs.spec.ts","jiraEpic":"OGC-685; OGC-312","featureDoc":"OGC-1567; OGC-1568","base":T,"capturedVersion":"3.3.0","capturedDate":"2026-10-22","routes":[{"path":"/qa/qms/capa-register","anchors":["CAPA Register","Open","Overdue","Due This Week","Completed (90d)","Person Responsible"]},{"path":"/NCECorrectiveAction","anchors":["Nonconforming Events Corrective Action","Search By","Text Value","Search"]}]},
 {"id":"eqa-in-house-blinding","title":"Run an in-house blinded EQA panel","confluencePageId":"1733886070","manualDoc":"Confluence 1733886070","captureSpec":"tests/docs/qa2-capture.docs.spec.ts","jiraEpic":"OGC-608","featureDoc":"OGC-1235","base":T,"capturedVersion":"3.3.0","capturedDate":"2026-10-22","routes":[{"path":"/qa/eqa/in-house","anchors":["In-House Blinding","In-house scheme","Launch blinding wizard","EQA material panel"]},{"path":"/qa/eqa/in-house/new","anchors":["Create in-house blinded panel","Scheme & cycle","Samples & prep","Analysts","Confirm & seal"]}]},
 {"id":"notifications-admin","title":"Admin: Set up notification triggers, templates, channels and delivery","confluencePageId":"1734017045","manualDoc":"Confluence 1734017045","captureSpec":"tests/docs/gapsb-*.docs.spec.ts","jiraEpic":"OGC-1506","featureDoc":"OGC-1557","base":T,"capturedVersion":"3.3.0","capturedDate":"2026-10-22","routes":[{"path":"/MasterListsPage/notificationTriggerConfig/triggers","anchors":["Notifications","Active Triggers","Save Configuration"]},{"path":"/MasterListsPage/notificationTriggerConfig/templates","anchors":["Notification Template Configuration","Available Merge Fields","Save Template"]},{"path":"/MasterListsPage/notificationTriggerConfig/channels","anchors":["Channels","Send test","Edit"]},{"path":"/MasterListsPage/notificationTriggerConfig/delivery","anchors":["Delivery Settings","Lab contact line","Default country code"]}]},
 {"id":"printed-report-header","title":"Admin: Set the patient report header (Printed Report Configuration)","confluencePageId":"1732739089","manualDoc":"Confluence 1732739089","captureSpec":"tests/docs/gapsb-*.docs.spec.ts","jiraEpic":"OGC-1111","featureDoc":"OGC-1556","base":T,"capturedVersion":"3.3.0","capturedDate":"2026-10-22","routes":[{"path":"/MasterListsPage/PrintedReportsConfigurationMenu","anchors":["Printed Report Configuration","SiteName","headerLeftImage","Modify"]}]},
]
for n in new:
    if n['id'] in byid: print('skip', n['id']); continue
    S.append(n); print('added', n['id'])
inv = byid['inventory-items']
if not any(r['path'] == '/Alerts' for r in inv['routes']):
    inv['routes'].append({"path": "/Alerts", "anchors": ["Alerts Dashboard", "Alert Type"]}); print('inventory-items + /Alerts')
inv['capturedDate'] = '2026-10-22'
mic = byid['microbiology-v2']
for r in [{"path":"/MasterListsPage/program","anchors":["Programs","Add Program","Show deactivated"]},
          {"path":"/MasterListsPage/MicrobiologyReference/dst-bindings","anchors":["Molecular resistance mappings","Add mapping"]},
          {"path":"/MasterListsPage/MicrobiologyReference/patient-origins","anchors":["Patient origins","WHONET code"]},
          {"path":"/Microbiology/whonet","anchors":["WHONET export","Configure","Preview","Generate"]}]:
    if not any(x['path'] == r['path'] for x in mic['routes']):
        mic['routes'].append(r); print('micro +', r['path'])
mic['capturedDate'] = '2026-10-22'
json.dump(d, open(P, 'w'), indent=1, ensure_ascii=False)

# landing page rows
spec = importlib.util.spec_from_file_location('pub', os.path.join(ROOT, 'publish', 'confluence-publish.py'))
pub = importlib.util.module_from_spec(spec); spec.loader.exec_module(pub)
b, a = pub.load_creds()
PID = '1326972929'
p = pub.api(b, a, 'GET', f'/api/v2/pages/{PID}?body-format=storage')
if str(p['id']) != PID: sys.exit('crossed read')
s = p['body']['storage']['value']
def row(title, desc):
    t = html.escape(title, quote=True)
    return (f'<tr><td><p><ac:link><ri:page ri:content-title="{t}" /><ac:link-body>{html.escape(title)}</ac:link-body></ac:link></p></td>'
            f'<td><p>{html.escape(desc)} In review.</p></td></tr>')
ADD = {
 'Quality assurance': [
  ('QA Overview and quality indicators', 'See what needs attention today and track turnaround, rejection, amendment and NCE indicators against your targets.'),
  ('Record corrective and preventive actions and use the CAPA Register', 'Record what was done about a non-conforming event and follow every open action to completion.'),
  ('Run an in-house blinded EQA panel', 'Send blinded samples through routine testing to check analysts and methods within your own laboratory.')],
 'Programs, rules and notifications': [
  ('Admin: Set up notification triggers, templates, channels and delivery', 'Choose which events send messages, word the messages, and set up email, SMS and WhatsApp.')],
 'Site and system settings': [
  ('Admin: Set the patient report header (Printed Report Configuration)', 'Put your laboratory name and logo at the top of the printed patient report.')],
}
ch = []
for h, rows in ADD.items():
    for title, desc in rows:
        if f'ri:content-title="{html.escape(title, quote=True)}"' in s: continue
        i = s.find(f'<h3>{h}</h3>')
        if i < 0: sys.exit('heading not found ' + h)
        j = s.find('</tbody></table>', i)
        s = s[:j] + row(title, desc) + s[j:]; ch.append(f'{h}: + {title}')
if '—' in ''.join(ch): sys.exit('em dash')
print('\n'.join(ch))
if ch:
    r = pub.api(b, a, 'PUT', f'/api/v2/pages/{PID}', {'id': PID, 'status': 'current', 'title': p['title'], 'parentId': p['parentId'],
        'body': {'representation': 'storage', 'value': s}, 'version': {'number': p['version']['number'] + 1, 'message': 'QA, notifications and report header pages added (in review)'}})
    print('landing v%d' % r['version']['number'])
# verify new pages
for pid in ['1732739133', '1733001264', '1733886070', '1734017045', '1732739089', '1729134594', '1729167388', '1729429517', '1729724423', '1729167362', '1729789973', '1729331248']:
    q = pub.api(b, a, 'GET', f'/api/v2/pages/{pid}?body-format=storage')
    body = q['body']['storage']['value']
    labels = [l['name'] for l in pub.api(b, a, 'GET', f'/rest/api/content/{pid}/label').get('results', [])]
    print(pid, q['title'][:55], 'v', q['version']['number'], 'parent', q.get('parentId'), 'imgs', body.count('<ac:image'), 'tok', body.count('{{IMG'), 'em', body.count('—'), labels)
