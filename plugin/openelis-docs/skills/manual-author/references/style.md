# OpenELIS user manual style guide

Read this before drafting any manual page. The mechanical rules are enforced by Vale (the manual-lint skill's `lint/` folder);
the rest are checked in Review gate 8. Sources: Write the Docs documentation principles, Google's
Open Docs project (CC BY 4.0), GitHub Docs' guidance on translation-friendly writing, and Casey's
own OpenELIS conventions.

Contents: 1 Principles · 2 Terminology · 3 Sentences and structure · 4 Write for translation ·
5 Version-agnostic prose · 6 Links · 7 Screenshots and captions · 8 Feedback line · 9 Linting

## 1. Principles

- **Wrong is worse than missing.** Incorrect documentation does more harm than a gap. This is why
  the evidence tiers exist; it is also why a page says "not yet available" instead of guessing.
- **Skimmable.** Readers jump to the step they need. Descriptive headings, one instruction per
  step, and the key concept at the start of every paragraph and list item.
- **Complete within its scope.** If a page covers the fields on a screen, it covers all of them,
  or states up front that it covers only some. A page that documents half the fields is worse than
  one that documents none.
- **Some repetition is fine.** Repeat a prerequisite in a sentence rather than forcing a reader
  to another page for it. Repeat whole procedures never: link instead.

## 2. Terminology

Use the words the rendered screen uses, exactly. When a label comes from an i18n string, the
English value in `en.json` is the source of truth (see the `openelis-ui-vocabulary` skill); the
translated manuals match the translated UI only if the English manual uses the real label.

Fixed terms (Casey's conventions):

| Write | Never write |
|---|---|
| Main menu (Main menu → Order → Add Order) | left menu, side menu, sidebar, left nav |
| Lab Number ("Lab No." only in a tight table header) | Accession Number, accession no. |
| Lab Unit | Test Section, Test Unit |
| sex | gender (OpenELIS records sex only) |
| reference ranges (the umbrella: valid range and critical range) | normal range, unless you mean only the normal values |

Format UI labels in **bold** exactly as shown, including capitalization ("click **Save & Next**").
Page titles are sentence case. Do not add `PART N` numbers.

## 3. Sentences and structure

- Imperative voice for steps: "Enter the Lab Number", not "The user should enter".
- One action per step. If a step has "and then", split it.
- Lead with the goal or location, then the action: "In the **Sample** section, select the sample
  type."
- Name the result of a step only when it was DRIVEN (see the evidence tiers in SKILL.md).
- Drop filler: simply, just, easily, obviously, please note, in order to (use "to"), as per.
- Headings name the task or the thing ("Edit a result after validation"), never "Overview 2" or
  "More information".

## 4. Write for translation

Every English page is machine-translated by Lango and then reviewed. Each ambiguity in English
becomes an ambiguity in French, Spanish, Indonesian and Chinese. Writing that translates well is
the same as writing that reads clearly; these rules make that concrete.

- **Short sentences.** Aim for 25 words or fewer. Split long conditionals into two sentences.
- **No idioms or phrasal verbs where a plain verb exists.** "start" not "kick off", "fill in" →
  "enter", "out of the box" → "by default", "under the hood" → cut it.
- **No Latin abbreviations.** "for example" not "e.g.", "that is" not "i.e.", and avoid "etc."
  (end the list or say "such as").
- **No vague pronouns.** Do not start a sentence with "It", "This" or "That" referring back to a
  previous sentence; name the thing. "This opens..." → "The **Search** button opens...".
- **Concrete numbers and conditions.** "after three failed attempts", not "after several attempts".
- **Same word for the same thing, every time.** Do not alternate "sample" and "specimen", or
  "order" and "request", for variety. Use the term the screen uses.
- **Dates in an unambiguous form** (14 March 2026 or 2026-03-14), never 03/14/26.
- **No text baked into images** other than the UI itself. Callouts, arrows with labels, and
  explanatory text go in the caption or prose, where they can be translated.
- **No culture-specific examples.** Use neutral, realistic lab data (see section 7).

## 5. Version-agnostic prose

Version numbers belong in labels (`verified-v3-3-0`), the provenance stamp, and `contracts.json`,
not in body text. Body prose describes how the product works now. Exceptions:

- The **version line** near the top of the page ("This page describes OpenELIS 3.3.0."), which the
  User Manual landing page promises readers. One per page, in one place.
- A **Legacy** pointer may name the version range the legacy page covers.
- A **Not yet available** item says "planned", never a target release.

If a behavior differs by version and both versions are live at sites, that is a Legacy page
question, not an "if you are on 3.2" paragraph.

## 6. Links

- Link by **numeric page ID**, never by title slug (see SKILL.md).
- Link text names the destination: "see [Validate results](...)", never "click here", "this page"
  or a bare URL.
- Every page links to its concept page (if one exists) and to the next task in the workflow under
  **Related**.

## 7. Screenshots and captions

**When a step gets a figure.** A figure earns its place when the step opens a new screen or
dialog, uses a control that is hard to find, or produces a state the reader must recognize (a
status, a flag, a disabled button). A step that only fills a field already visible in the previous
figure can rely on that figure. Screenshots are expensive to maintain and to localize, so every
one should be doing work.

**What a figure is not for.**
- Do not screenshot a message or confirmation dialog just to show its text. Quote the message in
  the prose: quoted text can be searched, copied, read by a screen reader, and translated.
- Do not use a generic landing page or an empty "no records" screen.

**Capture rules.**
- Crop to the area the step describes; prefer viewport captures over full-page strips.
- Seed realistic data with plausible names. No "DOC-", "TEST-" or similar prefixes; seeded data
  stays in place.
- Mask PII.
- No manual annotations baked into the image (see section 4).

**Captions** describe the screen for the reader ("The Add Order page with the Sample section
expanded"). Never include "captured", "screenshot", tool names or other provenance wording.
**Alt text** says what the figure shows and why it matters for the step, not the file name.

## 8. Feedback line

Every page ends with one line telling the reader where to report a problem with the page. Use the
route the User Manual landing page (1326972929) already gives readers, word for word:

> *Something on this page out of date or unclear? Add an inline comment on this page, or post in
> [OpenELIS Talk](https://talk.openelis-global.org).*

Inline comments are read when a page is reviewed or re-verified; reader reports go on the
Documentation triage bench like any other finding. If the landing page's feedback route changes,
change this line to match.

## 9. Linting

The manual-lint skill's `lint/` folder holds a Vale configuration and the `OpenELIS` rule set:

| Rule | Level | Catches |
|---|---|---|
| `OpenELIS.Terms` | error | Banned terms from section 2 (sidebar, Accession Number, Test Section, gender) |
| `OpenELIS.Filler` | warning | simply, just, easily, in order to, as per, please note |
| `OpenELIS.Translation` | warning | Latin abbreviations, common idioms, vague sentence-initial pronouns |
| `OpenELIS.Versions` | warning | Version numbers in body prose |
| `OpenELIS.LinkText` | error | "click here", "this page", "here" as link text |
| `OpenELIS.Placeholder` | error | Any unresolved `[[...]]` placeholder, such as a page ID still to fill in |
| `OpenELIS.SentenceLength` | suggestion | Sentences over 25 words |
| `OpenELIS.EmDash` | error | Any em dash (organization rule; use a colon, comma or parentheses) |

Run it against the storage XHTML (or a Markdown export) before delivering a draft:

```
cd lint
vale --config .vale.ini ../path/to/<section>.xhtml
```

Install: `brew install vale` on Casey's Mac; in the sandbox, download the Linux release from
github.com/errata-ai/vale (tested with v3.9.1). Errors block delivery. A warning may stand only with
a reason (for example, the version line at the top of the page, or a version number inside a quoted
error message). Extend the term list in
`lint/styles/OpenELIS/Terms.yml` whenever Casey sets a new convention.
