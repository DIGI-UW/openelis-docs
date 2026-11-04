---
name: manual-publish
description: This skill should be used whenever OpenELIS documentation is written to Confluence, such as publishing a new manual page with its figures, updating, moving, renaming, labelling or clearing an existing page, adding the Work in progress note, editing the landing page, or publishing any page in the OG or DEV spaces ("publish it", "push to Confluence", "put the figures on the page", "move it to the Administrator Guide", "fix the landing page"). It holds the publisher script, the ADF-only edit rule, the Confluence IDs and the publishing gotchas.
---

# Publish OpenELIS documentation to Confluence

Atlassian site `uwdigi.atlassian.net` (cloudId `57b4e32d-23d4-4a71-8985-82ac0274d145`), manual
space **OG**. IDs: `references/confluence.md`.

Publishing is public. The plugin's hooks ask Casey before any publish script runs and refuse an em
dash in a payload; a refused call is a prompt to fix the content, not to route around the hook.

## Pick the path

| Job | Path |
|---|---|
| New page with figures, or a full rewrite of one | `scripts/confluence-publish.py` on Casey's Mac (REST; uploads attachments) |
| Small edit to an existing page (text, a table row, a note, a move or rename) | Atlassian MCP, **ADF only** |
| Labels, content properties, many pages at once | REST script on the Mac (`docs-manual/publish/`), dry run first |
| A page with no figures that does not exist yet | Atlassian MCP `createConfluencePage` is fine |

The cloud sandbox cannot reach `uwdigi.atlassian.net` directly (egress policy); REST scripts run
on Casey's Mac through the Control-your-Mac connector (`osascript` `do shell script`). Credentials
live in `~/.openelis/confluence.env` and are read by the scripts; never print, paste or commit them.

## The publisher (`scripts/confluence-publish.py`)

The canonical copy is in this skill; `docs-manual/publish/confluence-publish.py` in the repo is
kept identical by the build check. Input is Confluence storage XHTML with each figure as a token on
its own line, `<p>{{IMG:01-search.png}}</p>`, and an `images/` folder holding those PNGs.

```bash
cd ~/Documents/"OpenELIS QA"/docs-manual/publish
python3 confluence-publish.py --page <pageId> --xhtml <page>.xhtml --images <dir> --dry-run
python3 confluence-publish.py --page <pageId> --xhtml <page>.xhtml --images <dir>
python3 confluence-publish.py --create --space OG --parent <folderOrPageId> \
  --title "<Title>" --xhtml <page>.xhtml --images <dir>
```

`--images` is only needed when the XHTML has figure tokens; `--title` renames on update; `--message`
sets the version message (say what changed). Images are uploaded as attachments (matched by file
name, so reruns update in place) and sized
with `ac:width` (max 1020 px by default, never upscaled; `--max-width` overrides). Long runs: start
with `nohup ... > pub.log 2>&1 &` and poll the log, because osascript calls time out.

**Use the publisher. Do not place images by hand.** Casey has said outright he does not want
figures placed by hand; a whole session was once lost uploading fourteen figures one at a time.

Before running it: lint the XHTML (`manual-lint`), and check the At a glance table has no
`<thead>`.

## Editing existing pages through the MCP: ADF only (hard rule, enforced by a hook)

Use `contentFormat: "adf"` on both the read and the write of `updateConfluencePage`. The HTML path
silently promotes the first table row's value cell to a header, strips `data-local-id`s (they
anchor inline comments), drops image alt text and borders, and on legacy-editor pages has recorded
a new version while keeping the old body. Markdown replaces the body wholesale and deletes every
figure.

- `body` is required, so every rename or move rewrites the body: read ADF, change only what is
  needed, write ADF.
- Guard every write: assert the read returned the `id` you asked for.
- Work serially. Never two page operations in one message, never parallel agents on the tree.
- Titles take a raw `&`, not `&amp;`.
- Folders are invisible to the page tools (404). You can set `parentId` to a folder; list a folder
  with CQL `parent = <id> AND type = page`.

## Links, labels and notes

- Link by numeric page ID (`/wiki/spaces/OG/pages/<id>` or the tiny link), never by title: titles
  change on promotion and title-bound links turn into "create page" links. Include macros are
  title-bound: avoid them, or re-point and check them after any rename.
- Labels cannot contain dots: `verified-v3-4-0`. Set them by REST (`docs-manual/publish/labels.py`)
  or in the UI; the MCP has no label tool.
- Work in progress note and landing-page "In review." marker: manual-author
  `references/outline.md`. Clearing a reviewed page: manual-author
  `references/review-and-promotion.md`.
- Check for an existing page before creating one (CQL on the title). Confluence rejects an exact
  duplicate title in a space; a near match quietly becomes a second page.

## Gotchas

- **Token scope.** A Jira-only API token authenticates as anonymous on Confluence: reads work
  (the space is public) and every upload fails 403 "not permitted to create attachments". Check
  `GET /wiki/rest/api/user/current` through a script on the Mac; `"type":"anonymous"` means Casey
  needs a new token with `write:attachment:confluence`. Do not retry.
- **Translated pages** are published by `translation-refresh`, never by this skill, and never over
  a human edit.
- Dump a page body before a risky write (`<id>.before.xhtml` or ADF JSON) so it can be restored.
- Fallbacks when REST cannot run: Word import (Insert > Import Word document), or publish prose with
  empty figure slots and a grey "drop image: ..." hint for Casey.

After publishing: register or update the drift contract (manual-author), then `bench-sync`.
