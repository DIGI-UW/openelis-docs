#!/usr/bin/env python3
"""List OG pages modified since a date: recent.py 2026-10-12"""
import sys, os, importlib.util, urllib.parse
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("pub", os.path.join(HERE, "confluence-publish.py"))
pub = importlib.util.module_from_spec(spec); spec.loader.exec_module(pub)
base, auth = pub.load_creds()
cql = f'space=OG and type=page and lastmodified >= "{sys.argv[1]}" order by lastmodified desc'
start = 0
while True:
    r = pub.api(base, auth, "GET", "/rest/api/content/search?limit=50&start=%d&expand=version,ancestors&cql=%s" % (start, urllib.parse.quote(cql)))
    for p in r.get("results", []):
        anc = p.get("ancestors", [])
        par = anc[-1]["id"] if anc else ""
        print(p["id"], "v%d" % p["version"]["number"], p["version"]["when"][:16], "parent", par, "|", p["title"])
    if r.get("size", 0) < 50: break
    start += 50
