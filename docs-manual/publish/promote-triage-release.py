#!/usr/bin/env python3
"""2026-10-09: promote Triage and release results (1661763585) into the End User Manual folder
Results, validation and reports (1679589479), stamp provenance, label it, and list it on the
TOC page 1326972929 next to Validate and release results (1441202177). ADF in / ADF out, v2 API.
--dry-run prints without writing."""
import json, importlib.util, os, sys, copy
here = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("f", os.path.join(here, "fix-at-a-glance-headers.py"))
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
base, auth = m.load_creds()
DRY = "--dry-run" in sys.argv
PID, FOLDER, TOC = "1661763585", "1679589479", "1326972929"
WIKI = "https://uwdigi.atlassian.net/wiki/spaces/OG/pages/"
def T(t, *marks): 
    n = {"type": "text", "text": t}
    if marks: n["marks"] = list(marks)
    return n
def link(t, pid): return T(t, {"type": "link", "attrs": {"href": WIKI + pid}})
STRONG = {"type": "strong"}; EM = {"type": "em"}

def get(pid):
    p = m.api(base, auth, "GET", f"/api/v2/pages/{pid}?body-format=atlas_doc_format")
    if str(p["id"]) != pid: sys.exit(f"crossed read on {pid}")
    return p, json.loads(p["body"]["atlas_doc_format"]["value"])
def text(n): 
    return "".join(c.get("text", "") for c in n.get("content", []) or [] if isinstance(c, dict)) if isinstance(n, dict) else ""
def put(p, doc, extra=None, msg=""):
    body = {"id": p["id"], "status": "current", "title": p["title"],
            "body": {"representation": "atlas_doc_format", "value": json.dumps(doc)},
            "version": {"number": p["version"]["number"] + 1, "message": msg}}
    if extra: body.update(extra)
    if DRY: print("DRY put", p["id"], extra, msg); return
    r = m.api(base, auth, "PUT", f"/api/v2/pages/{p['id']}", body)
    print("put", r["id"], "v", r["version"]["number"], "parent", r.get("parentId"))

# 1. the page
p, doc = get(PID)
c = doc["content"]
done_stamp = done_tip = False
for i, n in enumerate(c):
    if n.get("type") == "paragraph" and text(n).startswith("Awaiting second-reviewer verification"):
        c[i] = {"type": "paragraph", "content": [
            T("Verified by", STRONG), T(" Casey B. Iiams-Hauser · "), T("Date", STRONG), T(" 2026-10-09 · "),
            T("Instance", STRONG), T(" testing.openelis-global.org · "), T("OpenELIS version", STRONG), T(" 3.3.0-SNAPSHOT")]}
        c.insert(i + 1, {"type": "paragraph", "content": [
            T("Gates applied: ☑ workflow sentence ☑ first real step ☑ step↔screenshot fidelity ☑ driven live end-to-end ☑ process gates. Promoted by the author on 2026-10-09 before the second review (OGC-1285) closed.", EM)]})
        done_stamp = True; break
def fix_tip(n):
    global done_tip
    if isinstance(n, dict):
        if n.get("type") == "paragraph" and text(n).startswith("Electronic signatures are a laboratory setting.") and "1242759175" not in json.dumps(n):
            n["content"] += [T(" How to turn them on is in "), link("Electronic Signatures", "1242759175"), T(".")]
            done_tip = True
        for x in n.get("content", []) or []: fix_tip(x)
fix_tip(doc)
print("stamp", done_stamp, "tip", done_tip)
if not done_stamp: sys.exit("stamp paragraph not found")
put(p, doc, {"parentId": FOLDER}, "Promoted to End User Manual: Results, validation and reports; provenance stamped")

# 2. labels
labels = [{"prefix": "global", "name": "doc-verified"}, {"prefix": "global", "name": "verified-v3-3-0"}]
if DRY: print("DRY labels", labels)
else: print("labels", [l["name"] for l in m.api(base, auth, "POST", f"/rest/api/content/{PID}/label", labels).get("results", [])])

# 3. TOC
p, doc = get(TOC)
s = json.dumps(doc)
if PID in s: print("TOC already lists the page"); sys.exit(0)
para = doc["content"][1]["content"][1]["content"][1]["content"][0]
assert text(para).startswith("Entering and resulting orders:") and "1441202177" in json.dumps(para), text(para)
k = [i for i, x in enumerate(para["content"]) if x.get("text") == " and "][-1]
para["content"][k] = T(", ")
para["content"][k + 1:k + 1] = [link("Triage and release results", PID), T(" and, for releases before 3.2.2, ")]
tbl = doc["content"][14]
row = tbl["content"][3]
assert "1441202177" in json.dumps(row)
new = copy.deepcopy(row)
new["content"][0]["content"][0]["content"] = [link("Triage and release results", PID)]
new["content"][1]["content"][0]["content"] = [T("Work through the validation queue, release clear results in one action, and correct or retest the rest. OpenELIS 3.2.2 and later.")]
row["content"][1]["content"][0]["content"] = [T("Review entered results and release them, or send them back for retesting. Releases before 3.2.2.")]
tbl["content"].insert(3, new)
print("TOC para:", text(para))
put(p, doc, None, "Add Triage and release results (1661763585) next to Validate and release results")
