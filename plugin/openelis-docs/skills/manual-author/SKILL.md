---
name: manual-author
description: This skill should be used when Casey asks to write, draft, update, rewrite or re-verify an OpenELIS Global user manual page ("document this feature", "write the manual page for X", "update the page for 3.4", "how-to for OpenELIS", "concept page"), to review a page against the screen, or to clear or promote a reviewed page into the live manual. It holds the one rule (document only verified behavior), the evidence tiers, the page outline, the review gate and promotion, and the drift contract every page registers.
---

# Author an OpenELIS user manual page

Produces a Confluence-bound manual page for an OpenELIS feature or workflow: an At-a-glance
table, numbered steps with real figures, a field reference, tips, Related links and a feedback
line. The other skills in this plugin do the steps around it:

| Step | Skill |
|---|---|
| Capture figures and the walkthrough video | `openelis-qa:qa-evidence` (manual media mode; routes in its `references/routes.md`) |
| Lint, audit and grade | `manual-lint` |
| Publish to Confluence with images, labels, WIP note | `manual-publish` |
| Watch the page for UI drift afterwards | `docs-freshness` (via the drift contract this skill registers) |
| Translated twins (French, Indonesian, Spanish) | `translation-refresh` |
| Close out: project doc and triage bench | `bench-sync` |

UI wording: compose from existing strings with the `openelis-ui-vocabulary` skill; the
documentation spine (Epic, Feature Doc, spec registry) is described in the `openelis-design`
skill's `references/docs-spine.md`.

