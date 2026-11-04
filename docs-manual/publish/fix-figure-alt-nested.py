#!/usr/bin/env python3
"""Like fix-figure-alt.py, but also finds figures nested in lists (a mediaSingle inside a listItem).
Alt = the caption paragraph that follows the figure in the same parent. Retries because Confluence
drops alt while a fresh upload is still processing.
    python3 fix-figure-alt-nested.py <pageId> [...]
"""
import importlib.util, json, sys, time, os
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("pub", os.path.join(HERE, "attach-figures-and-restamp.py"))
pub = importlib.util.module_from_spec(spec); spec.loader.exec_module(pub)
def sanitize(c):
    return (c.replace(": ", " - ").replace(":", " - ").replace(" / ", " - ").replace("/", "-").replace('"', "").replace("“", "").replace("”", "").strip())
def walk(node, out):
    kids = node.get("content") or []
    for i, n in enumerate(kids):
        if n.get("type") == "mediaSingle":
            cap = pub.node_text(kids[i + 1]).strip() if i + 1 < len(kids) and kids[i + 1].get("type") == "paragraph" else ""
            out.append((n, sanitize(cap)))
        walk(n, out)
base, auth = pub.load_creds()
for pid in sys.argv[1:]:
    for attempt in range(1, 3):
        g = pub.api(base, auth, "GET", f"/api/v2/pages/{pid}?body-format=atlas_doc_format")
        if str(g["id"]) != str(pid): sys.exit(f"crossed read on {pid}")
        doc = json.loads(g["body"]["atlas_doc_format"]["value"])
        figs = []; walk(doc, figs); todo = 0
        for n, alt in figs:
            if alt and n["content"][0]["attrs"].get("alt") != alt:
                print("  diff:", repr(n["content"][0]["attrs"].get("alt")), "->", repr(alt)); n["content"][0]["attrs"]["alt"] = alt; todo += 1
        if not todo:
            missing = [i for i, (n, a) in enumerate(figs) if not n["content"][0]["attrs"].get("alt")]
            print(f"{pid} v{g['version']['number']}: {len(figs)} figures, missing alt: {missing or 'none'}"); break
        pub.api(base, auth, "PUT", f"/api/v2/pages/{pid}", {"id": str(pid), "status": "current", "title": g["title"],
            "version": {"number": g["version"]["number"] + 1, "message": "Figure alt text from captions"},
            "body": {"representation": "atlas_doc_format", "value": json.dumps(doc)}})
        print(f"{pid}: attempt {attempt} set {todo}"); time.sleep(4)
