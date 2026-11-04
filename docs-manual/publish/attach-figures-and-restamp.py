#!/usr/bin/env python3
"""
Attach the captured figures to the two test-catalog manual pages and re-stamp
their provenance to testing.openelis-global.org.

One pass per page:
  1. upload each PNG as a page attachment (Confluence REST, multipart via curl)
  2. read back each attachment's fileId
  3. GET the page as ADF
  4. swap every "[ drop image: <path> ]" paragraph for a mediaSingle node,
     taking the alt text from the caption paragraph that follows it
  5. replace the note panel and the Provenance block
  6. PUT the page back (version + 1)

Credentials come from ~/.openelis/confluence.env, exactly as confluence-publish.py
reads them; the token is never printed.

    python3 attach-figures-and-restamp.py --dry-run
    python3 attach-figures-and-restamp.py
    python3 attach-figures-and-restamp.py --page 1668972546

Why this and not confluence-publish.py: that publisher replaces the whole page body
from a storage-XHTML file. These two pages are live ADF with panels, tables and a
date node; rebuilding them as XHTML would lose that and would promote the first
At-a-glance row to a header. This edits the ADF in place and only touches the nodes
it names.
"""

import argparse, base64, json, os, re, struct, subprocess, sys, urllib.request, urllib.error

# Both are overridable so the script runs unchanged on the Mac itself or inside the
# Cowork VM, where the same folders are mounted under $HOME/mnt/.
CAPTURES = os.environ.get(
    "OE_CAPTURES",
    os.path.expanduser("~/dev/openelis-work-claude/docs-manual/captures"))
CONFLUENCE_ENV = os.environ.get(
    "OE_CONFLUENCE_ENV", os.path.expanduser("~/.openelis/confluence.env"))

# ---------------------------------------------------------------- credentials

def load_creds():
    env = dict(os.environ)
    cfg = CONFLUENCE_ENV
    if os.path.exists(cfg):
        with open(cfg) as f:
            for ln in f:
                ln = ln.strip()
                if ln and not ln.startswith("#") and "=" in ln:
                    k, v = ln.split("=", 1)
                    env.setdefault(k.strip(), v.strip())
    base = env.get("CONFLUENCE_BASE", "https://uwdigi.atlassian.net/wiki").rstrip("/")
    email, token = env.get("CONFLUENCE_EMAIL"), env.get("CONFLUENCE_API_TOKEN")
    if not (email and token):
        sys.exit("Missing CONFLUENCE_EMAIL / CONFLUENCE_API_TOKEN (env or ~/.openelis/confluence.env).")
    return base, base64.b64encode(f"{email}:{token}".encode()).decode()


def api(base, auth, method, path, body=None):
    url = base + path
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", "Basic " + auth)
    req.add_header("Accept", "application/json")
    if data is not None:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        sys.exit(f"{method} {path} -> {e.code}: {e.read().decode()[:500]}")


def check_identity(base, auth):
    """A Jira-scoped token authenticates as anonymous here and every upload 403s."""
    me = api(base, auth, "GET", "/rest/api/user/current")
    if me.get("type") == "anonymous":
        sys.exit("Token authenticates as anonymous on Confluence. It needs "
                 "write:attachment:confluence — issue a new one at id.atlassian.com.")
    return me.get("displayName", "?")

# ---------------------------------------------------------------- attachments

def existing_attachments(base, auth, page):
    res = api(base, auth, "GET", f"/rest/api/content/{page}/child/attachment?limit=200")
    return {a["title"]: a["id"] for a in res.get("results", [])}


def upload_attachment(base, auth, page, filepath, existing):
    name = os.path.basename(filepath)
    common = ["-s", "-S",
              "-H", "Authorization: Basic " + auth,
              "-H", "X-Atlassian-Token: nocheck",
              "-F", f"file=@{filepath}"]
    if name in existing:
        url = f"{base}/rest/api/content/{page}/child/attachment/{existing[name]}/data"
    else:
        url = f"{base}/rest/api/content/{page}/child/attachment"
    r = subprocess.run(["curl", *common, "-X", "POST", url], capture_output=True, text=True)
    if r.returncode != 0 or ('"statusCode"' in r.stdout and '"results"' not in r.stdout):
        sys.exit(f"attachment {name} failed: {r.stdout[:300]}")
    print(f"  + {name}")


