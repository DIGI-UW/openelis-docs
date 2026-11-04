#!/usr/bin/env python3
"""Follow-up to contracts-330.py after the 12 Oct drift run."""
import json, os
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "contracts.json")
d = json.load(open(P)); S = {s["id"]: s for s in d["sections"]}
e = S["eqa-provider"]
for r in e["routes"]:
    if r["path"] == "/qa/eqa/management":
        r["anchors"] = [a for a in r["anchors"] if a != "System Settings"]
    if r["path"] == "/qa/eqa/participants":
        r["anchors"] = [a for a in r["anchors"] if a != "Select Program"]
e["routes"] = [r for r in e["routes"] if r["path"] != "/qa/eqa/provider/schemes/8/performance"]
e["notes"] += " 12 Oct 2026: System Settings (removed, OGC-1247) and Select Program (V1 wording) dropped; the scheme-8 performance route was pngtest seed data and is dropped until a testing scheme is picked."
c = S["clinical-order-enter"]
for r in c["routes"]:
    if r["path"] == "/order/clinical":
        r["path"] = "/order/clinical/collect"
c["notes"] += " 12 Oct 2026: /order/clinical now redirects to /order/clinical/collect; route repointed."
json.dump(d, open(P, "w"), indent=2, ensure_ascii=False)
print("ok")
