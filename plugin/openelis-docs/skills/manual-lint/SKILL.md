---
name: manual-lint
description: This skill should be used when Casey asks to lint, audit, grade or style-check OpenELIS user manual pages ("lint this page", "check the style", "is this translation ready?", "audit the admin pages", "grade the manual for the bench", "find em dashes in the manual"), and before any manual draft is delivered or published. It runs the OpenELIS Vale rules (or the bundled fallback linter), audits live Confluence pages, and grades pages A, C or F for the triage bench.
---

# Lint, audit and grade OpenELIS manual pages

Three jobs: lint a draft before delivery, audit published pages, and grade pages for the
Documentation triage bench. The rules come from the manual-author skill's `references/style.md`;
this skill enforces the mechanical part.

## Lint a draft

Rules live in `lint/styles/OpenELIS/` (Vale format). Two ways to run them:

- **Vale** (reference): `cd lint && vale --config .vale.ini <page>.xhtml`. On Casey's Mac install
  it with `brew install vale` if `which vale` finds nothing.
- **Fallback, no install** (cloud sandbox, CI): `python3 lint/oe_lint.py <page>.xhtml [...]`
  (`--json` for machine output). Same rule files, same levels; exit 1 on any error. It needs
  PyYAML; where Python lacks it (Casey's Mac), use a throwaway venv:
  `/usr/bin/python3 -m venv /tmp/oe-lint-venv && /tmp/oe-lint-venv/bin/pip -q install pyyaml`, then
  run the linter with `/tmp/oe-lint-venv/bin/python`.

| Rule | Level | Catches |
|---|---|---|
| `OpenELIS.EmDash` | error | Any em dash |
| `OpenELIS.Terms` | error | Sidebar, left nav, Accession Number, Test Section or Unit, gender |
| `OpenELIS.LinkText` | error | "click here", "here", "this page" as link text |
| `OpenELIS.Placeholder` | error | Unresolved `[[...]]` placeholders |
| `OpenELIS.Filler` | warning | simply, just, easily, in order to, as per, please note |
| `OpenELIS.Translation` | warning | Latin abbreviations, idioms |
| `OpenELIS.VaguePronoun` | warning | Sentences starting "It is", "This opens" and the like |
| `OpenELIS.Versions` | warning | Version numbers in body prose |
| `OpenELIS.SentenceLength` | suggestion | Sentences over 25 words |

Errors block delivery. A warning may stand only with a reason (the version line at the top, a
version inside a quoted message). Lint again after review edits. When Casey sets a new term, add
it to `Terms.yml` and to the manual-author skill's `references/conventions.md`.

Lint does not check meaning. After lint, still check by reading: UI labels match the screen and
the en.json string; known-defect tips cite OGC keys; the feedback line is word for word; the At a
glance table has no `<thead>`.

## Audit published pages

1. List the pages: CQL by folder (`parent = <folderId> AND type = page`, folders are invisible to
   the page tools), by label (`label = "doc-in-review"`), or from `docs-manual/contracts.json`.
2. Fetch each page body with `contentFormat: "adf"` (read only), one page at a time: never run
   page reads in parallel (the MCP crosses responses between concurrent calls). Check that the
   returned `id` is the one you asked for.
3. Convert to text and lint (the fallback linter reads `.txt`). Also count em dashes outside
   `ri:content-title` attributes, and check: At a glance row 1 is not two header cells (the
   canary for an HTML-path write), every link is by page ID and resolves, feedback line present,
   WIP note present only on `doc-in-review` pages.
4. Report per page: errors, warnings, the checks above, and a grade. Fixes go through
   `manual-publish`; findings go on the bench (`bench-sync`).

## Grade (A, C, F) for the bench

Answer yes or no without a close read:

1. Does it follow the style guide?
2. Are the figures current with the live screen?
3. Does every link resolve and go where its text says?
4. Does it link to related pages?
5. Is there one clear audience?

A passes all, C passes most, F fails routinely. Write `grade` and `gradedDate` into the page's
contract (manual-author `references/contracts.md`). An F page becomes a bench item. Never
backfill grades from memory: grade a page only after reading it.
