#!/usr/bin/env python3
"""Set each figure's alt text from the caption paragraph beneath it.

Confluence rewrites a media node's attrs while it is still processing a freshly
uploaded file, and drops `alt` when it does. So this retries: write, wait, check,
write again, until every media node on the page keeps its alt.

    python3 fix-figure-alt.py            # both pages
    python3 fix-figure-alt.py 1668972546
"""
import importlib.util, json, sys, time, os

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location(
    "pub", os.path.join(HERE, "attach-figures-and-restamp.py"))
pub = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pub)

def sanitize(caption):
    """Confluence silently drops a media alt containing a colon (verified against
    this site - the same node keeps an alt with a hyphen or a semicolon and loses
    the identical string with a colon. Double quotes do the same. So the alt says
    what the caption says, with the colon written as a dash and quotes dropped."""
    return (caption.replace(": ", " - ").replace(":", " - ")
                   .replace('"', "").replace("\u201c", "").replace("\u201d", "")
                   .strip())


PAGES = sys.argv[1:] or ["1668972546", "1432453132"]
base, auth = pub.load_creds()

for pid in PAGES:
    for attempt in range(1, 4):
        g = pub.api(base, auth, "GET", f"/api/v2/pages/{pid}?body-format=atlas_doc_format")
        if str(g["id"]) != str(pid):
            sys.exit(f"crossed read on {pid}")
        doc = json.loads(g["body"]["atlas_doc_format"]["value"])
        c = doc["content"]
        todo = 0
        for i, n in enumerate(c):
            if n["type"] != "mediaSingle":
                continue
            cap = ""
            if i + 1 < len(c) and c[i + 1]["type"] == "paragraph":
                cap = pub.node_text(c[i + 1]).strip()
            alt = sanitize(cap)
            if alt and n["content"][0]["attrs"].get("alt") != alt:
                n["content"][0]["attrs"]["alt"] = alt
                todo += 1
        if not todo:
            print(f"{pid}: all alt text in place after {attempt - 1} write(s)")
            break
        pub.api(base, auth, "PUT", f"/api/v2/pages/{pid}", {
            "id": str(pid), "status": "current", "title": g["title"],
            "version": {"number": g["version"]["number"] + 1,
                        "message": "Figure alt text from captions"},
            "body": {"representation": "atlas_doc_format", "value": json.dumps(doc)},
        })
        print(f"{pid}: attempt {attempt} set {todo}")
        time.sleep(3)
    else:
        print(f"{pid}: still missing alt after 3 attempts")

    g = pub.api(base, auth, "GET", f"/api/v2/pages/{pid}?body-format=atlas_doc_format")
    ms = [n for n in json.loads(g["body"]["atlas_doc_format"]["value"])["content"]
          if n["type"] == "mediaSingle"]
    missing = [i for i, n in enumerate(ms) if not n["content"][0]["attrs"].get("alt")]
    print(f"  {pid} v{g['version']['number']}: {len(ms)} figures, missing alt: {missing or 'none'}")
