#!/usr/bin/env python3
"""Update the 📖 User Manual landing page (1326972929) reading lists after the 2026-09-16 promotion.
ADF in / ADF out via v2 API. Changes, all by page ID:
  end-user list: PART 12 -> Results Entry 1439072277, PART 13 -> Validation 1441202177,
                 PART 14 -> Running Reports 1440841744
  admin list:    PART 5: Dictionary item removed (Dictionary Menu 1438973976 already listed),
                 Menu Configuration link 1439694850 -> 1160282114,
                 Reflex Testing 1439137808 and Calculated Value Tests 1438842886 appended,
                 empty trailing list item removed
  a one-line pointer to the LEGACY Versions folder added after the end-user list.
"""
import json, importlib.util, os, sys
here = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("f", os.path.join(here, "fix-at-a-glance-headers.py"))
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
base, auth = m.load_creds()
PID = "1326972929"
WIKI = "https://uwdigi.atlassian.net/wiki/spaces/OG/pages/"
DRY = "--dry-run" in sys.argv

def item(link_text, pid, tail):
    return {"type": "listItem", "content": [{"type": "paragraph", "content": [
        {"type": "text", "text": link_text, "marks": [{"type": "link", "attrs": {"href": WIKI + pid}}]},
        {"type": "text", "text": tail}]}]}

def hrefs(n, out):
    if isinstance(n, dict):
        for mk in n.get("marks", []) or []:
            if mk.get("type") == "link": out.append(mk["attrs"].get("href", ""))
        for c in n.get("content", []) or []: hrefs(c, out)
    elif isinstance(n, list):
        for c in n: hrefs(c, out)
    return out

def has(li, pid): return any(pid in h for h in hrefs(li, []))

p = m.api(base, auth, "GET", f"/api/v2/pages/{PID}?body-format=atlas_doc_format")
adf = json.loads(p["body"]["atlas_doc_format"]["value"])
blocks = adf["content"]
lists = [i for i, b in enumerate(blocks) if b.get("type") == "orderedList"]
assert len(lists) == 2, lists
eu, admin = blocks[lists[0]], blocks[lists[1]]
changes = []

# end-user list
new = []
for li in eu["content"]:
    if has(li, "278626329"):
        new.append(item("Results Entry", "1439072277", " — how to record results from the bench on the unified worklist.")); changes.append("PART 12 -> Results Entry")
    elif has(li, "284196875"):
        new.append(item("Validation", "1441202177", " — the supervisor-level review step before results are released.")); changes.append("PART 13 -> Validation")
    elif has(li, "284393490"):
        new.append(item("Running Reports", "1440841744", " — pulling results out of the system.")); changes.append("PART 14 -> Running Reports")
    else:
        new.append(li)
eu["content"] = new

# admin list
new = []
for li in admin["content"]:
    txt = m.cell_text(li).strip()
    if has(li, "256737340"):
        changes.append("PART 5: Dictionary item removed"); continue
    if not txt:
        changes.append("empty trailing item removed"); continue
    if has(li, "1439694850"):
        s = json.dumps(li).replace("1439694850", "1160282114"); li = json.loads(s); changes.append("Menu Configuration -> 1160282114")
    new.append(li)
if not any(has(li, "1439137808") for li in new):
    new.append(item("Reflex Testing", "1439137808", " — defining rules that add a follow-up test when a result meets a condition.")); changes.append("Reflex Testing added")
if not any(has(li, "1438842886") for li in new):
    new.append(item("Calculated Value Tests", "1438842886", " — defining results computed from other results or patient attributes.")); changes.append("Calculated Value Tests added")
admin["content"] = new

# legacy pointer after the end-user list (insert once)
marker = "LEGACY Versions"
if not any(marker in m.cell_text(b) for b in blocks):
    blocks.insert(lists[0] + 1, {"type": "paragraph", "content": [
        {"type": "text", "text": "Running an older release? The previous versions of these pages are kept in the "},
        {"type": "text", "text": "LEGACY Versions", "marks": [{"type": "link", "attrs": {"href": "https://uwdigi.atlassian.net/wiki/spaces/OG/folder/1657864193"}}]},
        {"type": "text", "text": " folder."}]})
    changes.append("legacy pointer added")

print("changes:", changes)
if DRY: sys.exit(0)
res = m.api(base, auth, "PUT", f"/api/v2/pages/{PID}", {
    "id": PID, "status": p["status"], "title": p["title"],
    "body": {"representation": "atlas_doc_format", "value": json.dumps(adf)},
    "version": {"number": p["version"]["number"] + 1, "message": "Reading lists updated for the 2026-09-16 promotion; legacy pointer added"}})
print("v", p["version"]["number"], "->", res["version"]["number"])
