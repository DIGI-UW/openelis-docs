# Translator brief: OpenELIS Global documentation, English to Indonesian

You are translating pages of the OpenELIS Global documentation (an open-source laboratory information
system used by national and provincial public health laboratories, including in Indonesia) into
professional, formal Indonesian (Bahasa Indonesia). Readers are laboratory analysts, laboratory doctors,
lab managers and system administrators.

## Inputs
- `KIT/glossary-id.md`: the glossary and rules. Read it fully first and follow it strictly.
- Your batch file `ROOT/work/batchNN.json`: a list of pages. Each page has
  `page` (id), `title`, `segs` (list of `{id, kind, text}`), and `ui` (English UI labels found on that page
  mapped to the exact Indonesian interface strings, preferred first).

## Output
For each page write `ROOT/out/<page>.json`:
```json
{"page": "1439072277", "title": "<Indonesian title>", "segs": {"s0": "<Indonesian>", "s1": "<Indonesian>"}}
```
Every segment id of the page must be present. Write one file per page (use Python `json.dump(...,
ensure_ascii=False)` to avoid escaping mistakes). When all pages are done run
`python3 KIT/validate.py ROOT/work/batchNN.json` and fix every problem it reports until it prints `OK`.

## Segment markup (must be preserved)
Segments contain a small markup. Translate the text between tags; keep the tags.
- `<b>…</b>` bold, `<i>…</i>` italic, `<u>…</u>`, `<s>…</s>`: keep around the equivalent Indonesian words.
  You may move them to follow Indonesian word order.
- `<code>…</code>`: content must stay **byte-for-byte identical** (code, routes, settings, values).
- `<a n="3">…</a>` link and `<m n="4">…</m>` other formatting: keep each exactly once with the same
  `n`; translate the link text (page titles in link text: translate them).
- `<x n="5"/>` an embedded object (emoji, date, card): keep exactly once, same `n`.
- `<br/>` line break: keep.
- `&amp; &lt; &gt;` are escaped characters: keep them escaped in the output.
- Segments of kind `alt` are image alt text, `attr` are expand titles: translate as plain text.

## How to translate
- Bold UI labels: use the Indonesian interface string from the page's `ui` map (first option unless the
  context clearly calls for another listed option). On the first occurrence on a page, add the English
  in italics in parentheses after it: `<b>Simpan</b> (<i>Save</i>)`. Later occurrences: Indonesian only.
  If the `ui` map says "same as English", keep the label unchanged with no gloss. If the label is not in
  the map and is clearly an on-screen label, keep the English label in bold unchanged.
- Menu paths like `Main menu → Results → Results Entry`: "**Menu Utama** →" then UI strings.
- Prose: use the glossary terms. Natural, concise, formal Indonesian; not word-for-word. Address the
  reader as *Anda*; steps in the imperative ("Klik …", "Masukkan …", "Pilih …").
- Do not translate: code, URLs, file paths, commands, product and standard names, Jira keys, version
  numbers, seed data (patient names, lot numbers), anything inside `<code>`.
- Titles: translate page titles naturally, sentence case (for example "Enter and save results" →
  "Memasukkan dan menyimpan hasil"; "Admin: Manage providers" → "Admin: Mengelola penyelenggara").
  Use the "me-" verb form for how-to titles. Keep the "Admin: " prefix. If a source title has an em
  dash ("Admin — X"), write a colon instead ("Admin: X"). Keep leading emoji.
- Older pages written in ALL CAPS headings: keep the capitalisation style.
- Do not add or drop content. Do not summarise. Keep numbers, lists and table cells aligned
  one-to-one with the source segments.
- Never write an em dash (—), not even where the source has one. Use a colon, comma or parentheses
  instead. validate.py does not catch this; check your output with a search before you finish.
