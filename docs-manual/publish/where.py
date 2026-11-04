#!/usr/bin/env python3
"""where.py <pageId>... : title, parent chain, labels, first 300 chars of text."""
import sys, os, re, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("pub", os.path.join(HERE, "confluence-publish.py"))
pub = importlib.util.module_from_spec(spec); spec.loader.exec_module(pub)
base, auth = pub.load_creds()
for pid in sys.argv[1:]:
    p = pub.api(base, auth, "GET", f"/api/v2/pages/{pid}?body-format=storage")
    a = pub.api(base, auth, "GET", f"/api/v2/pages/{pid}/ancestors?limit=10")
    chain = " > ".join(x["id"] for x in a.get("results", []))
    lab = [l["name"] for l in pub.api(base, auth, "GET", f"/api/v2/pages/{pid}/labels").get("results", [])]
    txt = re.sub(r"<[^>]+>", " ", p["body"]["storage"]["value"])
    txt = re.sub(r"\s+", " ", txt)[:300]
    print(f"{pid} v{p['version']['number']} [{p['title']}] parent={p.get('parentId')}({p.get('parentType')}) chain={chain} labels={lab}\n   {txt}")