def file_ids(base, auth, page):
    """filename -> media fileId, which is what an ADF media node references."""
    res = api(base, auth, "GET",
              f"/rest/api/content/{page}/child/attachment?limit=200&expand=extensions")
    out = {}
    for a in res.get("results", []):
        fid = (a.get("extensions") or {}).get("fileId")
        if fid:
            out[a["title"]] = fid
    return out


def png_size(path):
    with open(path, "rb") as f:
        head = f.read(24)
    if head[:8] == b"\x89PNG\r\n\x1a\n" and head[12:16] == b"IHDR":
        return struct.unpack(">II", head[16:24])
    return (None, None)

# ---------------------------------------------------------------- ADF helpers

DROP = re.compile(r"^\s*\[\s*drop image:\s*(?P<path>\S+?)\s*\]\s*$")


def node_text(node):
    if node.get("type") == "text":
        return node.get("text", "")
    return "".join(node_text(c) for c in node.get("content") or [])


def media_node(file_id, page_id, alt, w, h):
    media = {"type": "media",
             "attrs": {"type": "file", "id": file_id,
                       "collection": f"contentId-{page_id}", "alt": alt}}
    if w and h:
        media["attrs"]["width"] = w
        media["attrs"]["height"] = h
    return {"type": "mediaSingle",
            "attrs": {"layout": "center", "width": 100, "widthType": "percentage"},
            "content": [media]}


def para(*parts):
    """para("plain", ("bold", "strong"), ("italic", "em")) -> ADF paragraph."""
    content = []
    for p in parts:
        if isinstance(p, tuple):
            text, mark = p
            content.append({"type": "text", "text": text, "marks": [{"type": mark}]})
        else:
            content.append({"type": "text", "text": p})
    return {"type": "paragraph", "content": content}


def note_panel(paragraphs):
    return {"type": "panel", "attrs": {"panelType": "note"}, "content": paragraphs}

# ---------------------------------------------------------------- page config

