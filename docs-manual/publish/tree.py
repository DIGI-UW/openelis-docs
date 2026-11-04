#!/usr/bin/env python3
"""tree.py <id> [maxdepth] : print the page/folder tree under a page or folder, with labels for pages."""
import sys, os, importlib.util, json
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("pub", os.path.join(HERE, "confluence-publish.py"))
pub = importlib.util.module_from_spec(spec); spec.loader.exec_module(pub)
base, auth = pub.load_creds()
root = sys.argv[1]; maxd = int(sys.argv[2]) if len(sys.argv) > 2 else 6
def kids(i, typ):
    out = []; url = f"/api/v2/{typ}s/{i}/direct-children?limit=250"
    while url:
        r = pub.api(base, auth, "GET", url)
        out += r.get("results", [])
        nxt = r.get("_links", {}).get("next")
        url = nxt.replace("/wiki", "", 1) if nxt else None
    return out
def labels(i):
    try:
        r = pub.api(base, auth, "GET", f"/api/v2/pages/{i}/labels?limit=50")
        return [l["name"] for l in r.get("results", [])]
    except Exception:
        return []
def walk(i, typ, d):
    if d > maxd: return
    for c in kids(i, typ):
        t = c.get("type")
        lab = labels(c["id"]) if t == "page" else []
        print("  " * d + f"[{t}] {c['id']} {c.get('title')}" + (f"  {{{','.join(lab)}}}" if lab else ""))
        walk(c["id"], t, d + 1)
typ = sys.argv[3] if len(sys.argv) > 3 else "page"
walk(root, typ, 0)
