import json, shutil, copy
p = 'docs-manual/contracts.json'
shutil.copy(p, p + '.bak-20261013-330d')
c = json.load(open(p))
S = {s['id']: s for s in c['sections']}
log = []
def note(s, t):
    s['note'] = (s.get('note', '') + ' ' + t).strip()

o = S['organization-management']
o['retired'] = True; o['confluencePageId'] = '1705541782'
note(o, '13 Oct 2026: retired. The 3.2.x screen is gone in 3.3.0; its page text is kept as legacy copy 1705541782, and page 1437892659 now documents 3.3.0 (contract organization-management-330).')
S['organization-management-330']['confluencePageId'] = '1437892659'
S['organization-management-330']['manualDoc'] = 'Confluence 1437892659 (Admin: Manage organizations, merged from draft 1702756385 on 13 Oct 2026)'

ls = S['label-store-shared']
ls.update({'confluencePageId': '1428684802', 'capturedVersion': '3.3.0', 'title': 'Label and store environmental and vector samples',
           'routes': [{'path': '/order/environmental/enter', 'anchors': ['Add Environmental Order', 'Label & Store', 'Sample check']}]})
note(ls, '13 Oct 2026: clinical orders left this stage in 3.3.0 (Prepare samples); page rewritten for environmental and vector, driven on pngtest because testing has no environmental sample types. The Label & Store route redirects to Enter Order without an order, so the contract watches the stepper on Enter Order.')
qa = S['qa-review-shared']
qa.update({'confluencePageId': '1429176321', 'capturedVersion': '3.3.0', 'title': 'Complete the sample check for an environmental or vector order',
           'routes': [{'path': '/order/environmental/qa', 'anchors': ['Sample check', 'Intake Acceptance']}]})
note(qa, '13 Oct 2026: QA Review became Sample check in 3.3.0; page rewritten for environmental and vector orders.')

ql = S['qc-control-lot']
ql['capturedVersion'] = '3.3.0'
if not any(r['path'] == '/analyzers/qc/control-lots/new' for r in ql['routes']):
    ql['routes'].append({'path': '/analyzers/qc/control-lots/new', 'anchors': ['New Control Lot', 'Lot Number', 'Control Material', 'Statistics Configuration']})
note(ql, '13 Oct 2026: recaptured on testing 3.3.0 (lot 26541).')

if 'workplans' not in S:
    w = copy.deepcopy(ql)
    for k in list(w.keys()):
        if k not in ('base',): w.pop(k)
    w.update({'id': 'workplans', 'title': 'Print a work plan', 'confluencePageId': '272760837',
              'manualDoc': 'Confluence 272760837 (rewritten in place 13 Oct 2026; older text kept as 1705378043)',
              'capturedVersion': '3.3.0', 'base': 'https://testing.openelis-global.org',
              'routes': [
                  {'path': '/WorkPlanByTestSection?type=', 'anchors': ['Workplan By Unit', 'Unit Type']},
                  {'path': '/WorkPlanByTest?type=test', 'anchors': ['Workplan By Test', 'Test Type']},
                  {'path': '/WorkPlanByPanel?type=panel', 'anchors': ['Workplan By Panel', 'Panel Type']},
                  {'path': '/WorkPlanByPriority?type=priority', 'anchors': ['Workplan By Priority', 'Priority']}],
              'note': 'Batch Workplan (/Workplan) not documented: OGC-1200 in Backlog.'})
    c['sections'].append(w)
json.dump(c, open(p, 'w'), indent=2, ensure_ascii=False)
print('sections', len(c['sections']))
