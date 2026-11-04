#!/usr/bin/env python3
"""PUT a storage-format XHTML body onto an existing Confluence page (v1 API), keeping title.
Usage: put-storage.py <pageId> <file.xhtml> "<version message>"
Credentials as confluence-publish.py (env or ~/.openelis/confluence.env)."""
import sys, os, importlib.util, re
here = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("pub", os.path.join(here, "confluence-publish.py"))
pub = importlib.util.module_from_spec(spec); spec.loader.exec_module(pub)

pid, xhtml, msg = sys.argv[1], sys.argv[2], sys.argv[3]
base, auth = pub.load_creds()
body = open(xhtml, encoding="utf-8").read()
# every referenced attachment must already exist on the page
names = set(re.findall(r'ri:filename="([^"]+)"', body))
existing = pub.existing_attachments(base, auth, pid)
missing = names - set(existing)
if missing:
    sys.exit("Missing attachments on page %s: %s" % (pid, ", ".join(sorted(missing))))
cur = pub.api(base, auth, "GET", f"/rest/api/content/{pid}?expand=version")
ver = cur["version"]["number"]
res = pub.api(base, auth, "PUT", f"/rest/api/content/{pid}", {
    "id": pid, "type": "page", "title": cur["title"],
    "version": {"number": ver + 1, "message": msg},
    "body": {"storage": {"value": body, "representation": "storage"}},
})
print(f"{pid} {cur['title']!r} v{ver} -> v{res['version']['number']}; attachments referenced: {len(names)}")
