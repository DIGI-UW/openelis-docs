# Page shapes

## Task page (the default)

In this order:

1. **Title**: the task in sentence case ("Enter and save results"). Admin pages start
   `Admin: ` (colon, never a dash). No `PART N` numbers (that scheme belongs to the legacy
   monolith).
2. **Type line** (italic): *How-to · Laboratory staff* (or Administrators).
3. **Version line**: which release the page describes, and a link by page ID to the legacy page
   for sites on older releases when one exists.
4. **At a glance**: a two-column label/value table, before the steps. Five rows, in order:
   - **Purpose**: the task in the reader's terms ("Register a new patient so they can be linked to
     test orders").
   - **You'll end up with**: the outcome ("A saved patient record, searchable when creating
     orders").
   - **Who does this**: the typical role, always with "Access is set by user permissions and can be
     configured by your administrator." Never publish a permission matrix: access is configurable
     per site.
   - **Before you start**: data and materials needed.
   - **Where**: the menu path (Main menu > ... > ...).
   Emit it with no `<thead>`: every row in `<tbody>`, label cell `<th>`, value cell `<td>`
   (a `<thead>` makes Confluence promote row 1's value cell to a header).
5. **Overview** (optional): two to four sentences on the workflow shape, when At a glance is not
   enough.
6. **Steps**: numbered, imperative, one instruction per step. A figure with a caption when the step
   opens a new screen or dialog, uses a hard-to-find control, or produces a state the reader must
   recognize. A step that only fills a field visible in the previous figure relies on that figure
   and names the control exactly as it shows. Never screenshot a message just to show its text:
   quote it in the prose so it can be searched and translated. Call out required fields and gates
   ("Save & Next stays disabled until...").
7. **Field reference**: a table of the key fields with notes.
8. **Tips and notes**: shortcuts, gotchas, known defects with OGC keys.
9. **Not yet available** (when relevant): adjacent things a reader will look for and not find,
   named plainly so they stop looking.
10. **Related**: links by page ID to the concept page and to the next task.
11. **Feedback line** (word for word from `style.md` section 8).
12. **Provenance**: instance, version, date, who verified, which steps were driven, observed or
    unverified, the review ticket, and the drift contract id.

## Concept page

No At-a-glance table and usually no figures. In order: an italic type line (*Concept ·
audience*); the version line; **In short** (three or four sentences a reader could stop after);
sections that explain the model, using tables for statuses and decisions rather than prose lists;
**Related**; the feedback line; **Provenance** naming the verified pages and drive dates the page
was assembled from, what was only observed, and what to re-check before review.

A concept page may be assembled from DRIVEN evidence recorded on other verified pages without
driving the screens again, but it inherits their gaps: anything those pages mark observed or
unverified stays out or is labelled the same way. Link unpublished concept pages to each other with
`[[CONCEPT-...-ID]]` placeholders and replace them with page IDs on publish (lint fails while any
remain).

## Overview page

A short page that orders a multi-page workflow (environmental surveillance, test catalog). It
links each step page by ID with one line on what it helps the reader do. It is cleared from review
only when every page it links is cleared.

## Work in progress note (pages waiting for review)

A yellow note panel at the top:

> **Work in progress.** This page is published before its review is finished so you can use it
> now. It is being reviewed under OGC-NNNN, so details may still change. If something on your
> screen does not match, add a comment to this page.

Plus the label `doc-in-review`, and "In review." at the end of the page's row on the landing page
1326972929.
