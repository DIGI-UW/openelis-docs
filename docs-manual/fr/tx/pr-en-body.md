## Summary
Standardizes English UI terms in `frontend/src/languages/en.json` (237 strings) and updates the tests that assert the old text. No application code changes.

| Decision | Strings |
|---|---|
| **Lab Number** for the sample/order identifier (not Accession, Accession Number, LabNo, Order Number). "Lab No." kept only as a narrow column header. | 50 |
| **Lab Unit** (not Test Section, Test Unit, Lab Section, "By Bench") | 34 |
| **Provider** for the requesting clinician (not Clinician, Physician, Prescriber) | 14 |
| **Sample** (Specimen kept for vector organisms, pool members, cytology, and the microbiology/WHONET and HL7 SPM terms) | 43 |
| **Analyzer** (Instrument kept for non-analyzer equipment, Device for cold storage and serial devices) | 42 |
| **Spellings:** Requester, Organization, Nonconformity / nonconforming, Workplan | 51 |
| **Ranges:** "Normal range" where only the normal interval is meant; "Reference ranges" for the whole set (normal, valid, critical) | 3 |

Sex, not gender: the English UI already says "Sex" everywhere; no English change was needed.

## Tests
- Unit tests: 21 test files updated (expected text only). The 22 affected files pass 348/348; full suite passes except `InventoryItemsBoard.test.jsx` "Expires in 20d", which fails on develop today for an unrelated reason (the 20-day window crosses the 1 Nov DST change).
- Playwright / Cypress: visible-text queries updated in 12 specs. Strings that come from the backend were left as they are (Custom Data Export field labels such as "Accession Number" and "Specimen ID", the "Non-Conformance" report type, the QC export CSV).

## Follow-ups (not in this PR)
- Backend labels still use the old words: Custom Data Export field labels in the Java data sources, `reporting/non-conformance.json`, the QC CSV export, and `common.accessionNumber` remains as a key (its text is now Lab Number).
- Other locales keep their current translations (Transifex `keep_translations`); French is being aligned through the French UI crosswalk.

The full old/new list is in the comments.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01A7nEGRMzBuPooiF3bFDwVu
