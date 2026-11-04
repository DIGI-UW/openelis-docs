#!/usr/bin/env python3
"""Copy one version of a manual page into the LEGACY Versions folder, with its figures.

Usage:
  make-legacy-copy.py <pageId> <version|latest|before:YYYY-MM-DD> "<new title>" <parentFolderId> "<3.3.0 page link text>"

Reads the chosen version's storage body (v1 historical API), creates a new page under the folder
(v2 API, which accepts a folder as parent), copies every attachment the body references from the
source page, then sets the body with a short note panel at the top pointing to the current page.
Credentials as confluence-publish.py.
"""
import sys, os, re, json, importlib.util, subprocess, tempfile, urllib.parse
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("pub", os.path.join(HERE, "confluence-publish.py"))
pub = importlib.util.module_from_spec(spec); spec.loader.exec_module(pub)

pid, which, title, parent, linktext = sys.argv[1:6]
base, auth = pub.load_creds()

def pick_version():
    if which == "latest":
        return pub.api(base, auth, "GET", f"/rest/api/content/{pid}?expand=version")["version"]["number"]
    if which.startswith("before:"):
        cutoff = which.split(":", 1)[1]
        vs = pub.api(base, auth, "GET", f"/api/v2/pages/{pid}/versions?limit=250&sort=-modified-date")["results"]
        older = [v for v in vs if v["createdAt"][:10] < cutoff]
        if not older: sys.exit("no version before " + cutoff)
        return max(v["number"] for v in older)
    return int(which)

ver = pick_version()
src = pub.api(base, auth, "GET", f"/rest/api/content/{pid}?status=historical&version={ver}&expand=body.storage,version,space")
if str(src["id"]) != str(pid): sys.exit("crossed read")
body = src["body"]["storage"]["value"]
print(f"source {pid} v{ver} {src['title']!r}, {len(body)} chars, edited {src['version']['when']}")

space_id = pub.api(base, auth, "GET", f"/api/v2/spaces?keys={src['space']['key']}")["results"][0]["id"]
created = pub.api(base, auth, "POST", "/api/v2/pages", {"spaceId": space_id, "status": "current", "title": title,
    "parentId": parent, "body": {"representation": "storage", "value": "<p/>"}})
new = created["id"]; print("created", new)

names = sorted(set(re.findall(r'ri:filename="([^"]+)"', body)))
atts = {a["title"]: a for a in pub.api(base, auth, "GET", f"/rest/api/content/{pid}/child/attachment?limit=250")["results"]}
tmp = tempfile.mkdtemp()
existing = {}
for n in names:
    a = atts.get(n)
    if not a: print("  ! not on source page:", n); continue
    dl = base + a["_links"]["download"]
    path = os.path.join(tmp, n)
    r = subprocess.run(["curl", "-s", "-S", "-L", "-H", "Authorization: Basic " + auth, "-o", path, dl], capture_output=True, text=True)
    if r.returncode: print("  ! download", n, r.stderr[:200]); continue
    pub.upload_attachment(base, auth, new, path, existing)

note = (f'<ac:structured-macro ac:name="note"><ac:rich-text-body><p><strong>Legacy version.</strong> '
        f'This copy describes OpenELIS releases before 3.3.0 (page version {ver}, last edited {src["version"]["when"][:10]}). '
        f'For OpenELIS 3.3.0 and later, see <a href="{base}/spaces/OG/pages/{pid}">{linktext}</a>.</p></ac:rich-text-body></ac:structured-macro>')
cur = pub.api(base, auth, "GET", f"/rest/api/content/{new}?expand=version")
pub.api(base, auth, "PUT", f"/rest/api/content/{new}", {"id": new, "type": "page", "title": title,
    "version": {"number": cur["version"]["number"] + 1, "message": f"Legacy copy of {pid} v{ver}"},
    "body": {"storage": {"value": note + body, "representation": "storage"}}})
print(f"legacy copy ready: {base}/spaces/OG/pages/{new}  ({len(names)} figures)")
