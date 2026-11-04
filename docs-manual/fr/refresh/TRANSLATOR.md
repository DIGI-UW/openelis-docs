# Translator brief: OpenELIS Global documentation, English to French

You are translating pages of the OpenELIS Global documentation (an open-source laboratory information
system used by national public health laboratories in francophone Africa, Madagascar and Haiti) into
professional French. Readers are laboratory technicians, biologists, lab managers and system
administrators.

## Inputs
- `KIT/glossary-fr.md`: the glossary and rules. Read it fully first and follow it strictly.
- Your batch file `ROOT/work/batchNN.json`: a list of pages. Each page has
  `page` (id), `title`, `segs` (list of `{id, text}`), and `ui` (English UI labels found on that page
  mapped to the exact French interface strings, preferred first).

## Output
For each page write `ROOT/out/<page>.json`:
```json
{"page": "1439072277", "title": "<French title>", "segs": {"s0": "<French>", "s1": "<French>"}}
```
Every segment id of the page must be present. Write one file per page (use Python `json.dump(...,
ensure_ascii=False)` to avoid escaping mistakes). When all pages are done run
`python3 KIT/validate.py ROOT/work/batchNN.json` and fix every problem it
reports until it prints `OK`.

## Segment markup (must be preserved)
Segments contain a small markup. Translate the text between tags; keep the tags.
- `<b>…</b>` bold, `<i>…</i>` italic, `<u>…</u>`, `<s>…</s>`: keep around the equivalent French words.
  You may move them to follow French word order.
- `<code>…</code>`: content must stay **byte-for-byte identical** (code, routes, settings, values).
- `<a n="3">…</a>` link and `<m n="4">…</m>` other formatting: keep each exactly once with the same
  `n`; translate the link text (page titles in link text: translate them).
- `<x n="5"/>` an embedded object (emoji, date, card): keep exactly once, same `n`.
- `<br/>` line break: keep.
- `&amp; &lt; &gt;` are escaped characters: keep them escaped in the output.
- Segments of kind `alt` are image alt text: translate as plain text.

## How to translate
- Bold UI labels: use the French interface string from the page's `ui` map (first option unless the
  context clearly calls for another listed option). On the first occurrence on a page, add the English
  in italics in parentheses after it: `<b>Enregistrer</b> (<i>Save</i>)`. Later occurrences: French only.
  If the `ui` map says "untranslated in UI: keep English", or the label is not in the map and is clearly
  an on-screen label, keep the English label in bold unchanged.
- Menu paths like `Main menu → Results → Results Entry`: "Menu principal →" then UI strings.
- Prose: use the glossary terms. Natural, concise French; not word-for-word. Imperative with *vous*
  for steps.
- Do not translate: code, URLs, file paths, commands, product and standard names, Jira keys, version
  numbers, seed data (patient names, lot numbers), anything inside `<code>`.
- Titles: translate page titles naturally, sentence case (for example "Enter and save results" →
  "Saisir et enregistrer les résultats"; "Admin — Manage providers" → "Admin — Gérer les prescripteurs";
  "PART 8: PATHOLOGY" → "PARTIE 8 : PATHOLOGIE"). Keep "Admin — " prefixes as "Admin — ".
- Older pages written in ALL CAPS headings: keep the capitalisation style.
- Do not add or drop content. Do not summarise. Keep numbers, lists and table cells aligned
  one-to-one with the source segments.
- Do not use em dashes of your own; keep any that are in the source titles.
