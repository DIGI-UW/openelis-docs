#!/usr/bin/env python3
"""Self-tests for docs_hooks.py. Run: python3 hooks/scripts/test_docs_hooks.py (exit 1 on failure)."""
import json
import os
import subprocess
import sys
import tempfile
import uuid

HERE = os.path.dirname(os.path.abspath(__file__))
HOOK = os.path.join(HERE, "docs_hooks.py")
EM = chr(0x2014)
FAILS = []
COUNT = 0


def run(cmd, payload):
    p = subprocess.run([sys.executable, HOOK, cmd], input=json.dumps(payload),
                       capture_output=True, text=True, timeout=20)
    if p.returncode != 0:
        FAILS.append(f"{cmd}: exit {p.returncode}")
    return json.loads(p.stdout) if p.stdout.strip().startswith("{") else p.stdout


def decision(out):
    return out.get("hookSpecificOutput", {}).get("permissionDecision") if isinstance(out, dict) else None


def expect(name, got, want):
    global COUNT
    COUNT += 1
    if got != want:
        FAILS.append(f"{name}: got {got!r}, want {want!r}")


def bash(command, cwd="/home/x"):
    return decision(run("command-gate", {"tool_name": "Bash", "cwd": cwd, "tool_input": {"command": command}}))


def osa(script):
    return decision(run("command-gate", {"tool_name": "mcp__remote-devices__Control_your_Mac__osascript",
                                         "tool_input": {"script": script}}))


# ---------------------------------------------------------------- command-gate: credentials
expect("cat env denied", bash("cat ~/.openelis/confluence.env"), "deny")
expect("osascript cat env denied", osa('do shell script "cat ~/.openelis/transifex.env"'), "deny")
expect("grep env without -q denied", bash("grep TOKEN ~/.openelis/confluence.env"), "deny")
expect("grep -c env allowed", bash("grep -c CONFLUENCE_API_TOKEN ~/.openelis/confluence.env"), None)
expect("source env allowed", bash('set -a; . "$HOME/.openelis/confluence.env"; set +a; python3 x.py'), None)
expect("echo token var denied", bash('echo "$CONFLUENCE_API_TOKEN"'), "deny")
expect("printenv denied", bash("printenv"), "deny")
expect("env grep token denied", bash("env | grep -i token"), "deny")
expect("ordinary ls allowed", bash("ls -la docs-manual"), None)

# ---------------------------------------------------------------- command-gate: git in the public repo
expect("git add -A denied", bash("cd ~/Documents/openelis-docs && git add -A"), "deny")
expect("git add . denied", bash("git add .", cwd="/Users/casey/Documents/openelis-docs"), "deny")
expect("git add env denied", bash("cd openelis-docs && git add docs-manual/confluence.env"), "deny")
expect("git force push denied", bash("cd openelis-docs && git push --force origin main"), "deny")
expect("git add by name allowed", bash("cd openelis-docs && git add plugin/openelis-docs/README.md"), None)
expect("git add -A elsewhere not ours", bash("cd ~/other-repo && git add -A"), None)

# ---------------------------------------------------------------- command-gate: publishing
expect("publish asks", bash("cd docs-manual/publish && python3 confluence-publish.py --page 123 --xhtml a.xhtml --images img"), "ask")
expect("publish dry run allowed", bash("python3 confluence-publish.py --page 123 --xhtml a.xhtml --dry-run"), None)
expect("osascript fr-publish asks", osa('do shell script "cd ~/Documents/\'OpenELIS QA\'/docs-manual/fr && (nohup /usr/bin/python3 fr-publish.py content --only 1 > p.log 2>&1 &)"'), "ask")
expect("fr-tree dry run allowed", bash("python3 fr-tree.py"), None)
expect("fr-tree apply asks", bash("python3 fr-tree.py --apply"), "ask")
expect("fr-banner apply asks", bash("OE_LANG=fr python3 docs-manual/fr/fr-banner.py --apply"), "ask")
expect("reading the publisher allowed", bash("cat confluence-publish.py | head"), None)
expect("grep in publisher allowed", bash("grep -n argparse docs-manual/fr/fr-publish.py"), None)
expect("em dash in title denied", bash(f'python3 confluence-publish.py --create --space OG --parent 1 --title "Admin {EM} X" --xhtml a.xhtml'), "deny")
tmp = tempfile.mkdtemp()
bad = os.path.join(tmp, "bad.xhtml")
good = os.path.join(tmp, "good.xhtml")
open(bad, "w", encoding="utf-8").write(f"<p>Save {EM} then close.</p>")
open(good, "w", encoding="utf-8").write(f'<p>See <ac:link><ri:page ri:content-title="Old {EM} title"/></ac:link>.</p>')
expect("em dash in xhtml input denied", bash(f"python3 confluence-publish.py --page 1 --xhtml {bad} --images x"), "deny")
expect("dash only in a title attribute asks", bash(f"python3 confluence-publish.py --page 1 --xhtml {good} --images x"), "ask")


# ---------------------------------------------------------------- payload-guard
def guard(name, tool_input):
    return decision(run("payload-guard", {"tool_name": name, "tool_input": tool_input}))


