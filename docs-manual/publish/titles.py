#!/usr/bin/env python3
"""titles.py "Title" ... : list OG pages whose title matches exactly."""
import sys, os, importlib.util, urllib.parse
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("pub", os.path.join(HERE, "confluence-publish.py"))
pub = importlib.util.module_from_spec(spec); spec.loader.exec_module(pub)
base, auth = pub.load_creds()
for t in sys.argv[1:]:
    cql = 'space = OG and type = page and title = "%s"' % t.replace('"', '\\"')
    r = pub.api(base, auth, "GET", "/rest/api/content/search?limit=10&cql=" + urllib.parse.quote(cql))
    print(t, "->", [(x["id"], x["title"]) for x in r.get("results", [])])
