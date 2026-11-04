#!/usr/bin/env python3
"""promote-wip.py plan.json [--dry-run]

Moves review-area drafts into the live manual as work in progress, one page at a time:
  - new parent (page or folder), optional new title
  - a note panel at the top: "Work in progress", naming the review ticket (idempotent)
  - labels: + doc-in-review, - manual-draft
plan.json: [{"id": "...", "parent": "...", "title": "..." | null, "ticket": "OGC-1234" | null, "wip": true}]
"""
import sys, os, json, importlib.util, urllib.parse
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("pub", os.path.join(HERE, "confluence-publish.py"))
pub = importlib.util.module_from_spec(spec); spec.loader.exec_module(pub)
base, auth = pub.load_creds()
plan = json.load(open(sys.argv[1])); DRY = "--dry-run" in sys.argv
MARK = "Work in progress."
JIRA = "https://uwdigi.atlassian.net/browse/"

def panel(ticket):
    rev = (f'It is being reviewed under <a href="{JIRA}{ticket}">{ticket}</a>, so details may still change.'
           if ticket else 'It is waiting for review, so details may still change.')
    return ('<ac:structured-macro ac:name="note" ac:schema-version="1"><ac:rich-text-body><p><strong>' + MARK +
            '</strong> This page is published before its review is finished so you can use it now. ' + rev +
            ' If something on your screen does not match, add a comment to this page.</p></ac:rich-text-body></ac:structured-macro>')

for step in plan:
    pid = step["id"]
    p = pub.api(base, auth, "GET", f"/api/v2/pages/{pid}?body-format=storage")
    if str(p["id"]) != str(pid): sys.exit(f"crossed read on {pid}")
    body = p["body"]["storage"]["value"]
    title = step.get("title") or p["title"]
    if step.get("wip", True) and MARK not in body:
        body = panel(step.get("ticket")) + body
    if "—" in title: sys.exit(f"em dash in title for {pid}: {title}")
    print(f"{pid}: {p['title']!r} -> {title!r}, parent {p.get('parentId')} -> {step['parent']}")
    if DRY: continue
    r = pub.api(base, auth, "PUT", f"/api/v2/pages/{pid}", {
        "id": pid, "status": "current", "title": title, "parentId": step["parent"],
        "body": {"representation": "storage", "value": body},
        "version": {"number": p["version"]["number"] + 1, "message": "Moved into the manual as work in progress"}})
    print(f"   v{r['version']['number']} parent {r.get('parentId')} ({r.get('parentType')})")
    if step.get("wip", True):
        pub.api(base, auth, "POST", f"/rest/api/content/{pid}/label", [{"prefix": "global", "name": "doc-in-review"}])
        labs = [l["name"] for l in pub.api(base, auth, "GET", f"/api/v2/pages/{pid}/labels").get("results", [])]
        if "manual-draft" in labs:
            try:
                pub.api(base, auth, "DELETE", f"/rest/api/content/{pid}/label/manual-draft")
            except SystemExit as e:
                print("   label delete:", e)
        print("   labels", [l["name"] for l in pub.api(base, auth, "GET", f"/api/v2/pages/{pid}/labels").get("results", [])])
