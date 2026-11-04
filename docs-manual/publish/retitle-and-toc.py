#!/usr/bin/env python3
"""2026-09-17 follow-up to the promotion: retitle the 22 pages per the style guide, update the
landing page (1326972929) list text to match, and remove the promoted pages from the review
queue (1189609473). All ADF round trips via the v2 API. --dry-run prints without writing."""
import json, importlib.util, os, sys, urllib.parse
here = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("f", os.path.join(here, "fix-at-a-glance-headers.py"))
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
base, auth = m.load_creds()
DRY = "--dry-run" in sys.argv

RENAMES = {
    "1439432709": ("Site Information", "Admin — Configure site information"),
    "1439367188": ("Application Properties", "Admin — Edit application properties"),
    "1439137808": ("Reflex Testing", "Admin — Define reflex testing rules"),
    "1438842886": ("Calculated Value Tests", "Admin — Define calculated value tests"),
    "1439006727": ("Program Entry", "Admin — Define programs"),
    "1439596548": ("Result Reporting Configuration", "Admin — Configure result reporting to external systems"),
    "1438973976": ("Dictionary Menu", "Admin — Manage dictionary entries"),
    "1439170565": ("Lab Number Management", "Admin — Choose the lab number format"),
    "1437892659": ("Organization Management", "Admin — Manage organizations"),
    "1439203334": ("Provider Management", "Admin — Manage providers"),
    "1439072261": ("Test Notification Configuration", "Admin — Configure test notifications"),
    "1439334404": ("Calendar Management", "Admin — Manage non-working days"),
    "1438973960": ("Search Index Management", "Admin — Rebuild the search index"),
    "1438908431": ("Logging Configuration", "Admin — Configure logging"),
    "1160282114": ("Menu Configuration", "Admin — Configure the navigation menu"),
    "1187840003": ("User Management", "Admin — Manage user accounts"),
    "1439072277": ("Results Entry", "Enter and save results"),
    "1441202177": ("Validation", "Validate and release results"),
    "1440350210": ("Order Search & Lookup", "Find an existing order"),
    "1440677908": ("Sample Storage", "Track sample storage and disposal"),
    "1440940035": ("Aliquot Management", "Create aliquots from a sample"),
    "1440841744": ("Running Reports", "Run reports"),
}
PROMOTED = set(RENAMES) | {"1439694850", "1439367205"}

def get(pid):
    p = m.api(base, auth, "GET", f"/api/v2/pages/{pid}?body-format=atlas_doc_format")
    return p, json.loads(p["body"]["atlas_doc_format"]["value"])

def put(pid, p, adf, title, msg):
    if DRY:
        print(f"  DRY {pid}: would write title={title!r}"); return
    r = m.api(base, auth, "PUT", f"/api/v2/pages/{pid}", {
        "id": pid, "status": p["status"], "title": title,
        "body": {"representation": "atlas_doc_format", "value": json.dumps(adf)},
        "version": {"number": p["version"]["number"] + 1, "message": msg}})
    print(f"  {pid}: v{p['version']['number']} -> v{r['version']['number']} {title!r}")

def link_pid(node):
    for mk in node.get("marks", []) or []:
        if mk.get("type") == "link":
            h = mk["attrs"].get("href", "")
            if "/pages/" in h: return h.split("/pages/")[1].split("/")[0].split("?")[0]
    return None

def walk(n, fn):
    if isinstance(n, dict):
        fn(n)
        for c in n.get("content", []) or []: walk(c, fn)
    elif isinstance(n, list):
        for c in n: walk(c, fn)

def item_pids(li):
    out = set()
    def f(n):
        if n.get("type") == "text":
            pid = link_pid(n)
            if pid: out.add(pid)
        if n.get("type") == "inlineCard":
            u = n["attrs"].get("url", "")
            if "/pages/" in u: out.add(u.split("/pages/")[1].split("/")[0])
    walk(li, f); return out

