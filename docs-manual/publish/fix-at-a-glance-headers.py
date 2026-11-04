#!/usr/bin/env python3
"""
Repair the At-a-glance table on OpenELIS manual pages that were written through the
Atlassian MCP's HTML path (2026-09-16 promotion). Confluence promoted the first row's
value cell (the "Purpose" text) from tableCell to tableHeader, so row 1 renders as two
grey header cells.

What it does, per page, using the Confluence v2 REST API with the body as
atlas_doc_format (ADF), so nothing else in the page is touched:
  1. GET the page body as ADF.
  2. Find every table whose first row has exactly two cells, the first cell's text is
     "Purpose" and the second cell is a tableHeader. Change that second cell's type to
     tableCell. Nothing else changes.
  3. PUT the page back with the same title, same status, version+1.

Credentials: CONFLUENCE_EMAIL and CONFLUENCE_API_TOKEN from the environment or from
~/.openelis/confluence.env (KEY=VALUE lines), same as confluence-publish.py.
The token needs Confluence write scope (write:page:confluence).

Usage:
  python3 fix-at-a-glance-headers.py --dry-run          # report only
  python3 fix-at-a-glance-headers.py                    # apply to the default page list
  python3 fix-at-a-glance-headers.py 1440940035 ...     # apply to specific page IDs
"""
import base64, json, os, sys, urllib.request, urllib.error

DEFAULT_PAGES = [
    # merges
    "1160282114",  # Menu Configuration
    "1187840003",  # User Management
    # Administrator Guide
    "1439432709", "1439367188", "1439137808", "1438842886", "1439006727",
    "1439596548", "1438973976", "1439170565", "1437892659", "1439203334",
    "1439072261", "1439334404", "1438973960", "1438908431",
    # End User Manual
    "1439072277", "1441202177", "1440350210", "1440677908", "1440940035", "1440841744",
]

def load_creds():
    env = dict(os.environ)
    cfg = os.path.expanduser("~/.openelis/confluence.env")
    if os.path.exists(cfg):
        for ln in open(cfg):
            ln = ln.strip()
            if ln and not ln.startswith("#") and "=" in ln:
                k, v = ln.split("=", 1); env.setdefault(k.strip(), v.strip())
    base = env.get("CONFLUENCE_BASE", "https://uwdigi.atlassian.net/wiki").rstrip("/")
    email = env.get("CONFLUENCE_EMAIL"); token = env.get("CONFLUENCE_API_TOKEN")
    if not email or not token:
        sys.exit("Missing CONFLUENCE_EMAIL / CONFLUENCE_API_TOKEN (env or ~/.openelis/confluence.env).")
    return base, base64.b64encode(f"{email}:{token}".encode()).decode()

def api(base, auth, method, path, body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(base + path, data=data, method=method)
    req.add_header("Authorization", "Basic " + auth)
    req.add_header("Accept", "application/json")
    if data is not None:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        sys.exit(f"{method} {path} -> HTTP {e.code}: {e.read().decode()[:500]}")

def cell_text(cell):
    out = []
    def walk(n):
        if isinstance(n, dict):
            if n.get("type") == "text":
                out.append(n.get("text", ""))
            for c in n.get("content", []) or []:
                walk(c)
    walk(cell)
    return "".join(out).strip()

def fix_tables(node):
    """Return number of cells changed."""
    changed = 0
    if isinstance(node, dict):
        if node.get("type") == "table":
            rows = node.get("content") or []
            if rows and rows[0].get("type") == "tableRow":
                cells = rows[0].get("content") or []
                if (len(cells) == 2 and cell_text(cells[0]) == "Purpose"
                        and cells[1].get("type") == "tableHeader"):
                    cells[1]["type"] = "tableCell"
                    changed += 1
        for c in node.get("content", []) or []:
            changed += fix_tables(c)
    elif isinstance(node, list):
        for c in node:
            changed += fix_tables(c)
    return changed

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    dry = "--dry-run" in sys.argv
    pages = args or DEFAULT_PAGES
    base, auth = load_creds()
    for pid in pages:
        page = api(base, auth, "GET", f"/api/v2/pages/{pid}?body-format=atlas_doc_format")
        title = page["title"]; ver = page["version"]["number"]
        adf = json.loads(page["body"]["atlas_doc_format"]["value"])
        n = fix_tables(adf)
        if n == 0:
            print(f"{pid}  {title!r}  v{ver}: nothing to fix")
            continue
        if dry:
            print(f"{pid}  {title!r}  v{ver}: would change {n} cell(s)")
            continue
        body = {
            "id": pid,
            "status": page["status"],
            "title": title,
            "body": {"representation": "atlas_doc_format", "value": json.dumps(adf)},
            "version": {"number": ver + 1,
                        "message": "Repair At-a-glance row 1 (tableHeader -> tableCell) via ADF"},
        }
        res = api(base, auth, "PUT", f"/api/v2/pages/{pid}", body)
        print(f"{pid}  {title!r}  v{ver} -> v{res['version']['number']}: changed {n} cell(s)")

if __name__ == "__main__":
    main()
