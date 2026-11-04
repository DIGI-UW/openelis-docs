#!/usr/bin/env python3
"""Print the TOC page (1326972929) blocks that link 1441202177 or 1661763585, with their path."""
import json, importlib.util, os, sys
here = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("f", os.path.join(here, "fix-at-a-glance-headers.py"))
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
base, auth = m.load_creds()
p = m.api(base, auth, "GET", "/api/v2/pages/1326972929?body-format=atlas_doc_format")
assert str(p["id"]) == "1326972929"
doc = json.loads(p["body"]["atlas_doc_format"]["value"])
def walk(n, path):
    if isinstance(n, dict):
        s = json.dumps(n)
        if n.get("type") in ("listItem", "paragraph", "tableRow") and ("1441202177" in s or "1661763585" in s):
            print(path, n.get("type")); print(s[:1500]); print()
        for i, c in enumerate(n.get("content", []) or []): walk(c, path + [i])
walk(doc, [])
print("version", p["version"]["number"])