Read `references/style.md` before drafting and `references/conventions.md` before publishing.
Never write an em dash (organization rule; the plugin's hooks refuse them in publish payloads).

## The one rule

**Document only shipped, verified behavior, never the spec.** Many OpenELIS designs are specced
but not built, or built differently. Before writing any step, confirm it on a live instance. If a
capability exists only in an FRS, PR, Jira ticket or DTO, leave it out or list it under "Not yet
available". When unsure, drive the instance and watch what happens.

## Evidence tiers (read `references/evidence-tiers.md` once per session)

| Tier | Means | Wording licence |
|---|---|---|
| **DRIVEN** | You performed the action on a live instance and saw the result | Describe the outcome |
| **OBSERVED** | You saw the rendered screen (or a screenshot) but did not act | Describe only what is visible |
| **INFERRED** | You read it in an FRS, PR, DTO, spec or ticket | Not manual content. Drive it or mark it unverified |

Three failures cause almost every wrong page: writing from the model instead of the screen,
missing Carbon controls with a narrow DOM query, and concluding a feature is absent from a guessed
endpoint. **Open and look at every figure before writing a word about that screen.**

## Where to verify

- **testing.openelis-global.org** is the evidence instance for manual pages and drift contracts.
- **pngtest.openelis-global.org** for QA surfaces (EQA, QC) and anything testing lacks
  (environmental and vector sample types). It is a test server: change and seed data there
  without asking.
- indonesiademo is decommissioned. Confirm the feature is deployed on the instance you chose
  (menu entry or a real endpoint) before writing anything.
- Seed realistic data (plausible names, no `DOC-` or test prefixes) and leave it in place.
- Test servers and logins: the QA project doc `claude/qa-testing-servers.md`, or the
  openelis-qa plugin's `qa-run` skill `references/servers.md`.

## Workflow

0. **Resolve the spine.** Find the owning OGC Epic and its Feature Doc child (create the Feature
   Doc if the automation did not). Read the FRS and design-gallery preview as background only:
   the FRS says what to look for; the instance says what is true. Docs are owed once the Epic is in
   Acceptance.
1. **Check for an existing page.** CQL search the space (`space = OG AND title ~ "..."`) and the
   landing page 1326972929. Where a page exists, keep its ID and rewrite it (links are by page ID);
   the old text moves to LEGACY Versions (see `references/conventions.md`).
2. **Scope and verify.** Name the routes, drive the workflow end to end, and note required
   fields, gates (a Save that stays disabled until X), messages, and anything that differs from the
   spec.
3. **Capture** with `openelis-qa:qa-evidence` in manual media mode: one figure per step that opens
   a new screen or dialog, uses a hard-to-find control, or shows a state the reader must recognize;
   plus the walkthrough video for multi-screen workflows. Viewport shots, populated data, PII
   masked. Cropping and docx details: `references/figures-and-docx.md`.
4. **Read every figure**, then draft each step from its figure, naming the controls, columns and
   states the figure shows.
5. **Outline first for big workflows.** For a workflow spanning three or more pages, show Casey
   the outline (At a glance, step list, planned figures) before drafting prose.
6. **Draft** in the shape in `references/outline.md`, as Confluence storage XHTML with
   `{{IMG:file.png}}` tokens and an `images/` folder (the publisher's input). A Word file is made
   only when Casey asks for one (docx skill; `references/figures-and-docx.md`).
7. **Lint** with `manual-lint`. Errors block; a warning stands only with a reason.
8. **Review gate**: run it with the `page-reviewer` agent (fresh eyes, not the author), giving it
   the draft, the figures and the instance. See `references/review-and-promotion.md`.
9. **Publish** with `manual-publish`: straight into its live folder with the yellow Work in
   progress note naming the review ticket and the `doc-in-review` label (Casey, 13 Oct 2026).
   Planning pages stay in the review area 1189609473.
10. **Register the drift contract** in `docs-manual/contracts.json` (`references/contracts.md`),
    anchors picked from the figures.
11. **Close the loop**: Feature Doc issue links the page by numeric ID; a review sub-task under
    OGC-1271 for Taib; report the page ID for the design spec registry's Docs column.
12. **Close out** with `bench-sync`: project doc in "OpenELIS User Manual", then the bench.

## Page types

Task pages ("How do I...?") are the default. When a task needs more than two or three sentences
of "why", put the model on a separate concept page and link it under Related. Concept pages follow
the same evidence rules. Shapes for both: `references/outline.md`.

## Known defects belong in the manual, carefully

If a shipped screen has a defect a reader will hit, say so in Tips, factually and without
describing it as intended. Every known-defect tip cites its OGC key and is listed in the
contract's `knownDefects`. A defect with no issue gets a spec plus Jira (Casey's preference) before
the tip is published; QA filing goes through the openelis-qa plugin's `qa-file-bug`. Never invent
an untested workaround. Exception: dates shown one day off (timezone) are tracked elsewhere; no
tips, no bugs.

## Review and promotion (details in `references/review-and-promotion.md`)

- The verdict is a label plus a stamp, never a title suffix: `doc-verified` plus
  `verified-vX-Y-Z` (hyphens: labels cannot hold dots), or `doc-blocked`.
- Taib records a passed review as a text stamp at the top of the page and moves his OGC-1271
  sub-task to Done. Clearing a page means: remove the Work in progress note, normalize the stamp
  to `verified-vX.Y.Z`, set the labels, remove `doc-in-review`, update the provenance status line,
  drop "In review" from the landing page row. Ask Casey before clearing a batch.
- An overview page is cleared only when every step page it links is cleared.

## Reader testing

For the most used pages (order entry, results, validation, patient search, QC, EQA), take any
chance (trainings especially) to give one or two real users the page and a task, without help, and
log every stall. Record it in the contract's `readerTest`; page fixes go on the bench.

## Definition of done

- Every step verified live, or explicitly marked unverified; every step's prose checked against
  its own figure, control by control.
- Figures legible, captioned, with real alt text; PII masked; walkthrough video for multi-screen
  workflows.
- Lint clean (errors none, warnings justified); no em dashes; feedback line present.
- Published with the right parent, WIP note and labels; landing page row added by page ID.
- Drift contract registered with spine fields, `docType`, `audience`, `updateTrigger`, `grade`.
- Feature Doc linked, review sub-task exists, spec registry Docs column reported.
- Project doc written and the triage bench synced (`bench-sync`).
