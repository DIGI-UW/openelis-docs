#!/usr/bin/env python3
"""Dump storage of pages and contexts of patterns: ctx.py outdir pid... """
import sys, os, importlib.util, re, json
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("pub", os.path.join(HERE, "confluence-publish.py"))
pub = importlib.util.module_from_spec(spec); spec.loader.exec_module(pub)
base, auth = pub.load_creds()
out = sys.argv[1]; os.makedirs(out, exist_ok=True)
for pid in sys.argv[2:]:
    p = pub.api(base, auth, "GET", f"/rest/api/content/{pid}?expand=body.storage,version")
    s = p["body"]["storage"]["value"]
    open(os.path.join(out, f"{pid}.xhtml"), "w").write(s)
    n = len(re.findall("—|&mdash;", s))
    print(pid, "v%d" % p["version"]["number"], "emdash", n, "|", p["title"])
