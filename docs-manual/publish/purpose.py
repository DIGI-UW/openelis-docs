#!/usr/bin/env python3
"""purpose.py <id>... : print each page's At a glance Purpose cell."""
import sys, os, re, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("pub", os.path.join(HERE, "confluence-publish.py"))
pub = importlib.util.module_from_spec(spec); spec.loader.exec_module(pub)
base, auth = pub.load_creds()
for pid in sys.argv[1:]:
    p = pub.api(base, auth, "GET", f"/api/v2/pages/{pid}?body-format=storage")
    s = p["body"]["storage"]["value"]
    m = re.search(r'Purpose.{0,40}?</th>\s*<td[^>]*>(.*?)</td>', s, re.S)
    t = re.sub(r"<[^>]+>", "", m.group(1)) if m else "(no purpose row)"
    print(pid, p["title"], "::", re.sub(r"\s+", " ", t)[:220])
