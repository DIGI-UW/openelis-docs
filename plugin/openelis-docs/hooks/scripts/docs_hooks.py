#!/usr/bin/env python3
"""Hooks for the openelis-docs plugin.

Subcommands (each reads the hook's JSON from stdin):
  session-start    print the docs context reminder
  command-gate     PreToolUse on shell tools (Bash, device_bash, osascript):
                     - deny printing a credential (~/.openelis/*.env, *TOKEN* variables)
                     - deny broad git adds, commit -a and force pushes in the public openelis-docs repo
                     - deny a publish command or its XHTML input that carries an em dash
                     - ask Casey before any script that writes to Confluence runs
  payload-guard    PreToolUse on Confluence page/comment tools and file writes:
                     - deny an em dash in a Confluence title, body or comment
                     - deny updateConfluencePage unless contentFormat is "adf"
                     - deny an em dash written into a publish payload (.xhtml, .adf.json)
  bench-reminder   Stop: ask once per change for a triage bench sync after manual work

Every failure inside a hook exits 0 with no output, so a broken hook never blocks work.
"""
from __future__ import annotations

import json
import os
import re
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
BENCH_ID = "LdorWo3a3SHUgKpRAQUJcp"
EM = chr(0x2014)
DOCS_REPO = re.compile(r"openelis-docs", re.I)


def read_input() -> dict:
    try:
        return json.load(sys.stdin)
    except Exception:
        return {}


def emit(obj: dict) -> None:
    sys.stdout.write(json.dumps(obj))


def pre_tool(decision: str, reason: str) -> None:
    emit({"hookSpecificOutput": {"hookEventName": "PreToolUse",
                                 "permissionDecision": decision,
                                 "permissionDecisionReason": reason}})


def shell_text(tool_input: dict) -> str:
    text = " ".join(str(tool_input.get(k) or "") for k in ("command", "script", "cmd"))
    # osascript: look inside `do shell script "..."`
    return re.sub(r'do shell script\s+"', "; ", text).replace('\\"', '"')


def segments(text: str):
    """Shell segments split on ; && || | and newlines (good enough for a guard)."""
    return [s.strip() for s in re.split(r"\|\||&&|[;|\n]", text) if s.strip()]


def strip_title_attrs(text: str) -> str:
    """Drop ri:content-title attributes: they must match real page titles, dashes and all."""
    return re.sub(r'ri:content-title="[^"]*"', "", text)


# ---------------------------------------------------------------- session-start
def session_start(_: dict) -> None:
    with open(os.path.join(ROOT, "hooks", "context.md"), encoding="utf-8") as f:
        sys.stdout.write(f.read())


# ---------------------------------------------------------------- command-gate
ENV_FILE = re.compile(r"\.openelis/[\w.-]*\.env")
PRINTERS = {"cat", "less", "more", "head", "tail", "bat", "nl", "od", "xxd", "hexdump", "strings",
            "awk", "sed", "open", "pbcopy", "base64", "tee", "cp", "scp", "curl"}
SECRET_VAR = r"\$\{?[A-Za-z_]*(?:TOKEN|SECRET|PASSWORD|PASSWD|API_KEY|AUTH)[A-Za-z_]*\}?"


def prints_secret(text: str) -> str | None:
    for seg in segments(text):
        words = seg.split()
        if not words:
            continue
        cmd = os.path.basename(words[0].lstrip("("))
        if ENV_FILE.search(seg):
            if cmd in PRINTERS:
                return f"`{cmd}` on a credentials file"
            if cmd in {"grep", "egrep", "rg"} and not re.search(r"\s-[A-Za-z]*[qclL]", seg):
                return "grep on a credentials file without -q, -c or -l"
        if cmd in {"echo", "printf"} and re.search(SECRET_VAR, seg, re.I):
            return "echoing a credential variable"
        if cmd == "printenv" and (len(words) == 1 or re.search(r"TOKEN|SECRET|PASS|KEY|AUTH", seg, re.I)):
            return "printenv of credentials"
    if re.search(r"\benv\b\s*\|\s*(?:grep|rg)\b[^|;\n]*(?:token|secret|pass|key|auth)", text, re.I):
        return "env piped to grep for a credential"
    return None


GIT_BAD = [
    (re.compile(r"\bgit\s+add\s+(?:\S+\s+)*(?:-A|--all)\b"), "git add -A"),
    (re.compile(r"\bgit\s+add\s+(?:\S+\s+)*\.(?:\s|$|;|&|\|)"), "git add ."),
    (re.compile(r"\bgit\s+commit\s+(?:\S+\s+)*-a[mv]*\b"), "git commit -a"),
    (re.compile(r"\bgit\s+push\s+(?:\S+\s+)*(?:--force\b|-f\b)(?!-with-lease)"), "git push --force"),
    (re.compile(r"\bgit\s+add\s+(?:\S+\s+)*\S*(?:\.env\b|\.auth\b)"), "adding a credentials file"),
]

