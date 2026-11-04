# Changelog

## 0.1.0 (2026-11-04)

First version. Replaces the `openelis-user-manual`, `openelis-docs-freshness` and
`triage-bench-sync` skills (and the retired `openelis-screenshots`).

- One source: this folder in DIGI-UW/openelis-docs, built and checked in CI, next to the docs
  tooling it drives (`docs-manual/`, `run-d.sh`), which had lived only on Casey's Mac.
- Six skills along the pipeline: `manual-author`, `manual-lint`, `manual-publish`,
  `docs-freshness`, `translation-refresh` (French, Indonesian, Spanish; split out of freshness),
  `bench-sync`.
- Review practice as it is now: pages waiting for review go live with a Work in progress note and
  `doc-in-review`; Taib's stamp plus a Done OGC-1271 sub-task clears them (13 and 28 Oct 2026).
  The old "draft under the review area first" step is gone.
- Capture points at `openelis-qa:qa-evidence` (manual media mode); the five references to the old
  screenshots skill are gone.
- `page-reviewer` agent for the review gate.
- Hooks: ask before Confluence publish scripts; refuse printing credentials and broad git adds in
  this public repo; ADF-only page edits; no em dashes in any Confluence payload; bench reminder.
- `manual-lint`: an `EmDash` rule, a `.vale.ini` (was missing), and `oe_lint.py`, which applies the
  same rules where Vale is not installed.
- The 62 em dashes in the old user-manual skill are gone; the plugin has none.
