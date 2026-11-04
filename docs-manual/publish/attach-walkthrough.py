#!/usr/bin/env python3
"""Attach a walkthrough video to a manual page and add a link line under the How-to line (ADF, v2).
    python3 attach-walkthrough.py <pageId> <video path> [--dry-run]"""
import json, importlib.util, os, sys
here = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("pub", os.path.join(here, "confluence-publish.py"))
pub = importlib.util.module_from_spec(spec); spec.loader.exec_module(pub)
pid, video = sys.argv[1], sys.argv[2]
DRY = "--dry-run" in sys.argv
base, auth = pub.load_creds()
name = os.path.basename(video)
if not DRY:
    pub.upload_attachment(base, auth, pid, video, pub.existing_attachments(base, auth, pid))
p = pub.api(base, auth, "GET", f"/api/v2/pages/{pid}?body-format=atlas_doc_format")
if str(p["id"]) != pid: sys.exit("crossed read")
doc = json.loads(p["body"]["atlas_doc_format"]["value"])
href = f"{base}/download/attachments/{pid}/{name}"
if href in json.dumps(doc): print("link already present"); sys.exit(0)
c = doc["content"]
idx = next(i for i, n in enumerate(c) if n.get("type") == "paragraph" and "How-to" in json.dumps(n))
c.insert(idx + 1, {"type": "paragraph", "content": [
    {"type": "text", "text": "Walkthrough video: "},
    {"type": "text", "text": "watch the whole workflow on OpenELIS 3.3.0 (4 minutes, MP4)", "marks": [{"type": "link", "attrs": {"href": href}}]},
    {"type": "text", "text": "."}]})
body = {"id": pid, "status": "current", "title": p["title"],
        "body": {"representation": "atlas_doc_format", "value": json.dumps(doc)},
        "version": {"number": p["version"]["number"] + 1, "message": "Walkthrough video linked"}}
if DRY: print("DRY insert at", idx + 1, href); sys.exit(0)
r = pub.api(base, auth, "PUT", f"/api/v2/pages/{pid}", body)
print("put", r["id"], "v", r["version"]["number"], "parent", r.get("parentId"))