RESTAMP = {
    "1668972546": {
        "title": "Manage lab units",
        "captures": "lab-units-editor",
        "panel": [
            para(("Draft for verification.", "strong"),
                 " Re-verified on 2026-09-22 against testing.openelis-global.org, version 3.2.2.0: "
                 "the Lab Units Editor is deployed there and every control, helper line and dialog "
                 "described below renders on it. The walkthrough was driven on a development build "
                 "of develop (commit d538b3c32, version 3.2.2.0) on the local dev stack, and the "
                 "figures were captured on that build."),
        ],
        "provenance": [
            para(("Drafted", "strong"), " 2026-09-21 · ",
                 ("Re-verified", "strong"), " 2026-09-22 · ",
                 ("Instance", "strong"), " testing.openelis-global.org · ",
                 ("OpenELIS version", "strong"), " 3.2.2.0 · ",
                 ("Jira", "strong"), " OGC-949 (Feature Doc OGC-1211) · ",
                 ("Drift contract", "strong"), " lab-units-editor"),
            para(("Driven live on the development build (2026-09-21):", "strong"),
                 " opening the list; filtering by typing and by domain; adding a unit and being "
                 "taken to its Basic Info; saving a description; refusing a duplicate and an "
                 "over-long name; changing the domain and cancelling the confirmation; saving a "
                 "display order position and reading the renumbered table, then restoring it; "
                 "opening Assign tests, searching, assigning one active test and seeing the unit "
                 "become active; selecting a test and reassigning it to another unit; switching a "
                 "unit off and seeing the warning for one that still has tests."),
            para(("Re-verified on testing (2026-09-22):", "strong"),
                 " the Lab Unit Management list with its domain counters, search, the two filters "
                 "and Add Lab Unit; the Add New Lab Unit form and its helper text; a unit's Basic "
                 "Info with the Active switch and the 60-character Description; Assigned Tests "
                 "with Assign tests and Reassign selected; and the Assign Tests to This Lab Unit "
                 "dialog, whose wording matches the figure."),
            para(("Not re-driven on testing", "strong"),
                 ", because each one writes to a shared instance: the save confirmations, the "
                 "duplicate-name and over-long-name refusals, the Change Lab Unit Domain? "
                 "confirmation, the deactivation warning, and the display-order save. Those "
                 "remain as driven on the development build."),
            para(("Figures", "strong"),
                 " were captured on the development build, so the counts they show are that "
                 "instance's data and they show one name field per language enabled there. "
                 "Four of them — the duplicate-name refusal, the save confirmation, the domain "
                 "dialog and the deactivation warning — carry a capture artifact: the application "
                 "header renders partway down the page. The controls and messages in them are "
                 "correct; re-capture when convenient."),
            {"type": "paragraph", "content": [
                {"type": "text",
                 "text": "Awaiting second-reviewer verification. Not yet labelled doc-verified.",
                 "marks": [{"type": "em"}]}]},
        ],
        "captions": {},
    },
    "1432453132": {
        "title": "Test Catalog Management: the unified editor",
        "captures": "test-catalog-editor",
        "panel": [
            para(("Revised for verification.", "strong"),
                 " Re-verified on 2026-09-22 against testing.openelis-global.org, version 3.2.2.0: "
                 "the unified editor is deployed there and every section, control and helper line "
                 "described below renders on it. The walkthrough was driven on a development build "
                 "of develop (commit d538b3c32, version 3.2.2.0) on the local dev stack, and the "
                 "figures were captured on that build."),
        ],
        "provenance": [
            para(("Drafted", "strong"), " 2026-06-29 · ",
                 ("Revised", "strong"), " 2026-09-13, 2026-09-21 · ",
                 ("Re-verified", "strong"), " 2026-09-22 · ",
                 ("Instance", "strong"), " testing.openelis-global.org · ",
                 ("OpenELIS version", "strong"), " 3.2.2.0 · ",
                 ("Jira", "strong"), " OGC-949 (Feature Doc OGC-1203; review epic OGC-1154; "
                 "OGC-1230) · ",
                 ("Drift contract", "strong"), " test-catalog-editor"),
            para(("Driven live on the development build (2026-09-21):", "strong"),
                 " opening the list, opening the filter row, searching by name, opening a test and "
                 "each of its fifteen sections, changing and saving a Description and reading it "
                 "back after a reload, typing into the Lab Unit field, creating a panel from the "
                 "Panels section and finding it in the Panel Editor, creating a test, giving its "
                 "primary component a Numeric result type and saving, activating it from Basic "
                 "Info and finding it in the orderable test list, switching it off again, opening "
                 "the Panel Editor list, a panel's four sections and the Add Panel form."),
            para(("Re-verified on testing (2026-09-22):", "strong"),
                 " the Test Catalog list with Filters, the configuration-issues banner and the "
                 "Name / Sample Type / Code / Domain / Status columns; the unified editor's "
                 "fifteen sections; Basic Info including Lab Unit, Sample types, Domain, AMR "
                 "surveillance test, Culture workflow and its four options, Active and Orderable; "
                 "the Create new test form with its Select at least one sample type and created "
                 "Inactive notes; and the Panel Editor list with the domain note, the Mixed domain "
                 "tag and the Sample Types (derived) column."),
            para(("Not re-driven on testing", "strong"),
                 ", because each one writes to a shared instance: creating a test, activating it "
                 "and the activation gate, creating a panel from the Panels section, and the save "
                 "confirmations. Those remain as driven on the development build."),
            para(("Figures", "strong"),
                 " were captured on the development build, so the counts they show are that "
                 "instance's data. One of them — Basic Info after activation — carries a capture "
                 "artifact: the application header renders partway down the page. The controls and "
                 "messages in it are correct; re-capture when convenient."),
            {"type": "paragraph", "content": [
                {"type": "text",
                 "text": "Awaiting second-reviewer verification. Not yet labelled doc-verified.",
                 "marks": [{"type": "em"}]}]},
        ],
        # caption fixes: exact current text -> replacement
        "captions": {
            "Basic Info right after switching Active on: Test activated., Orderable on, and the LOINC warning.":
                "Basic Info after switching Active on: Active and Orderable are both on, and the "
                "test carries the warning that it has no LOINC code.",
        },
    },
}

# ---------------------------------------------------------------- the pass

