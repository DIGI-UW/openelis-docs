import importlib.util, sys, time
s=importlib.util.spec_from_file_location('pub','confluence-publish.py');p=importlib.util.module_from_spec(s);s.loader.exec_module(p)
b,a=p.load_creds(); pid='1680048163'
existing={}
for at in p.api(b,a,'GET','/rest/api/content/'+pid+'/child/attachment?limit=250')['results']: existing[at['title']]=at['id']
p.upload_attachment(b,a,pid,'qms-330/qc/qc330-dashboard.png',existing)
r=p.api(b,a,'GET','/rest/api/content/'+pid+'?expand=body.storage,version')
v=r['body']['storage']['value']
reps=[
('Written against pngtest.openelis-global.org, version 3.2.2.0, 27 September 2026.','Written against pngtest.openelis-global.org, version 3.2.2.0, 27 September 2026; dashboard re-checked on testing.openelis-global.org, 3.3.0-SNAPSHOT, 12 October 2026.'),
('<strong>Overall QC Pass Rate</strong>. <strong>Last Updated</strong> shows when the figures were read; <strong>Refresh</strong> and <strong>Export</strong> sit beside it.','<strong>% Instruments In Control</strong> (called Overall QC Pass Rate on 3.2.2.0). <strong>Last Updated</strong> shows when the figures were read; <strong>Refresh</strong> and <strong>Export</strong> sit beside it. <strong>Export</strong> opens <strong>Export QC Data</strong>, where you choose the <strong>Instrument</strong>, the <strong>Control Level</strong> (All levels by default) and a <strong>Start Date</strong> and <strong>End Date</strong>, then <strong>Export CSV</strong> or <strong>Export PDF</strong>. On the test server, with no instrument to choose, both export buttons were unavailable.'),
('ri:filename="01_qa_qc_dashboard.png"','ri:filename="qc330-dashboard.png"'),
('ac:alt="Figure 2. The QC Dashboard on its Instruments tab. This instance has no instruments connected, so the list is empty."','ac:alt="Figure 2. The QC Dashboard on its Instruments tab (3.3.0). This instance has no instruments connected, so the list is empty."'),
('<em>Figure 2. The QC Dashboard on its Instruments tab. This instance has no instruments connected, so the list is empty.</em>','<em>Figure 2. The QC Dashboard on its Instruments tab (3.3.0). This instance has no instruments connected, so the list is empty.</em>'),
('<tr><th><p>Reviewer</p></th>','<tr><th><p>Updated</p></th><td><p>12 October 2026 on testing.openelis-global.org, 3.3.0-SNAPSHOT: menu items and routes unchanged (QC Dashboard, QC Alerts, QC Lot Management, Rule Configuration, Reagent QC and Analyzer Manual QC still future features); the fourth tile is now % Instruments In Control; Export opens Export QC Data (observed, not exported: no instruments); Bench QC empty on testing (Figure 3 is from pngtest in September). Figure 2 recaptured.</p></td></tr><tr><th><p>Reviewer</p></th>'),
]
for o,n in reps:
    c=v.count(o); print(c, o[:50])
    assert c==1, o
    v=v.replace(o,n)
p.api(b,a,'PUT','/rest/api/content/'+pid,{'id':pid,'type':'page','title':r['title'],'version':{'number':r['version']['number']+1,'message':'3.3.0: tile renamed, Export QC Data, Figure 2 recaptured'},'body':{'storage':{'value':v,'representation':'storage'}}})
print('ok v', r['version']['number']+1)
