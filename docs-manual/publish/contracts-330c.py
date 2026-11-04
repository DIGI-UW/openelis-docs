#!/usr/bin/env python3
"""Round 2 (13 Oct 2026): analyzer pages, Bridge pairing, Alerts Dashboard."""
import json, os, shutil
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "contracts.json")
shutil.copy(P, P + ".bak-20261013-pre-round2")
d = json.load(open(P)); S = {s["id"]: s for s in d["sections"]}
T = "https://testing.openelis-global.org"; DATE = "2026-10-13"
a = S["analyzer-setup"]
a.update(capturedVersion="3.3.0", capturedDate=DATE, confluencePageId="1648361491",
  routes=[{"path": "/analyzers", "anchors": ["Analysers", "Add Analyser", "Paired with the Analyzer Bridge", "Total analysers", "In setup", "Needs attention"]},
          {"path": "/analyzers?setup=instrument", "anchors": ["Set up a new analyser", "Analyser type", "Analyser name", "Lab units", "Continue to Assays", "Instrument not listed?"]},
          {"path": "/analyzers/types", "anchors": ["Analyser Types", "The reusable setups behind your analysers", "Duplicate Profile", "Create Profile", "Mapping status"]}],
  notes="13 Oct 2026: rewritten for 3.3.0 on paired testing (four-step wizard, per-analyser mapping). 3.2.2.0 copy 1708425232.")
m = S["analyzer-mapping-qc"]
m["capturedDate"] = DATE
m["routes"] = [r for r in m["routes"] if not r["path"].startswith("/analyzers/")] + [
  {"path": "/analyzers/6/mapping", "anchors": ["This analyzer's own mapping", "Apply mappings and retry held results", "Test and result mappings", "Control result recognition"]}]
m["notes"] = m.get("notes", "") + " 13 Oct 2026: Part 1 rewritten for per-analyser mappings; route /analyzers/6/mapping is the seed analyser GeneXpert IV 803456 (TB lab) on testing. 3.2.2.0 copy 1708818439."
NEW = [
 {"id": "analyzer-bridge-install", "title": "Install the Analyzer Bridge", "confluencePageId": "1669758983", "manualDoc": "Confluence 1669758983 (draft)",
  "captureSpec": "scratch/qms-330 (interactive driver)", "jiraEpic": "OGC-1054", "featureDoc": "", "base": T,
  "routes": [{"path": "/analyzers", "anchors": ["Paired with the Analyzer Bridge", "Pair again"]}], "uiPaths": ["frontend/src/components/analyzers"],
  "notes": "Pairing panel only; the rest of the page is Bridge-side. 3.2.x/Bridge 3.3.0 password version kept at 1708720130."},
 {"id": "alerts-dashboard", "title": "Review and act on alerts (3.3.0)", "confluencePageId": "1705377997", "manualDoc": "Confluence 1705377997 (draft)",
  "captureSpec": "scratch/qms-330 (interactive driver)", "jiraEpic": "", "featureDoc": "OGC-1372", "base": T,
  "routes": [{"path": "/Alerts", "anchors": ["Alerts Dashboard", "Critical Alerts", "EQA Deadlines", "Overdue STAT Orders", "Samples Expiring", "Alert Type", "EQA Deadline Summary"]}], "uiPaths": []},
]
for n in NEW:
    assert n["id"] not in S
    n["capturedVersion"] = "3.3.0"; n["capturedDate"] = DATE
    d["sections"].append(n)
json.dump(d, open(P, "w"), indent=2, ensure_ascii=False)
print("sections", len(d["sections"]))
