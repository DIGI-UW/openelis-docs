# openelis-docs plugin

Documentation for OpenELIS Global, built from what the OpenELIS User Manual project learned between
July and November 2026. It replaces three standalone skills: `openelis-user-manual`,
`openelis-docs-freshness` and `triage-bench-sync` (and `openelis-screenshots`, whose capture job
moved to the openelis-qa plugin's `qa-evidence`). Remove those after installing this, or both sets
of instructions will load.

## What's in it

The pipeline runs in this order: verify, capture, author, lint, publish, register the drift
contract, translate, sync the bench.

| Skill | Use it for |
|---|---|
| `manual-author` | The one rule (document only verified behavior), evidence tiers, page shapes, review gate, clearing and promotion, drift contracts, Casey's conventions. |
| `manual-lint` | Vale rules (with a no-install fallback linter), audits of published pages, A/C/F grades for the bench. |
| `manual-publish` | The REST publisher with figures, the ADF-only edit rule, Confluence IDs, labels, gotchas. |
| `docs-freshness` | The weekly drift run (`run-d.sh`): English UI drift, commit impact, bench summary. |
| `translation-refresh` | French, Indonesian and Spanish trees: freshness, mirror, labels, the segment-level refresh kit. |
| `bench-sync` | Write the Documentation triage bench after any manual work. |

| Other | What it does |
|---|---|
| Agent `page-reviewer` | Runs the review gate on a page cold (re-derive, then diff), so the author is not grading their own page. |
| Hook: session start | Reminds the session of the one rule, the bench and the credential rule. |
| Hook: command gate | Asks Casey before any script that writes to Confluence (dry runs pass); refuses printing a credential; refuses `git add -A`, `git add .`, `commit -a`, force pushes and env files in this public repo; refuses a publish command or XHTML input with an em dash. |
| Hook: payload guard | Refuses `updateConfluencePage` unless `contentFormat` is `adf`; refuses an em dash in a Confluence title, body or comment, or written into a `.xhtml` or `.adf.json` payload. Dashes inside `ri:content-title` attributes are allowed (they must match real titles). |
| Hook: bench reminder | Once per change, asks for a bench sync when a Confluence write, publish, drift run or User Manual project doc happened and the bench was not written. |

Capture stays in the openelis-qa plugin (`openelis-qa:qa-evidence`, manual media mode); UI wording
stays with `openelis-ui-vocabulary` and the documentation spine with `openelis-design`. Install the
openelis-qa plugin too.

Hooks and the agent work in Claude Code-style sessions. In a plain chat only the skills load. The
hooks need `python3`; without it they do nothing.

## Where the source lives

This folder in DIGI-UW/openelis-docs is the only source. The same repo holds the docs tooling
(`docs-manual/`, `run-d.sh`). `npm run build:plugin` checks the plugin and writes
`dist/openelis-docs.plugin`; CI runs `npm run check:plugin`, which fails on a malformed skill or
agent, a missing hook script, a failing hook self-test, an em dash, or a publisher copy that differs
from `docs-manual/publish/confluence-publish.py`.

To change the plugin: edit files here, run `npm run build:plugin`, bump `version` in
`.claude-plugin/plugin.json`, add a line to `CHANGELOG.md`, open a PR.

## Setup notes

- Connectors used: Atlassian (Confluence and Jira), Control your Mac, Claude in Chrome (UI checks),
  GitHub (read), and the "OpenELIS User Manual" project.
- Credentials: `~/.openelis/confluence.env` (Confluence token with `write:attachment:confluence`)
  and `~/.openelis/transifex.env`, on Casey's Mac only.
- On the Mac the repo is cloned at `~/Documents/openelis-docs`; `~/Documents/OpenELIS QA/docs-manual`
  and `run-d.sh` there are symlinks into it, because the drift spec runs from the QA harness folder.
