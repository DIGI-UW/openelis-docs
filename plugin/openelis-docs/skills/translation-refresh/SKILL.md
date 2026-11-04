---
name: translation-refresh
description: This skill should be used for the translated OpenELIS manual (French, Indonesian, Spanish), such as "refresh the French pages", "which translations are stale?", "translate the new page into French", "fix the French tree", "check the French UI labels", "start the Spanish manual", reading bench-translations.json, or any change to a translated page. It holds the mirror and scope rules, how to read translation freshness, the segment-level refresh kit, and the rule never to republish over a human edit.
---

# Translated manual: freshness and refresh

The English manual is the source. Each language has a mirrored tree in the same space (OG), linked
page to page by ID, translated by Claude with a glossary, and tracked by the docs spine.

Never write an em dash. Never print a token. Never delete a translated page: archive it to the
language's "previous versions" folder.

## Languages

Configured in `docs-manual/fr/langs.json`; pick one with `OE_LANG=<code>` (default `fr`). Every
script in `docs-manual/fr/` honours it.

| Code | Home | Manual root | Glossary | Notes |
|---|---|---|---|---|
| `fr` | 1701970059 | 1641447437 | `refresh/glossary-fr.md` (fr-v1, Confluence 1704362069) | Live since 9 Oct 2026; French screenshots on the most used pages only |
| `id` | 1733722115 | 1733492739 | `refresh/glossary-id.md` (id-v1) | Wave 1 live 22 Oct 2026; in Indonesia OpenELIS is called SILNAS, keep it |
| `es` | not created | not created | (es-v1 planned) | Next after Indonesian |

Scope: verified or live English manual pages, install and ops pages, landing pages and
implementation guides (`scope*.json` plus pages labelled `doc-verified`). Review-area drafts are not
translated until they are live. Indonesian and Spanish leave out the Madagascar implementation
guides and legacy PART pages. Madagascar's `fr_MG` UI strings are out of scope. Reviewers are
proposed on the triage bench only, never named on pages.

## Structure rules (Casey, 20 Oct 2026)

- The translated tree mirrors the English tree: every English page and folder has one twin in the
  same place under the language home. Archives map to the language's previous-versions folder.
- Pages are linked by page ID (content property `openelis-translation`: sourceId, sourceVersion,
  glossary; Lango `adapps-lango-lang` for the flag switcher). Never by title.
- Translated pages are kept together under their language home, never next to the English pages.
- Lango stays installed for its switcher; its automation stays off (it would overwrite reviewed
  translations and delete pages sites still use).

## Read freshness (`bench-translations.json`, `bench-translations-id.json`)

Written by `fr/translation-freshness.py` (run by `run-d.sh`, or alone with `OE_LANG=<code>
python3 docs-manual/fr/translation-freshness.py` through nohup):

- **wait for English**: the English contract is in drift or error. Do not translate yet.
- **retranslate changed sections**, **copy figures**, **bump version only**: refresh with the kit
  below (the kit reuses unchanged text, so figure-only and version-only cases cost almost nothing).
- **missing**: a tracked English page with no twin. Translate it fully: add it to the scope file
  and `build*/plan.json`, then `fr-publish.py pages content --only <id>`.
- **orphan**: the English page was deleted or archived; move the twin to previous versions
  (`fr-archive.py`).
- **tree misplaced**: run `fr-tree.py` (dry run), check the moves, then `fr-tree.py --apply`. An
  unmapped English parent needs a `folders` twin or a `parentOnly` target in the state file first.
  Never map a parent to a node that is itself a pair.
- **labels, new since baseline**: bold strings on a translated page that are not current UI strings.
  Prose bold (headings, notes) is noise. Real findings are old wording (French: Ordonnance or
  Commande for a lab order), English menu names, or labels whose string changed in Transifex.
  Labels with no translation at all are Transifex gaps or reference data (OGC-1507).
- **figuresStale**: an English figure was re-uploaded after the translated capture; recapture
  (`openelis-qa:qa-evidence`, French UI) or accept the English figure.

## Refresh stale pages (segment-level kit, `docs-manual/fr/refresh/`)

Unchanged English text keeps its existing translation; only changed segments are translated.