def transform(doc, page_id, ids, cap_dir, captions, panel, provenance, report):
    out, i, n = [], 0, len(doc["content"])
    seen_panel = False
    while i < n:
        node = doc["content"][i]

        # 1. the note panel at the top
        if node.get("type") == "panel" and not seen_panel:
            seen_panel = True
            out.append(note_panel(panel))
            report.append("panel: replaced")
            i += 1
            continue

        # 2. the Provenance heading swallows everything after it
        if node.get("type") == "heading" and node_text(node).strip() == "Provenance":
            out.append(node)
            out.extend(provenance)
            report.append(f"provenance: replaced {n - i - 1} paragraph(s) with {len(provenance)}")
            break

        # 3. image placeholders
        if node.get("type") == "paragraph":
            m = DROP.match(node_text(node))
            if m:
                name = os.path.basename(m.group("path"))
                if name not in ids:
                    sys.exit(f"no uploaded attachment for {name}")
                alt = ""
                if i + 1 < n and doc["content"][i + 1].get("type") == "paragraph":
                    alt = node_text(doc["content"][i + 1]).strip()
                w, h = png_size(os.path.join(cap_dir, name))
                out.append(media_node(ids[name], page_id, alt, w, h))
                report.append(f"figure: {name} -> media node ({w}x{h})")
                i += 1
                continue

            # 4. caption fixes
            txt = node_text(node).strip()
            if txt in captions:
                out.append({"type": "paragraph", "content": [
                    {"type": "text", "text": captions[txt], "marks": [{"type": "em"}]}]})
                report.append(f"caption: rewritten ({txt[:40]}...)")
                i += 1
                continue

        out.append(node)
        i += 1

    return {**doc, "content": out}


def run_page(base, auth, page_id, cfg, dry):
    print(f"\n=== {page_id} — {cfg['title']} ===")
    cap_dir = os.path.join(CAPTURES, cfg["captures"])
    if not os.path.isdir(cap_dir):
        sys.exit(f"captures not found: {cap_dir}")

    got = api(base, auth, "GET", f"/api/v2/pages/{page_id}?body-format=atlas_doc_format")
    if str(got.get("id")) != str(page_id):
        sys.exit(f"crossed read: asked for {page_id}, got {got.get('id')} — discard and retry")
    doc = json.loads(got["body"]["atlas_doc_format"]["value"])

    wanted = []
    for node in doc["content"]:
        if node.get("type") == "paragraph":
            m = DROP.match(node_text(node))
            if m:
                wanted.append(os.path.basename(m.group("path")))
    print(f"  {len(wanted)} figure slot(s)")
    missing = [w for w in wanted if not os.path.exists(os.path.join(cap_dir, w))]
    if missing:
        sys.exit("missing capture files: " + ", ".join(missing))

    if dry:
        ids = {w: f"DRY-{i}" for i, w in enumerate(wanted)}
    else:
        existing = existing_attachments(base, auth, page_id)
        for w in wanted:
            upload_attachment(base, auth, page_id, os.path.join(cap_dir, w), existing)
        ids = file_ids(base, auth, page_id)
        absent = [w for w in wanted if w not in ids]
        if absent:
            sys.exit("uploaded but no fileId came back for: " + ", ".join(absent))

    report = []
    new_doc = transform(doc, page_id, ids, cap_dir, cfg["captions"],
                        cfg["panel"], cfg["provenance"], report)
    for line in report:
        print("  " + line)
    for old in cfg["captions"]:
        if not any(old[:40] in r for r in report):
            sys.exit(f"caption to fix was not found on the page: {old[:60]}")

    if dry:
        print("  (dry run — nothing written)")
        return

    api(base, auth, "PUT", f"/api/v2/pages/{page_id}", {
        "id": str(page_id),
        "status": "current",
        "title": got["title"],
        "version": {"number": got["version"]["number"] + 1,
                    "message": "Attach figures; re-stamp provenance to testing 3.2.2.0"},
        "body": {"representation": "atlas_doc_format",
                 "value": json.dumps(new_doc)},
    })
    print(f"  written — version {got['version']['number'] + 1}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--page", action="append", help="page id (default: both)")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    base, auth = load_creds()
    if not a.dry_run:
        print("authenticated as " + check_identity(base, auth))
    for pid in (a.page or list(RESTAMP)):
        run_page(base, auth, pid, RESTAMP[pid], a.dry_run)


if __name__ == "__main__":
    main()
