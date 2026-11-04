# openelis-docs

Documentation tooling for [OpenELIS Global](https://github.com/DIGI-UW/OpenELIS-Global-2) and the
**openelis-docs** Claude plugin that drives it. The user manual itself lives in Confluence
([📖 User Manual](https://uwdigi.atlassian.net/wiki/spaces/OG/pages/1326972929)); this repo holds
what keeps it accurate:

| Path | What it is |
|---|---|
| `plugin/openelis-docs/` | The Claude plugin: six skills (author, lint, publish, freshness, translation, triage bench), a page-reviewer agent and hooks. See its [README](plugin/openelis-docs/README.md). |
| `docs-manual/contracts.json` | One drift contract per manual page: routes and the on-screen anchors the page relies on, plus its Jira Epic, Feature Doc and design spec. |
| `run-d.sh` | The weekly freshness run: UI drift against testing.openelis-global.org, commit-to-doc impact, the triage bench summary, then translation freshness per language. |
| `docs-manual/publish/` | `confluence-publish.py` (storage XHTML plus figures to Confluence) and the page sources and one-off scripts used to publish and repair pages. |
| `docs-manual/fr/` | The translated manuals (French, Indonesian; Spanish next): language config, mirror tree tools, the segment-level refresh kit, glossaries and translation state. |
| `docs-manual/*.json` | The latest drift and translation reports the triage bench loads. |

Figures, captures, logs, backups and fetched page copies stay out of git (see `.gitignore`).
Credentials never enter the repo: the scripts read `~/.openelis/confluence.env` and
`~/.openelis/transifex.env` on the machine that runs them.

## How it runs

The drift spec (`tests/docs/drift.check.spec.ts`) belongs to the QA harness in
[DIGI-UW/OpenELIS-QA](https://github.com/DIGI-UW/OpenELIS-QA), so `run-d.sh` runs from that
harness folder. On Casey's Mac this repo is cloned at `~/Documents/openelis-docs` and
`~/Documents/OpenELIS QA/docs-manual` and `run-d.sh` are symlinks into it.

## Plugin

```bash
npm run check:plugin   # validate (CI runs this)
npm run build:plugin   # writes dist/openelis-docs.plugin
npm run test:hooks     # hook self-tests
npm run lint:page -- path/to/page.xhtml
```

Upload the built `.plugin` file to Claude, together with the openelis-qa plugin,
which does the screen capture.

## Rules for contributors

- This repo is public: stage files by name, never `git add -A`; never commit env or `.auth` files.
- No em dashes in anything that reaches Confluence (organization writing rule; CI checks the plugin).
- Document only behavior verified on a live instance.

License: [MPL-2.0](LICENSE).