UPD = "mcp__Atlassian__updateConfluencePage"
adf = {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "text", "text": "Fine."}]}]}
expect("update adf allowed", guard(UPD, {"pageId": "1", "contentFormat": "adf", "body": json.dumps(adf)}), None)
expect("update html denied", guard(UPD, {"pageId": "1", "contentFormat": "html", "body": "<p>x</p>"}), "deny")
expect("update default format denied", guard(UPD, {"pageId": "1", "body": "<p>x</p>"}), "deny")
expect("update markdown denied", guard(UPD, {"pageId": "1", "contentFormat": "markdown", "body": "x"}), "deny")
expect("update adf with em dash denied", guard(UPD, {"pageId": "1", "contentFormat": "adf", "body": json.dumps(adf).replace("Fine.", f"A {EM} B")}), "deny")
expect("update adf dict body with em dash denied", guard(UPD, {"pageId": "1", "contentFormat": "adf", "title": f"Part 5 {EM} X", "body": adf}), "deny")
expect("create markdown allowed", guard("mcp__Atlassian__createConfluencePage", {"spaceId": "OG", "title": "New page", "body": "Hello", "contentFormat": "markdown"}), None)
expect("create with em dash denied", guard("mcp__Atlassian__createConfluencePage", {"title": f"A {EM} B", "body": "x"}), "deny")
expect("footer comment em dash denied", guard("mcp__Atlassian__createConfluenceFooterComment", {"pageId": "1", "body": f"a {EM} b"}), "deny")
expect("write xhtml em dash denied", guard("Write", {"file_path": "/x/page.xhtml", "content": f"<p>a {EM} b</p>"}), "deny")
expect("write xhtml clean allowed", guard("Write", {"file_path": "/x/page.xhtml", "content": "<p>a: b</p>"}), None)
expect("edit adf.json em dash denied", guard("Edit", {"file_path": "/x/p.adf.json", "old_string": "a", "new_string": f"b {EM}"}), "deny")
expect("write markdown note not a payload", guard("Write", {"file_path": "/x/notes.md", "content": f"a {EM} b"}), None)
expect("filesystem write xhtml denied", guard("mcp__remote-devices__Filesystem__write_file", {"path": "/Users/c/p.xhtml", "content": f"{EM}"}), "deny")


# ---------------------------------------------------------------- bench-reminder
def transcript(events, project=True):
    path = os.path.join(tmp, f"t-{uuid.uuid4().hex}.jsonl")
    with open(path, "w", encoding="utf-8") as f:
        if project:
            f.write(json.dumps({"message": {"role": "user", "content": "This session is attached to the Project **\"OpenELIS User Manual\"**."}}) + "\n")
        for name, inp in events:
            f.write(json.dumps({"message": {"role": "assistant", "content": [
                {"type": "tool_use", "name": name, "input": inp}]}}) + "\n")
    return path


def stop(path, sid=None, active=False):
    out = run("bench-reminder", {"transcript_path": path, "session_id": sid or uuid.uuid4().hex,
                                 "stop_hook_active": active})
    return out.get("decision") if isinstance(out, dict) else None


BENCH = "https://claude.ai/artifact/LdorWo3a3SHUgKpRAQUJcp"
pub = ("Bash", {"command": "python3 confluence-publish.py --page 1 --xhtml a.xhtml --images i"})
bench_write = ("ArtifactData", {"action": "batch", "url": BENCH, "writes": []})
bench_read = ("ArtifactData", {"action": "list", "url": BENCH, "collection": "items"})
doc = ("Projects", {"method": "project_write", "path": "x.md", "content": "y"})

expect("publish without bench blocks", stop(transcript([pub])), "block")
expect("publish then bench write passes", stop(transcript([pub, bench_write])), None)
expect("bench read is not a sync", stop(transcript([pub, bench_read])), "block")
expect("bench then new publish blocks", stop(transcript([bench_write, pub])), "block")
expect("project doc in manual project blocks", stop(transcript([doc])), "block")
expect("project doc elsewhere passes", stop(transcript([doc], project=False)), None)
expect("drift run blocks", stop(transcript([("mcp__x__osascript", {"script": 'do shell script "cd q && (nohup ./run-d.sh > /dev/null 2>&1 &)"'})])), "block")
expect("confluence update blocks", stop(transcript([(UPD, {"pageId": "1", "contentFormat": "adf", "body": "{}"})])), "block")
expect("no manual work passes", stop(transcript([("Bash", {"command": "ls"})])), None)
expect("stop_hook_active passes", stop(transcript([pub]), active=True), None)
sid = uuid.uuid4().hex
p = transcript([pub])
expect("first stop blocks", stop(p, sid), "block")
expect("second stop for same change passes", stop(p, sid), None)

# ---------------------------------------------------------------- session-start
out = run("session-start", {})
expect("session-start prints context", isinstance(out, str) and "bench-sync" in out and EM not in out, True)

# ---------------------------------------------------------------- robustness
p2 = subprocess.run([sys.executable, HOOK, "command-gate"], input="not json", capture_output=True, text=True)
expect("bad input exits 0 silently", (p2.returncode, p2.stdout), (0, ""))

if FAILS:
    print(f"{len(FAILS)} of {COUNT} hook tests failed:")
    for f in FAILS:
        print("  " + f)
    sys.exit(1)
print(f"all {COUNT} hook tests passed")
