#!/usr/bin/env python3
"""Close-out of the 3.3.0 manual update (12 Oct 2026): rebaseline and register contracts."""
import json, shutil, os
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "contracts.json")
shutil.copy(P, P + ".bak-20261012-pre-330-closeout")
d = json.load(open(P))
S = {s["id"]: s for s in d["sections"]}
DATE = "2026-10-12"
T = "https://testing.openelis-global.org"

def bump(sid, **kw):
    s = S[sid]
    s["capturedVersion"] = "3.3.0"; s["capturedDate"] = DATE
    s.update(kw)
    return s

bump("electronic-signatures", confluencePageId="1242759175",
     routes=[{"path": "/validation", "anchors": ["Lab Unit", "Search by patient", "Load results"]},
             {"path": "/qa/qms/e-signature-log", "anchors": ["Electronic Signature Log", "Subject Type", "Apply Filters", "Export CSV", "Export PDF", "Signed At", "Signer"]}],
     notes="3.3.0: validation routes merged into /validation; signature dialogs only render while signing, so on-load anchors cover the validation search and the Electronic Signature Log (OGC-703). Rewritten 12 Oct 2026; 3.2.x copy 1706917975.")
bump("register-new-patient", confluencePageId="1440841760",
     routes=[{"path": "/PatientManagement", "anchors": ["Add Or Modify Patient", "New Patient", "National ID", "Sex"]}],
     notes="3.3.0: Gender renamed Sex.")
bump("patient-management", confluencePageId="1441136648")
bump("admin-sample-type-management", title="Admin: Sample Type Management",
     routes=[{"path": "/MasterListsPage/SampleTypeEditor", "anchors": ["Sample Type Editor", "Add Sample Type", "Filter by domain", "Search sample types"]}],
     notes="3.3.0: /MasterListsPage/SampleTypeManagement opens the Sample Type Editor; the legacy page 1420853278 carries a note.")
g = bump("general-configurations")
for r in g["routes"]:
    if r["path"] == "/MasterListsPage/ResultConfigurationMenu":
        r["anchors"] = ["Result Entry Configuration", "Modify", "Value", "qcFailBlocksValidation", "allowBulkReleaseClear"]
    if r["path"] == "/MasterListsPage/SampleEntryConfigurationMenu":
        r["anchors"] = ["Order Entry Configuration", "Modify", "Value", "eqaEnabled", "validateAccessionNumber", "Patient sex required", "Patient age required"]
g["notes"] = g.get("notes", "") + " 3.3.0 (12 Oct 2026): resultsEntryUnifiedRoute removed; new settings marked on the page."
r = bump("results-entry", confluencePageId="1439072277", manualDoc="Confluence 1439072277 (live)")
r.pop("configToggle", None)
r["notes"] = "3.3.0: /Results is the only results entry route. Rewritten 12 Oct 2026; 3.2.x copy 1705083137."
for sid in ("eqa-provider", "eqa-participant"):
    e = bump(sid)
    e["notes"] = e["notes"] + " 12 Oct 2026: re-verified on pngtest 3.3.0-SNAPSHOT (EQA V2 now also on testing, with QA-named seed data)."
q = bump("qc-overview", title="Statistical QC: overview and daily review")
q["routes"][0]["anchors"] = ["Quality Control Dashboard", "Instruments In Control", "Out of Control", "% Instruments In Control", "Instruments", "Bench QC"]
a = bump("analyzer-mapping-qc")
a["routes"][0]["anchors"] = [x if x != "Overall QC Pass Rate" else "% Instruments In Control" for x in a["routes"][0]["anchors"]]
S["organization-management-330"]["capturedVersion"] = "3.3.0"

NEW = [
 {"id": "label-presets", "title": "Manage label presets", "confluencePageId": "1433468931", "manualDoc": "Confluence 1433468931 (live)",
  "captureSpec": "tests/docs/lp-probe.docs.spec.ts", "jiraEpic": "", "featureDoc": "OGC-1217, OGC-1218", "base": T,
  "routes": [{"path": "/MasterListsPage/labelPresets", "anchors": ["Label Presets", "Site-wide Barcode Settings", "Pre-printed label numbers come from", "A separate pre-printed series", "Add Preset", "Barcode Type", "Dimensions", "Scope"]}],
  "uiPaths": ["frontend/src/components/admin/labelPresets"]},
 {"id": "locations-import-export", "title": "Admin: Import and export locations (3.3.0)", "confluencePageId": "1706295354", "manualDoc": "Confluence 1706295354 (draft)",
  "captureSpec": "tests/docs/loc-import-explore.docs.spec.ts", "jiraEpic": "OGC-1363", "featureDoc": "OGC-1414", "base": T,
  "routes": [{"path": "/MasterListsPage/locations/import", "anchors": ["Import / Export", "Download template", "Add & update", "Replace", "Preview", "Recent imports"]}], "uiPaths": []},
 {"id": "geographic-areas", "title": "Admin: Manage geographic areas (3.3.0)", "confluencePageId": "1706524697", "manualDoc": "Confluence 1706524697 (draft)",
  "captureSpec": "tests/docs/loc-cap.docs.spec.ts", "jiraEpic": "OGC-1363", "featureDoc": "OGC-1414", "base": T,
  "routes": [{"path": "/MasterListsPage/locations/areas", "anchors": ["Geographic Areas", "Search areas by name or code", "Expand all", "Collapse all", "Add Region", "Child areas"]}], "uiPaths": []},
 {"id": "sampling-sites", "title": "Admin: Manage sampling sites (3.3.0)", "confluencePageId": "1705083175", "manualDoc": "Confluence 1705083175 (draft)",
  "captureSpec": "tests/docs/loc-site.docs.spec.ts", "jiraEpic": "OGC-1363", "featureDoc": "OGC-1414", "base": T,
  "routes": [{"path": "/MasterListsPage/locations/sites", "anchors": ["Sampling Sites", "Organization or sampling site: which do I need?", "Location (includes areas beneath)", "Site type", "In use"]}], "uiPaths": []},
 {"id": "test-accreditation", "title": "QMS: Test accreditation and report logos (3.3.0)", "confluencePageId": "1705246900", "manualDoc": "Confluence 1705246900 (draft)",
  "captureSpec": "scratch/qms-330 (interactive driver)", "jiraEpic": "", "featureDoc": "OGC-720", "base": T,
  "routes": [{"path": "/qa/qms/accreditation", "anchors": ["Test Accreditation", "Accrediting Bodies", "Add body", "Enrolled Tests", "Enroll tests", "EQA Coverage of Accredited Scope"]}], "uiPaths": []},
 {"id": "custom-data-export", "title": "Reports: Custom Data Export and My Report Queue (3.3.0)", "confluencePageId": "1707704440", "manualDoc": "Confluence 1707704440 (draft)",
  "captureSpec": "scratch/qms-330 (interactive driver)", "jiraEpic": "", "featureDoc": "OGC-479, OGC-481, OGC-483", "base": T,
  "routes": [{"path": "/reports/custom-data-export", "anchors": ["Custom Data Export", "My Report Queue", "Create a new export", "Start a new export", "Use a saved report"]}], "uiPaths": [],
  "notes": "Every export on testing returned 0 rows at capture (comment on OGC-479)."},
]
for n in NEW:
    n["capturedVersion"] = "3.3.0"; n["capturedDate"] = DATE
    if n["id"] in S:
        raise SystemExit("duplicate id " + n["id"])
    d["sections"].append(n)
json.dump(d, open(P, "w"), indent=2, ensure_ascii=False)
print("sections", len(d["sections"]))
