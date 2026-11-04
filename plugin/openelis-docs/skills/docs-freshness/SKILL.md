---
name: docs-freshness
description: This skill should be used for the OpenELIS docs freshness check (the docs spine), such as the weekly drift run, "check docs freshness", "run the drift check", "which manual pages are stale?", "did the new release break the manual?", reading drift-report.json or bench-drift.json, fixing a drift contract, or adding a page to the drift check. It runs run-d.sh (English UI drift, commit-to-doc impact, bench summary, then translation freshness per language) and turns the results into work.
---

# OpenELIS docs freshness (English drift)

One run answers: which English manual pages no longer match the screen, which code changes touched
documented screens, and (through `translation-refresh`) which translated pages are behind their
English page. The weekly scheduled task and any interactive "check docs freshness" use this skill.

Never write an em dash. Never print or paste a token.

## Where things are

The tooling lives in the **DIGI-UW/openelis-docs** repo (`run-d.sh`, `docs-manual/`). On Casey's
Mac the clone is `~/Documents/openelis-docs`, and `~/Documents/OpenELIS QA/docs-manual` and
`~/Documents/OpenELIS QA/run-d.sh` are symlinks into it, so every older path still works. The
drift spec itself (`tests/docs/drift.check.spec.ts`, Playwright project `docs`) is in the QA
harness folder `~/Documents/OpenELIS QA`, which is why `run-d.sh` runs from there.

| File (in `docs-manual/`) | What it is |
|---|---|
| `contracts.json` | One section per manual page: routes, anchors, spine fields (manual-author `references/contracts.md`) |
| `drift-report.json` | Per contract: ok, review, drift or error, with missing anchors |
| `commit-doc-impact.py` / `.json` | Recent develop commits mapped to documented screens (`uiPaths`) |
| `bench_summary.py` -> `bench-drift.json` | The summary the triage bench loads into `drift/latest` |
| `fr/translation-freshness.py` -> `bench-translations*.json` | Translation freshness, one file per language |

Everything that reaches OpenELIS or Confluence runs on the Mac through the Control-your-Mac
connector (`osascript` `do shell script`); the sandbox cannot launch the browser against the
instances or reach Confluence REST. As of 9 Oct 2026 only testing.openelis-global.org is watched;
do not add bases back unless Casey asks.

## Run the check

1. Start it in the background (osascript calls time out on long jobs):
   `do shell script "cd ~/Documents/'OpenELIS QA' && (nohup ./run-d.sh > /dev/null 2>&1 &) ; echo started"`
2. Poll for `~/Documents/OpenELIS QA/drift.done` (short polls, under about 170 s each). The English
   part takes up to about 30 minutes; each translation language about 3. If `drift.done` never
   appears, read the tail of `drift.log`.
3. **Sanity check before believing anything.** In `bench-drift.json` the testing entry under
   `instances` must have `checked == contracts`. `checked: 0`, a `!!! <base> run failed` line, or a
   wall of `drift` right after a version bump is a failed run (usually a stale login or a timeout),
   not data. Rerun testing alone:
   `BASE=https://testing.openelis-global.org npx playwright test --project=docs tests/docs/drift.check.spec.ts --timeout=5400000 --retries=0 >> drift.log 2>&1; python3 docs-manual/bench_summary.py`
4. Read `bench-drift.json`, then the translation files (hand those to `translation-refresh`).

## Read the results

- **ok**: nothing to do.
- **review**: the instance version differs from `capturedVersion`. Recheck the page when
  convenient; bump `capturedVersion` once it is re-verified.
- **drift**: a documented control is gone. The page needs recapture and rewrite (`manual-author`,
  capture with `openelis-qa:qa-evidence`). Look at the screen before blaming the product: an anchor
  can be wrong.
- **error**: the route failed or redirected. Check the contract (retired route, wizard-gated deep
  link) and the instance before calling it drift.
- **codeChanged** in a row: develop commits touched the page's `uiPaths` since capture; worth a
  look even when anchors pass.
- Uncovered areas in `commit-doc-impact.json`: changed screens with no contract; candidates for new
  pages or new contracts.

## Fix a contract

Edit `contracts.json` with a short script after a dated backup; validate the JSON; rerun the check
for that base. Anchors come from a current figure, spelling-neutral (testing renders en_GB). A
page moved to LEGACY Versions gets `"retired": true`, not deletion.

## Unattended (scheduled) runs

Run the check and the sanity check, publish the raw reports as the scheduled task says, and sync
the bench. Make no Confluence changes and no contract edits: list what needs fixing as bench items.
If the bench write fails, leave the prepared writes in `docs-manual/bench-sync-pending-<date>/` and
say plainly that the bench was not updated.

## Close out (every run)

1. Write or update a project doc in "OpenELIS User Manual" (`claude/<topic>-<date>.md`): what ran,
   counts, what was fixed, what is open.
2. Sync the triage bench with `bench-sync` (`drift/latest`, `translations/latest*`, items,
   `meta/sync`).
3. Tell Casey in two or three lines: ok / review / drift / error counts, translation counts, and the
   next item.
