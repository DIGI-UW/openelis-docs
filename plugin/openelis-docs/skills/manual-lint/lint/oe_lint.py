#!/usr/bin/env python3
"""Lint OpenELIS manual pages with the OpenELIS Vale rules, without Vale.

Vale is the reference linter (`vale --config .vale.ini <file>`). This script reads the same
rule files in styles/OpenELIS/ and applies the rule types they use (existence, substitution,
occurrence), so a page can be linted where Vale is not installed (the cloud sandbox, CI).

Usage:
  python3 oe_lint.py <file> [<file> ...]      # .xhtml (storage format), .html, .md, .txt
  python3 oe_lint.py --json <file>            # machine-readable findings
Exit code 1 when any error-level finding remains.
"""
from __future__ import annotations

import html
import json
import os
import re
import sys

try:
    import yaml  # PyYAML
except ImportError:  # pragma: no cover
    sys.exit("oe_lint.py needs PyYAML (pip install pyyaml)")

HERE = os.path.dirname(os.path.abspath(__file__))
STYLES = os.path.join(HERE, "styles", "OpenELIS")


def py_regex(rx: str) -> str:
    """Translate the RE2 escapes the rules use into Python's."""
    return re.sub(r"\\x\{([0-9A-Fa-f]{4})\}", lambda m: "\\u" + m.group(1).lower(), rx)


def load_rules():
    rules = []
    for name in sorted(os.listdir(STYLES)):
        if name.endswith((".yml", ".yaml")):
            with open(os.path.join(STYLES, name), encoding="utf-8") as f:
                r = yaml.safe_load(f)
            r["name"] = "OpenELIS." + os.path.splitext(name)[0]
            rules.append(r)
    return rules


def to_text(raw: str, path: str) -> str:
    """Readable text of a page: tags dropped, CDATA kept, entities decoded."""
    if not path.endswith((".xhtml", ".html", ".htm")):
        return raw
    t = re.sub(r"<!\[CDATA\[(.*?)\]\]>", r"\1", raw, flags=re.S)
    t = re.sub(r"<ac:parameter[^>]*>.*?</ac:parameter>", " ", t, flags=re.S)
    t = re.sub(r"</(p|li|h[1-6]|td|th|tr|div)>", "\n", t)
    t = re.sub(r"<br\s*/?>", "\n", t)
    t = re.sub(r"<[^>]+>", " ", t)
    t = html.unescape(t)
    return re.sub(r"[ \t]+", " ", t)


def line_of(text: str, pos: int) -> int:
    return text.count("\n", 0, pos) + 1


def check(path: str, rules):
    raw = open(path, encoding="utf-8").read()
    text = to_text(raw, path)
    out = []
    for r in rules:
        scope = r.get("scope", "text")
        body = raw if scope == "raw" else text
        flags = re.I if r.get("ignorecase") else 0
        ext = r.get("extends")
        if ext == "existence":
            pats = list(r.get("tokens") or [])
            if r.get("raw"):
                pats.append("".join(r["raw"]))
            for p in pats:
                p = py_regex(p)
                if not r.get("nonword"):
                    p = r"\b(?:" + p + r")\b"
                for m in re.finditer(p, body, flags):
                    out.append((r, m.group(0), line_of(body, m.start()), r["message"].replace("%s", m.group(0).strip(), 1)))
        elif ext == "substitution":
            for bad, good in (r.get("swap") or {}).items():
                for m in re.finditer(r"\b(?:" + py_regex(bad) + r")\b", body, flags):
                    msg = r["message"].replace("%s", str(good), 1).replace("%s", m.group(0), 1)
                    out.append((r, m.group(0), line_of(body, m.start()), msg))
        elif ext == "occurrence" and scope == "sentence":
            tok = py_regex(r.get("token", r"\b(\w+)\b"))
            pos = 0
            for sent in re.split(r"(?<=[.!?])\s+|\n+", text):
                n = len(re.findall(tok, sent))
                if n > int(r.get("max", 25)):
                    out.append((r, sent[:60], line_of(text, text.find(sent, pos)), r["message"]))
                pos += len(sent)
    return [{"file": path, "line": ln, "rule": r["name"], "level": r.get("level", "warning"),
             "match": match, "message": msg} for (r, match, ln, msg) in out]


def main(argv):
    as_json = "--json" in argv
    files = [a for a in argv if a != "--json"]
    if not files:
        print(__doc__)
        return 2
    rules = load_rules()
    findings = []
    for f in files:
        findings.extend(check(f, rules))
    if as_json:
        print(json.dumps(findings, indent=1, ensure_ascii=False))
    else:
        for x in findings:
            print(f"{x['file']}:{x['line']}  {x['level']:<10} {x['rule']:<26} {x['message']}")
        counts = {lvl: sum(1 for x in findings if x["level"] == lvl) for lvl in ("error", "warning", "suggestion")}
        print(f"\n{counts['error']} errors, {counts['warning']} warnings, {counts['suggestion']} suggestions")
    return 1 if any(x["level"] == "error" for x in findings) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
