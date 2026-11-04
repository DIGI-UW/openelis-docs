# Review gate, clearing and promotion

## Recording a verdict

Never encode review state in a page title. Title suffixes are not queryable, drift in case, lose
provenance and force renames that break title-bound links.

**Labels** (queryable, survive renames):
- `doc-in-review`: published live as work in progress, review ticket open.
- `doc-verified`: a reviewer drove the workflow live and it passed.
- `verified-v3-4-0`: the version verified against, hyphens for dots (Confluence labels cannot
  contain dots, so `verified-v3.4.0` can never exist).
- `doc-blocked`: a step could not be reached; resolve before clearing.

Pages awaiting a clear: `label = "doc-in-review" AND space = OG AND type = page`.

**Provenance stamp** at the top of the provenance section:

> **Verified by** <name> · **Date** <YYYY-MM-DD> · **Instance** <testing|pngtest> ·
> **OpenELIS version** <x.y.z>
> Gates applied: workflow sentence, first real step, screen fidelity, step and figure fidelity,
> driven end to end, process gates, style and translation readiness.

**How Taib records a pass (since Oct 2026).** Review sub-tasks sit under OGC-1271. Taib adds a text
stamp at the top of the page ("doc-verified + verified-v3.4.0", spellings vary) and moves his
sub-task to Done. He does not change labels. The stamp plus a Done ticket is the verdict; clearing
applies the labels for him.

## Review gate (fresh eyes: the `page-reviewer` agent or a second person, never the author)

Re-derive, then diff. First state the goal, the minimal real workflow to reach it, and the steps
and figures that workflow needs. Then diff the draft against that:

1. **One-sentence workflow.** Write the workflow as one sentence; every step serves it. Cut setup
   that belongs to another page.
2. **First real step.** Delete everything before the first action unique to this workflow (menu
   navigation, prerequisite configuration documented elsewhere).
3. **Screen fidelity.** For each step, list the controls, columns, statuses and help text visible
   in its figure, and check the prose names the same things and invents nothing. A noun in the prose
   that is absent from the figure probably came from an FRS or a DTO. Worth more than all other
   gates together.
4. **Step and figure fidelity.** Every figure shows the action or state of its step. No generic
   landing pages, empty lists or mismatched selections.
5. **Driven end to end.** A step that could not be reached (gated dialog, flag off) is a blocker:
   label `doc-blocked`, never carry prose over from an older draft or the spec.
6. **Process gates.** Built in the outline shape; existing page ID reused; drift contract
   registered.
7. **Workflow completeness** (overview pages): every linked step is cleared, or the overview waits.
8. **Style and translation readiness.** `manual-lint` clean; UI labels match the screen and the
   en.json string; no version numbers in body prose; link text names its target; known-defect tips
   cite OGC keys; no em dashes.

Mark every finding blocking or non-blocking. Gates 3, 4 and 5 are blocking. Style nits that do not
change meaning are non-blocking: fix in the same pass, or log and move on. Only Casey or the
assigned reviewer can block a page.

## Clearing a reviewed page (WIP to verified)

Ask Casey before clearing a batch; list the candidates first (ticket Done and page stamped).

1. Dump each page body first (`*.before.xhtml` or ADF JSON) so the change can be undone.
2. Remove the Work in progress panel; keep the reviewer's stamp, spelling normalized to
   `verified-vX.Y.Z`.
3. Labels: add `doc-verified` and `verified-vX-Y-Z`; remove `doc-in-review`.
4. Provenance status line: "Reviewed under OGC-NNNN; cleared from review <date>."
5. Remove any em dashes from body text. Leave dashes inside `ri:content-title` link attributes
   that must match a real page title.
6. Drop "In review." from the page's row on the landing page 1326972929.
7. Record it in the project doc and sync the bench.

## Promotion from the review area (older drafts and planning pages)

Pages still parented under the review area 1189609473:

1. Confirm the verdict (labels and stamp). No verdict, no promotion: ask the reviewer.
2. Overview subtrees: re-parent unverified children back to 1189609473 first.
3. Route by audience: end-user pages to the End User Manual folder 1329758211 (into its topic
   subfolder); `Admin: ` pages to the Administrator Guide folder 257458193; Quality pages to the
   Quality assurance folder 1706098877. Keep an overview with its own domain's pages.
4. Move and rename in one ADF write (`manual-publish`). Sentence case; no suffixes; no `PART N`.
5. Re-point Include macros on the moved page and any page that transcludes it (they are
   title-bound), then load both and confirm they render.
6. Link the page from the landing page by numeric ID.
7. Close the loop: Feature Doc issue links the page by ID with the contract id; report the page
   ID for the spec registry's Docs column (the design thread owns that file).