1. On the Mac (osascript, `OE_LANG` set): `python3 fr-fetch.py <ids>` (current English into
   `src/`) and `python3 refresh/fr-fetch-old.py <ids>` (English at the translated version into
   `refresh/old/`).
2. Stage into the sandbox: the kit (`refresh/*`), `refresh/old/<id>.json`, `src/<id>.json`,
   `build*/<id>.json`, `build*/plan.json`, the live UI strings (`tx/<lang>-live.json`) and an English
   UI file (`tests/docs/i18n/en.json`, refreshed from develop if old). Lay them out as ROOT/old,
   ROOT/src, ROOT/build, ROOT/plan.json, ROOT/en.json, ROOT/<lang>-live.json; the kit in its own
   folder (KIT).
3. `python3 KIT/prep.py ROOT <ids>` prints aligned / reused / toTranslate per page and writes
   `ROOT/work/batchNN.json` (about 12k characters each). `aligned: False` means the whole page is
   retranslated; expected after a big English rewrite.
4. Translate each batch with a subagent, in parallel: "Read KIT/BRIEF-REFRESH.md and follow it
   (Indonesian: KIT/TRANSLATOR-id.md); KIT=<path>, ROOT=<path>; your batch is
   ROOT/work/batchNN.json; write ROOT/out/<page>.json and run the validator until it prints OK;
   reply in one line with counts and any terms you decided yourself." Pages with translated
   screenshots drop the English gloss after UI labels; say so in the prompt.
5. Review the translators' term decisions against the glossary and the settled terms in the brief.
   Grep the output for known mistakes (French: "Clear" lane is "sans anomalie"; ordonnance or
   commande for a lab order; any "En français" self-link) and for em dashes. Fix in `ROOT/out`
   before merging. Add new recurring terms to the glossary.
6. `python3 KIT/merge.py ROOT <ids>` writes `ROOT/publish/<id>.json` and `ROOT/publish/plan.json`.
7. On the Mac, back up `build*/plan.json` and the affected `build*/<id>.json` (dated `.bak`), then
   write the publish files into `docs-manual/fr/build*/`. Verify on the Mac (grep a changed
   string): a copy can land stale; write it again if so.
8. **Never republish over a human edit.** Check each page's version history first: an author other
   than the publishing account, or a version message not starting with the language's
   `versionMsg` prefix ("Traduction FR", "Terjemahan ID"), means a person edited it. Stop and ask
   Casey; republishing overwrites the whole body.
9. Publish: `OE_LANG=<code> python3 fr-publish.py content --only <ids>` (nohup; the hook asks Casey
   first). Check the log for WARN lines.
10. Rerun `translation-freshness.py`; expect the pages current. Then reset the label baseline
    (`mv -n labels-baseline*.json labels-baseline-<date>.json`; the next run recreates it).

`fr-banner.py --apply` (yellow "English changed" note on stale pages) runs only if Casey has said
yes on the bench item "Show French readers when a page is out of date?".

## Starting a new language (Spanish next)

The recipe used for Indonesian is in the project doc
`claude/handoff-indonesian-spanish-manual-2026-10-22.md`: language config in `langs.json`, glossary
and translator brief, skeleton tree (`fr-publish.py folders pages`), waves of about ten pages with
Casey looking at two rendered pages before wave 2, then the spine (`run-d.sh` per language, bench
`translations/latest-<code>`).

## Gotchas

- `fr-publish.py content` skips pages already done at the plan version unless `--only` is given.
- The French home 1701970059 is the twin of the space home; the French manual root is a page under
  it, not under the English manual.
- Transifex strings can contain curly apostrophes; quote UI strings as they are, write your own
  text with straight apostrophes.
- A translator may keep an English on-screen label when the UI has no translated string. That is
  correct; note it as a Transifex gap rather than inventing a translation.
- Credentials: `~/.openelis/confluence.env` and `~/.openelis/transifex.env`, read by the scripts on
  the Mac only.

## Close out

Project doc in "OpenELIS User Manual", then `bench-sync` (`translations/latest` for French,
`translations/latest-<code>` for the others; French item ids start with `fr`).
