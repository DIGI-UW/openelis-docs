#!/usr/bin/env python3
"""Retitle a page, keeping its storage body: retitle.py <pageId> "<new title>" """
import sys, os, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("pub", os.path.join(HERE, "confluence-publish.py"))
pub = importlib.util.module_from_spec(spec); spec.loader.exec_module(pub)
base, auth = pub.load_creds()
pid, title = sys.argv[1], sys.argv[2]
p = pub.api(base, auth, "GET", f"/rest/api/content/{pid}?expand=body.storage,version,space")
body = {"id": pid, "type": "page", "title": title, "space": {"key": p["space"]["key"]},
        "version": {"number": p["version"]["number"] + 1, "message": "Retitle: remove em dash"},
        "body": {"storage": {"value": p["body"]["storage"]["value"], "representation": "storage"}}}
r = pub.api(base, auth, "PUT", f"/rest/api/content/{pid}", body)
print(pid, "v%d" % r["version"]["number"], r["title"])
