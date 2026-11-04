import json, shutil
p = '/Users/casey/Documents/OpenELIS QA/docs-manual/contracts.json'
shutil.copy(p, p + '.bak-20260927-pre-programs')
d = json.load(open(p))
c = d['sections']
old = [x for x in c if x['id'] == 'program-entry']
print('program-entry', json.dumps(old[0])[:400] if old else None)
if not any(x['id'] == 'programs-v2' for x in c):
    c.append({"id": "programs-v2", "title": "Admin — Define programs and their questionnaires",
      "confluencePageId": "1679949842", "manualDoc": "Confluence 1679949842 (draft under 1189609473); replaces 1439006727 on promotion",
      "captures": "docs-media/programs-v2 (8 figures)", "base": "https://testing.openelis-global.org",
      "capturedVersion": "3.2.3.0", "capturedDate": "2026-09-27", "jiraEpic": "OGC-781", "featureDoc": "OGC-1236",
      "frs": "https://github.com/DIGI-UW/openelis-work/blob/main/designs/admin-config/programs-management.md",
      "captureSpec": "tests/docs/programs-v2.docs.spec.ts",
      "routes": [{"path": "/MasterListsPage/program", "anchors": ["Programs", "Add Program", "Show deactivated", "Name", "Domain", "Status", "Lab unit(s)"]}]})
json.dump(d, open(p, 'w'), indent=2, ensure_ascii=False)
print('sections', len(c))
