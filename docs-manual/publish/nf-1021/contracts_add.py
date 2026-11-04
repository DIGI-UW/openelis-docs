import json, os, shutil
P = os.path.expanduser('~/Documents/OpenELIS QA/docs-manual/contracts.json')
shutil.copy(P, P + '.bak-20261021')
d = json.load(open(P)); S = d['sections']
T = 'https://testing.openelis-global.org'; PNG = 'https://pngtest.openelis-global.org'
new = [
 {'id': 'report-print-queue', 'title': 'Report Print Queue: print and reprint patient reports', 'confluencePageId': '1729429517',
  'manualDoc': 'Confluence 1729429517', 'captureSpec': 'tests/docs/rpq-330-manual-r2.docs.spec.ts', 'jiraEpic': 'OGC-1031', 'featureDoc': 'OGC-431',
  'base': T, 'capturedVersion': '3.3.0', 'capturedDate': '2026-10-21',
  'routes': [{'path': '/ReportPrintQueue', 'anchors': ['Report Print Queue', 'To print', 'Amended to print', 'Lab Number', 'Range', 'Search by patient', 'Print status', 'Time window', 'Facility', 'Requester', 'Released / Submitted']}]},
 {'id': 'sent-messages', 'title': 'Sent Messages: check and resend deliveries', 'confluencePageId': '1729724423',
  'manualDoc': 'Confluence 1729724423', 'captureSpec': 'tests/docs/rpq-330-manual-r2.docs.spec.ts', 'featureDoc': 'OGC-439',
  'base': T, 'capturedVersion': '3.3.0', 'capturedDate': '2026-10-21',
  'routes': [{'path': '/SentMessages', 'anchors': ['Sent Messages', 'Product', 'Status', 'Channel', 'Lab Number', 'Recipient', 'Attempts', 'Sent by']},
             {'path': '/MasterListsPage/notificationTriggerConfig/channels', 'anchors': ['Channels', 'Delivery Settings', 'Send test']}]},
 {'id': 'modify-order-requester', 'title': 'Modify an order and the optional requesting provider', 'confluencePageId': '1729462279',
  'manualDoc': 'Confluence 1729462279', 'captureSpec': 'tests/docs/rpq-330-manual-r2.docs.spec.ts', 'featureDoc': 'OGC-1514; OGC-1143',
  'base': T, 'capturedVersion': '3.3.0', 'capturedDate': '2026-10-21',
  'routes': [{'path': '/SampleEdit', 'anchors': ['Modify Order', 'Search By Accession Number', 'Search By Patient']},
             {'path': '/MasterListsPage/SampleEntryConfigurationMenu', 'anchors': ['Order Entry Configuration', 'requesterRequired']},
             {'path': '/order/clinical/enter', 'anchors': ['Enter Order', 'Site Search', 'Site Name', 'Provider Search']}]},
 {'id': 'pathology-cassettes-slides', 'title': 'Record cassettes and slides on a pathology case', 'confluencePageId': '1729560592',
  'manualDoc': 'Confluence 1729560592', 'captureSpec': 'tests/docs/rpq-330-manual-r2.docs.spec.ts', 'featureDoc': 'OGC-264',
  'base': T, 'capturedVersion': '3.3.0', 'capturedDate': '2026-10-21',
  'routes': [{'path': '/PathologyDashboard', 'anchors': ['Pathology', 'Cases in Progress']}]},
 {'id': 'inventory-items', 'title': 'Manage inventory items, lots, counts and reorders', 'confluencePageId': '1729134594',
  'manualDoc': 'Confluence 1729134594', 'captureSpec': 'tests/docs/inventory-330-manual.docs.spec.ts', 'jiraEpic': 'OGC-438',
  'base': T, 'capturedVersion': '3.3.0', 'capturedDate': '2026-10-21',
  'routes': [{'path': '/inventory', 'anchors': ['Items', 'What you have and what to reorder', 'Filter by Status', 'Filter by Location', 'Filter by Tags', 'New item', 'Count mode', 'Manage tags', 'Import items', 'Log usage']}]},
 {'id': 'inventory-receive-reports', 'title': 'Receive stock and run inventory reports', 'confluencePageId': '1729167388',
  'manualDoc': 'Confluence 1729167388', 'captureSpec': 'tests/docs/inventory-330-manual.docs.spec.ts', 'jiraEpic': 'OGC-438',
  'base': T, 'capturedVersion': '3.3.0', 'capturedDate': '2026-10-21',
  'routes': [{'path': '/inventory/receive', 'anchors': ['Receive', 'Scan the box', 'Item Name', 'Lot Number', 'Expiration Date', 'Current Quantity', 'Add to delivery']},
             {'path': '/inventory/reports', 'anchors': ['Reports', 'Report Type', 'Run report', 'Export Format', 'Export']}]},
 {'id': 'microbiology-v2', 'title': 'Microbiology (pre-release): work a case from culture to release', 'confluencePageId': '1729789973',
  'manualDoc': 'Confluence 1729789973 (with 1729167362 admin and 1729331248 WHONET, review area)', 'captureSpec': 'tests/docs/amr-v2-manual.docs.spec.ts', 'jiraEpic': 'OGC-1383',
  'base': PNG, 'capturedVersion': '3.3.0-SNAPSHOT (Microbiology V2 pre-release stack)', 'capturedDate': '2026-10-21',
  'routes': [{'path': '/Microbiology/worklist', 'anchors': ['Microbiology worklist', 'AST runs']}],
  'note': 'Pre-release: pngtest only. Re-point base to testing once Microbiology V2 is merged.'},
]
have = {s['id'] for s in S}
for n in new:
    if n['id'] in have: print('skip', n['id']); continue
    S.append(n); print('added', n['id'])
json.dump(d, open(P, 'w'), indent=1, ensure_ascii=False)