# Scripts that write to Confluence. Matched only when invoked (interpreter, ./ or nohup), so
# reading or copying the script is not gated.
PUBLISHERS = [
    ("confluence-publish.py", None),
    ("fr-publish.py", None),
    ("fr-tree.py", "--apply"),
    ("fr-banner.py", "--apply"),
    ("fr-archive.py", None),
    ("put-storage.py", None),
    ("copy-into.py", None),
    ("labels.py", None),
    ("fix-at-a-glance-headers.py", None),
    ("attach-figures-and-restamp.py", None),
    ("attach-walkthrough.py", None),
    ("attach-wizard-figures.sh", None),
    ("insert-wizard-media.sh", None),
    ("en-landing-fr.py", None),
    ("fr-landing.py", None),
]
INVOKE = r"(?:^|[\s;&|(])(?:\S*python3?(?:\.\d+)?\s+(?:-\S+\s+)*|bash\s+(?:-\S+\s+)*|sh\s+|\./)(?:\S*/)?"


def publish_calls(text: str):
    """(script, segment) for each publishing script this command runs, skipping dry runs."""
    out = []
    for seg in segments(text):
        for name, needs in PUBLISHERS:
            if re.search(INVOKE + re.escape(name) + r"(?=\s|$|[\"'])", seg):
                if "--dry-run" in seg:
                    continue
                if needs and needs not in seg:
                    continue
                out.append((name, seg))
    return out


def xhtml_inputs(seg: str):
    return re.findall(r"--xhtml[=\s]+[\"']?([^\s\"']+)", seg)


def command_gate(data: dict) -> None:
    ti = data.get("tool_input") or {}
    text = shell_text(ti)
    if not text.strip():
        return
    why = prints_secret(text)
    if why:
        pre_tool("deny", f"openelis-docs: {why}. Credentials stay in ~/.openelis/*.env and are read "
                         "by the scripts; never print, paste or commit them. To check a key is set, "
                         "use `grep -c KEY_NAME <file>`.")
        return
    in_repo = bool(DOCS_REPO.search(text) or DOCS_REPO.search(str(data.get("cwd") or "")))
    if in_repo and "git" in text:
        for rx, label in GIT_BAD:
            if rx.search(text):
                pre_tool("deny", f"openelis-docs: {label} is not allowed in the openelis-docs repo "
                                 "(it is public). Stage files by name with `git add <paths>`, never "
                                 "env or .auth files; --force-with-lease only on your own branch.")
                return
    calls = publish_calls(text)
    if not calls:
        return
    for name, seg in calls:
        if EM in strip_title_attrs(seg):
            pre_tool("deny", f"openelis-docs: the {name} command contains an em dash (organization "
                             "rule). Use a colon, comma or parentheses, then run it again.")
            return
        for path in xhtml_inputs(seg):
            p = os.path.expanduser(path)
            if os.path.isfile(p):
                try:
                    body = open(p, encoding="utf-8").read()
                except Exception:
                    continue
                n = strip_title_attrs(body).count(EM)
                if n:
                    pre_tool("deny", f"openelis-docs: {path} has {n} em dash(es) (organization rule). "
                                     "Run manual-lint, replace them, then publish.")
                    return
    names = ", ".join(sorted({n for n, _ in calls}))
    first = calls[0][1]
    pre_tool("ask", f"openelis-docs: this writes to Confluence ({names}). Lint clean, no human edits "
                    f"overwritten, dry run checked? Command: {first[:300]}")


# ---------------------------------------------------------------- payload-guard
CONFLUENCE_WRITE = re.compile(r"(createConfluencePage|updateConfluencePage|createConfluenceFooterComment|"
                              r"createConfluenceInlineComment)$")
FILE_WRITE = re.compile(r"(^Write$|^Edit$|^MultiEdit$|Filesystem__write_file$|Filesystem__edit_file$)")
PAYLOAD_PATH = re.compile(r"(\.xhtml|\.adf\.json)$", re.I)


def as_text(v) -> str:
    if isinstance(v, str):
        return v
    try:
        return json.dumps(v, ensure_ascii=False)
    except Exception:
        return str(v)


