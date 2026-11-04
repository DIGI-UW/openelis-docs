#!/usr/bin/env python3
"""Add or remove Confluence labels. Usage: labels.py <pageId> +label -label ...  (no args after id: list)"""
import sys, os, importlib.util, urllib.parse
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("pub", os.path.join(HERE, "confluence-publish.py"))
pub = importlib.util.module_from_spec(spec); spec.loader.exec_module(pub)
base, auth = pub.load_creds()
pid = sys.argv[1]
for op in sys.argv[2:]:
    name = op[1:]
    if op[0] == "+":
        pub.api(base, auth, "POST", f"/rest/api/content/{pid}/label", [{"prefix": "global", "name": name}])
    elif op[0] == "-":
        import urllib.request, urllib.error
        req = urllib.request.Request(f"{base}/rest/api/content/{pid}/label?name={urllib.parse.quote(name)}", method="DELETE")
        req.add_header("Authorization", "Basic " + auth)
        try: urllib.request.urlopen(req)
        except urllib.error.HTTPError as e: print("  delete", name, e.code)
res = pub.api(base, auth, "GET", f"/rest/api/content/{pid}/label")
print(pid, [l["name"] for l in res.get("results", [])])