# 1. retitle
print("== retitle")
for pid, (old, new) in RENAMES.items():
    p, adf = get(pid)
    if p["title"] == new:
        print(f"  {pid}: already {new!r}"); continue
    put(pid, p, adf, new, "Retitled per user manual style guide (sentence case, verb-first, Admin prefix)")

# 2. landing page: link text -> new title
print("== landing page 1326972929")
p, adf = get("1326972929")
n_changed = [0]
def fix_text(n):
    if n.get("type") == "text":
        pid = link_pid(n)
        if pid in RENAMES and n["text"].strip().lower() == RENAMES[pid][0].lower():
            n["text"] = RENAMES[pid][1]; n_changed[0] += 1
walk(adf, fix_text)
print("  link texts updated:", n_changed[0])
put("1326972929", p, adf, p["title"], "Reading-list titles aligned with renamed pages")

# 3. queue page
print("== queue page 1189609473")
p, adf = get("1189609473")
blocks = adf["content"]
# 3a. label name
def fix_label(n):
    if n.get("type") == "text" and "verified-v3.2.1" in n["text"]:
        n["text"] = n["text"].replace("verified-v3.2.1", "verified-v3-2-1")
walk(adf, fix_label)
# 3b. drop promoted items from every bullet list; collect empties
removed = 0
for b in blocks:
    if b.get("type") == "bulletList":
        keep = [li for li in b["content"] if not (item_pids(li) & PROMOTED)]
        removed += len(b["content"]) - len(keep); b["content"] = keep
print("  queue items removed:", removed)
# 3c. rewrite the admin section (heading + paragraph + now-empty list) and the end-user heading
def para(text): return {"type": "paragraph", "content": [{"type": "text", "text": text}]}
def heading(text, level=3): return {"type": "heading", "attrs": {"level": level}, "content": [{"type": "text", "text": text}]}
new_blocks = []
i = 0
while i < len(blocks):
    b = blocks[i]; t = m.cell_text(b)
    if b.get("type") == "heading" and t.startswith("Administrator configuration"):
        new_blocks.append(heading("Administrator configuration — promoted 16 September 2026"))
        new_blocks.append(para("All sixteen drafts were verified under OGC-1165 / OGC-1106 / OGC-1109 and now live in the Administrator Guide folder (257458193) with doc-verified and verified-v3-2-1 labels, retitled per the style guide. Menu Configuration and User Management were merged into the pre-existing pages 1160282114 and 1187840003; the two superseded review copies can be deleted."))
        i += 1
        while i < len(blocks) and blocks[i].get("type") in ("paragraph", "bulletList"): i += 1
        continue
    if b.get("type") == "heading" and t.startswith("End-user workflows"):
        new_blocks.append(heading("End-user workflows — 3 drafts remaining · owned by OGC-1166"))
        new_blocks.append(para("Six of the nine (Results Entry, Validation, Order Search & Lookup, Sample Storage, Aliquot Management, Running Reports) were verified under OGC-1107 and promoted to the End User Manual folder (1329758211) on 16 September 2026, retitled per the style guide. The three below remain."))
        i += 1
        if i < len(blocks) and blocks[i].get("type") == "paragraph": i += 1  # drop old intro paragraph
        continue
    if b.get("type") == "heading" and t.startswith("Queue — "):
        r = m.api(base, auth, "GET", "/rest/api/content/search?cql=" + urllib.parse.quote("parent=1189609473 and type=page") + "&limit=100")
        new_blocks.append(heading(f"Queue — {r['size']} pages parented here (22 promoted 16 September 2026)", b.get("attrs", {}).get("level", 2)))
        i += 1; continue
    new_blocks.append(b); i += 1
adf["content"] = new_blocks
put("1189609473", p, adf, p["title"], "Promoted pages removed from the queue; label name corrected (Confluence labels cannot contain dots)")
