#!/usr/bin/env python3
"""mkfolder.py <parentId> "<title>" : create a folder in space OG under a page or folder (v2 API)."""
import sys, os, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("pub", os.path.join(HERE, "confluence-publish.py"))
pub = importlib.util.module_from_spec(spec); spec.loader.exec_module(pub)
base, auth = pub.load_creds()
parent, title = sys.argv[1], sys.argv[2]
space_id = pub.api(base, auth, "GET", "/api/v2/spaces?keys=OG")["results"][0]["id"]
r = pub.api(base, auth, "POST", "/api/v2/folders", {"spaceId": space_id, "title": title, "parentId": parent})
print("folder", r.get("id"), r.get("title"), "parent", r.get("parentId"))
