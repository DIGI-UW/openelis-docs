# Changelog

## 2026-11-04

- Repo created. `docs-manual/` and `run-d.sh` moved in from Casey's Mac (where they lived outside
  any repo); figures, logs, backups and fetched copies are ignored.
- openelis-docs plugin 0.1.0 (see `plugin/openelis-docs/CHANGELOG.md`).
- `run-d.sh` now runs translation freshness for every language with a home in
  `docs-manual/fr/langs.json` (French and Indonesian), not French only.
- `docs-manual/publish/confluence-publish.py` is the same file as the plugin's copy (CI keeps them
  identical).
