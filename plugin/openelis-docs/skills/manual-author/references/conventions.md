# Casey's conventions for the OpenELIS manual

Decisions Casey has made, with dates where known. They override older text in any skill. When
Casey sets a new one, add it here (and to `manual-lint`'s Terms rule if it is a term).

## Where pages live

- One Confluence space, OG. Landing page: 📖 User Manual 1326972929 (links every page by ID).
  Folder and page IDs: `manual-publish` skill, `references/confluence.md`.
- Pages waiting for review go **live now** in their folder, marked work in progress (yellow note
  naming the review ticket, label `doc-in-review`, "In review." on the landing page). Planning and
  authoring-guidance pages stay in the review area 1189609473 (13 Oct 2026).
- Quality pages (EQA, QC, alerts, accreditation) live in the Quality assurance folder 1706098877
  of the End User Manual.
- Pre-release features (built on pngtest, not merged) stay in the review area with a "Pre-release"
  note until merged and checked on a release build (example: Microbiology V2, OGC-1383).

## Replacing and merging pages

- When a new page replaces a legacy "PART n" page, the PART page moves to LEGACY Versions
  1657864193 (kept for sites on old versions) and the new page links to it by ID. Casey creates
  new Legacy folders himself.
- Merges keep the **older page ID** and paste the newer content in, because manual links are made
  by page ID. The superseded copy gets a "Merged into ..." note.
- A page rewritten for a new release keeps its ID; the previous text is saved as a new page in
  LEGACY Versions (as Organizations 3.2.x was kept as 1705541782 on 13 Oct 2026).
- Never delete a manual page: archive it. (Translated pages likewise go to their language's
  "previous versions" folder.)

## What to document

- The manual documents the **Test Catalogue Management** editor, never the legacy test editor
  under `/MasterListsPage/TestModifyEntry`.
- EQA is documented as two pages, provider side and participant side; samuel's "EQA User Guide"
  doc is reference material for them, not a page to replace.
- Dates shown one day off (timezone shift) are a known issue tracked elsewhere: no bugs, no tips.

## Instances and data

- testing.openelis-global.org is the evidence instance; contracts point there. Re-point any
  contract still aimed at another base rather than checking it separately.
- pngtest.openelis-global.org is a test server: make changes there without asking and seed what a
  capture needs. EQA and QC are verified and captured there.
- Screenshots look realistic: plausible real-world names, no `DOC-` or test prefixes. Seeded data
  is left in place.

## Terms (also in `manual-lint`)

- Lab Number everywhere (never Accession Number; "Lab No." only in tight column headers).
- Lab Unit (never Test Section or Test Unit).
- Sex, never gender: OpenELIS does not collect gender.
- "Reference ranges" is the umbrella that includes valid and critical ranges; "Normal range"
  means only the normal values.
- Main menu (never sidebar or left nav).

## Work habits

- Casey does not make code changes himself: for a product fix, write a spec plus a Jira issue
  rather than a code PR, and prefer one Epic the developer slices over many pre-split stories.
- Every finished doc ends with a project doc in "OpenELIS User Manual" and a triage bench sync.
- No em dashes anywhere. Never print, paste or commit a credential.