def payload_guard(data: dict) -> None:
    name = str(data.get("tool_name") or "")
    ti = data.get("tool_input") or {}
    if CONFLUENCE_WRITE.search(name):
        if name.endswith("updateConfluencePage"):
            fmt = str(ti.get("contentFormat") or "html").lower()
            if fmt != "adf":
                pre_tool("deny", "openelis-docs: edit existing Confluence pages with contentFormat "
                                 "\"adf\" on both the read and the write. The HTML path promotes table "
                                 "cells to headers and strips comment anchors and alt text; markdown "
                                 "deletes every figure (manual-publish skill).")
                return
        fields = [ti.get(k) for k in ("title", "body", "commentBody", "content")]
        text = strip_title_attrs(" ".join(as_text(f) for f in fields if f is not None))
        n = text.count(EM)
        if n:
            pre_tool("deny", f"openelis-docs: {n} em dash(es) in the Confluence title or body "
                             "(organization rule). Replace them with a colon, comma or parentheses, "
                             "including any already on the page, then write again.")
        return
    if FILE_WRITE.search(name):
        path = str(ti.get("file_path") or ti.get("path") or "")
        if not PAYLOAD_PATH.search(path):
            return
        parts = [ti.get("content"), ti.get("new_string")]
        for e in ti.get("edits") or []:
            if isinstance(e, dict):
                parts += [e.get("new_string"), e.get("newText")]
        text = strip_title_attrs(" ".join(as_text(p) for p in parts if p))
        n = text.count(EM)
        if n:
            pre_tool("deny", f"openelis-docs: {n} em dash(es) in a publish payload ({os.path.basename(path)}). "
                             "Organization rule: use a colon, comma or parentheses.")


# ---------------------------------------------------------------- bench-reminder
def transcript(path: str):
    """Yield ('tool', name, input) and ('text', text) events from a transcript JSONL."""
    with open(path, encoding="utf-8") as f:
        for line in f:
            try:
                d = json.loads(line)
            except Exception:
                continue
            content = (d.get("message") or {}).get("content")
            if isinstance(content, str):
                yield ("text", content, None)
                continue
            if not isinstance(content, list):
                continue
            for item in content:
                if not isinstance(item, dict):
                    continue
                if item.get("type") == "tool_use":
                    yield ("tool", item.get("name") or "", item.get("input") or {})
                elif item.get("type") == "text":
                    yield ("text", item.get("text") or "", None)


def is_manual_work(name: str, inp: dict, in_manual_project: bool) -> bool:
    if re.search(r"(createConfluencePage|updateConfluencePage)$", name):
        return True
    text = shell_text(inp)
    if text and (publish_calls(text) or re.search(r"run-d\.sh|translation-freshness\.py", text)):
        return True
    if name == "Projects" and inp.get("method") == "project_write" and in_manual_project:
        return True
    return False


def is_bench_write(name: str, inp: dict) -> bool:
    if not (name.endswith("ArtifactData") or name.endswith("Artifact")):
        return False
    s = json.dumps(inp)
    if BENCH_ID not in s:
        return False
    if name.endswith("ArtifactData"):
        return inp.get("action") in {"set", "update", "batch", "str_replace", "delete"}
    return inp.get("action", "publish") == "publish"


def bench_reminder(data: dict) -> None:
    if data.get("stop_hook_active"):
        return
    path = data.get("transcript_path")
    if not path or not os.path.exists(path):
        return
    events = list(transcript(path))
    in_manual = any(kind == "text" and "OpenELIS User Manual" in a for kind, a, _ in events)
    last_work = last_bench = -1
    i = 0
    for kind, a, b in events:
        if kind != "tool":
            continue
        if is_manual_work(a, b, in_manual):
            last_work = i
        if is_bench_write(a, b):
            last_bench = i
        i += 1
    if last_work < 0 or last_bench > last_work:
        return
    sid = re.sub(r"[^A-Za-z0-9_-]", "", str(data.get("session_id") or "x"))
    state = os.path.join(tempfile.gettempdir(), f"openelis-docs-bench-{sid}")
    try:
        with open(state, encoding="utf-8") as f:
            if int(f.read().strip() or -1) >= last_work:
                return
    except Exception:
        pass
    with open(state, "w", encoding="utf-8") as f:
        f.write(str(last_work))
    emit({"decision": "block",
          "reason": "openelis-docs: manual work happened (a Confluence write, a publish or drift run, "
                    "or a User Manual project doc) since the Documentation triage bench was last "
                    "written in this session. Sync it now (bench-sync skill), or say in one line why "
                    "this round does not change the bench."})


COMMANDS = {
    "session-start": session_start,
    "command-gate": command_gate,
    "payload-guard": payload_guard,
    "bench-reminder": bench_reminder,
}

if __name__ == "__main__":
    try:
        COMMANDS[sys.argv[1]](read_input())
    except Exception:
        pass
    sys.exit(0)
