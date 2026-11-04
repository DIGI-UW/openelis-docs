## Summary
Removes **1,652 keys from `frontend/src/languages/en.json`** that nothing in the codebase references. en.json goes from 12,698 to 11,046 keys. Only en.json changes; the other locale files will follow through the normal Transifex push and nightly pull.

Largest groups: eqa 256, analyzer 189, nce 143, storage 124, qc 105, sampleManagement 69, vector 66, compliance 44, result 43, shipment 35, patient 33, env 32.

## How the keys were found
- Every en.json key was searched as an exact token across develop @ `5ae8a35`: frontend (including `languages/*.js(x)`), backend Java, Liquibase, SQL, properties. Locale JSON files and `specs/` docs were not counted as references.
- Keys that match a dynamically built prefix (`"x.y." + v` or `` `x.y.${v}` ``) count as possibly used and are **kept** (1,113 keys).
- Keys referenced only by tests are kept (18).

## Protecting work in flight
Of 2,320 unreferenced keys, **668 are kept** (a key can have more than one reason):
- changed in en.json in the last 30 days (features whose UI may still be landing): 438
- referenced by code on a branch pushed since 13 Aug (151 branches scanned): 87
- referenced by code in an open PR (203 open PRs scanned, added lines only): 25
- edited in en.json by an open PR: 45
- analyzer menu labels used by `openelisglobal-plugins`: 14
- menu labels (`banner.menu.*`, `sidenav.*`, `master.lists.*`): menus are database-driven, so deployments may still use them: 51
- the `common.*` shared vocabulary seeded on purpose in 8265cbbd: 70

Three open PRs could not be compared with develop because of unusual history and were not scanned: #2686, #3434, #3496.

## Checks
- JSON parses; every remaining key keeps its value and order; formatting unchanged apart from the removed lines.
- No duplicate keys; `scripts/ci/check-i18n-plurals.py` passes.

## Reviewer notes
- If any removed key belongs to work that is not on a branch or PR yet, comment and it goes back in.
- The full list is in the comments below.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01A7nEGRMzBuPooiF3bFDwVu
