#!/usr/bin/env python3
"""copy-into.py <srcId> <dstId> "<message>" [old=>new ...]

Puts the source page's current storage body onto the destination page (keeping the destination's
ID, title and parent), copying every attachment the body references. Optional old=>new pairs are
plain string replacements applied to the body first. Used to merge a newer draft into an older page
ID (manual links are made by page ID).
"""
import sys, os, re, subprocess, tempfile, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("pub", os.path.join(HERE, "confluence-publish.py"))
pub = importlib.util.module_from_spec(spec); spec.loader.exec_module(pub)
base, auth = pub.load_creds()
src, dst, msg = sys.argv[1:4]
reps = [a.split("=>", 1) for a in sys.argv[4:]]
s = pub.api(base, auth, "GET", f"/api/v2/pages/{src}?body-format=storage")
if str(s["id"]) != str(src): sys.exit("crossed read")
body = s["body"]["storage"]["value"]
for old, new in reps:
    n = body.count(old); body = body.replace(old, new); print(f"replaced {n}x {old[:60]!r}")
names = sorted(set(re.findall(r'ri:filename="([^"]+)"', body)))
atts = {a["title"]: a for a in pub.api(base, auth, "GET", f"/rest/api/content/{src}/child/attachment?limit=250")["results"]}
existing = pub.existing_attachments(base, auth, dst)
tmp = tempfile.mkdtemp()
for n in names:
    a = atts.get(n)
    if not a: print("  ! not on source:", n); continue
    path = os.path.join(tmp, n)
    r = subprocess.run(["curl", "-s", "-S", "-L", "-H", "Authorization: Basic " + auth, "-o", path, base + a["_links"]["download"]], capture_output=True, text=True)
    if r.returncode: print("  ! download", n); continue
    pub.upload_attachment(base, auth, dst, path, existing)
d = pub.api(base, auth, "GET", f"/api/v2/pages/{dst}")
if str(d["id"]) != str(dst): sys.exit("crossed read dst")
r = pub.api(base, auth, "PUT", f"/api/v2/pages/{dst}", {"id": dst, "status": "current", "title": d["title"], "parentId": d["parentId"],
    "body": {"representation": "storage", "value": body}, "version": {"number": d["version"]["number"] + 1, "message": msg}})
print(f"{dst} v{r['version']['number']} {r['title']!r} ({len(names)} figures)")
