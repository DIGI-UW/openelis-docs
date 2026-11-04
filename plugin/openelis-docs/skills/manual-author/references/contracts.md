# Provenance and drift contracts

Every page registers a contract in `docs-manual/contracts.json` (in the openelis-docs repo; on
Casey's Mac the same folder is reached as `~/Documents/OpenELIS QA/docs-manual`). The weekly drift
run (`docs-freshness`) visits each contract's routes and checks its anchors, so a shipped page
watches itself: if the screen changes, the triage bench names the section and the missing control.

Back up the file before editing it (`contracts.json.bak-YYYYMMDD-<reason>`), edit with a short
script rather than by hand, and validate the JSON afterwards.

## Fields

| Field | Meaning |
|---|---|
| `id` | Stable contract id, kebab-case |
| `title` | Page title |
| `confluencePageId` | Numeric page ID |
| `manualDoc`, `captureSpec` | Source files (storage XHTML, capture spec in the QA repo) |
| `jiraEpic`, `featureDoc`, `frs` | Spine: OGC Epic key, Feature Doc key, design-gallery permalink |
| `base` | Instance the page documents (testing.openelis-global.org unless Casey says otherwise) |
| `capturedVersion`, `capturedDate` | What and when the figures were captured against |
| `routes[]` | `{ path, anchors[] }`: headings, labels and buttons visible on initial load |
| `uiPaths[]` | Frontend source folders, used by the commit-impact check |
| `retired` | `true` when the page moved to LEGACY Versions; the run skips it |
| `notes` | Free text |

**Pick anchors from the figure, not from memory.** An anchor that is not on the screen fails the
check forever and trains everyone to ignore it. Testing renders en_GB strings (Organisation,
Analyser), so keep anchors spelling-neutral. Wizard-gated routes deep-link through
`{{ORDER_IN_PROGRESS}}`; a redirect scores as a route error, which is correct.

## Inventory fields (fill on every page you author or re-verify)

| Field | Values | Purpose |
|---|---|---|
| `docType` | `task` · `concept` · `reference` · `overview` | Keeps similar titles apart; shows missing concept pages |
| `audience` | `end-user` · `admin` · `implementer` | Matches the routing folder |
| `updateTrigger` | `release` · `scheduled` | Task pages change with their screens; concept pages are reviewed on a cycle |
| `grade` | `A` · `C` · `F` | First impression from the `manual-lint` rubric; not a review verdict |
| `gradedDate` | `YYYY-MM-DD` | When `grade` was set |
| `rot` | `true` · `false` | Redundant, outdated or trivial: merge, move to Legacy, or delete |
| `knownDefects[]` | `{ "ogc": "OGC-1234", "summary": "..." }` | Every known-defect tip; the bench checks whether each is closed |
| `readerTest` | `{ "date", "who", "findings" }` | Last time a real user followed the page |

Do not backfill grades in bulk from memory: grade a page only after reading it.

## Drift statuses (from `drift-report.json`)

- **ok**: anchors present, version matches.
- **review**: instance version differs from `capturedVersion`; recheck when convenient.
- **drift**: a documented control is gone; recapture and rewrite, then bump `capturedVersion`.
- **error**: route failed or redirected; check the contract and the instance before calling it
  drift.
