import json, shutil
p = '/Users/casey/Documents/OpenELIS QA/docs-manual/contracts.json'
shutil.copy(p, p + '.bak-20260927-pre-qc')
d = json.load(open(p)); c = d['sections']
new = [
 {"id": "qc-control-lot", "title": "Receive and activate a control lot", "confluencePageId": "1680048146",
  "manualDoc": "Confluence 1680048146 (draft under 1189609473)", "captures": "docs-media/qc-png-drive (4 figures)",
  "base": "https://pngtest.openelis-global.org", "capturedVersion": "3.2.2.0", "capturedDate": "2026-09-27",
  "jiraEpic": "OGC-682", "featureDoc": "OGC-1213", "frs": "pending", "captureSpec": "tests/docs/qc-png-drive.docs.spec.ts",
  "routes": [{"path": "/qa/qc/control-lots", "anchors": ["New Control Lot", "Lot Number", "Control Material", "Control Level", "Calculation Method", "Expiration Date"]}]},
 {"id": "qc-overview", "title": "Statistical QC — overview and daily review", "confluencePageId": "1680048163",
  "manualDoc": "Confluence 1680048163 (draft under 1189609473)", "captures": "docs-media/qc-png-explore + qc-png-drive (4 figures)",
  "base": "https://pngtest.openelis-global.org", "capturedVersion": "3.2.2.0", "capturedDate": "2026-09-27",
  "jiraEpic": "OGC-682", "featureDoc": "OGC-1213", "frs": "pending", "captureSpec": "tests/docs/qc-png-explore.docs.spec.ts",
  "routes": [{"path": "/qa/qc/dashboard", "anchors": ["Quality Control Dashboard", "Instruments In Control", "Out of Control", "Overall QC Pass Rate", "Instruments", "Alerts", "Bench QC"]},
             {"path": "/qa/qc/rule-config", "anchors": ["Configured Rule Sets", "Analyzer", "Enabled Rules"]}]}]
ids = {x['id'] for x in c}
for n in new:
    if n['id'] in ids:
        print('exists, replacing', n['id']); c[:] = [x for x in c if x['id'] != n['id']]
    c.append(n)
json.dump(d, open(p, 'w'), indent=2, ensure_ascii=False)
print('sections', len(c))
