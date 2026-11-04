#!/usr/bin/env python3
"""Move a page under a new parent (page or folder) with the v2 API: move.py <pageId> <parentId>"""
import sys, os, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("pub", os.path.join(HERE, "confluence-publish.py"))
pub = importlib.util.module_from_spec(spec); spec.loader.exec_module(pub)
base, auth = pub.load_creds()
pid, parent = sys.argv[1], sys.argv[2]
p = pub.api(base, auth, "GET", f"/api/v2/pages/{pid}?body-format=storage")
body = {"id": pid, "status": "current", "title": p["title"], "parentId": parent,
        "body": {"representation": "storage", "value": p["body"]["storage"]["value"]},
        "version": {"number": p["version"]["number"] + 1, "message": "Promoted: moved into the live manual"}}
r = pub.api(base, auth, "PUT", f"/api/v2/pages/{pid}", body)
print(pid, "v%d" % r["version"]["number"], "parent", r.get("parentId"), r.get("parentType"))
