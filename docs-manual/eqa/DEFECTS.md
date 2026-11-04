# Defects found during EQA capture (pngtest 3.2.2.0)

## EQA / i18n
1. Program→Scheme relabel landed only in en.json. en-US, fr, es, id, fr-MG still carry V1 "Program" wording (e.g. en-US: Program Administration, EQA Programs, Add Program, Program Name, Enroll in Program, My EQA Programs). A user on English (US) sees different words from the manual.
2. Residual "program" in English strings: breadcrumb "EQA Programs" (eqa.management.programs.title); Main menu item "Programs" under EQA Management; Participants subtitle "Manage organization enrollment in EQA programs"; Add Scheme helper "Result intake for this program offers exactly these tests…"; "Select Program"; "No enrollments found for this program"; "Select a program to view enrollments".
3. Scheme type label inconsistency: Add Scheme form says "Inter-lab split"; My Cycles "Scheme type" filter says "Split-sample".
4. Add Scheme Provider field is free text but its placeholder reads "Select provider", implying a picker.

## Organization Management (seed-data side, not EQA)
5. Type of Activity table: TableSelectRow onSelect AND TableRow onClick both toggle the row, so one click on the checkbox toggles twice (net: unchanged). Checking a type is unreliable.
6. Save shows "Organization Information Updated Succesfully" without checking the server response; a rejected save (e.g. no type selected) reports success and silently creates nothing. Five of six first attempts failed this way.
7. Street Address and City have maxLength 15 and truncate silently ("Taurama Road, Boroko" stored as "Taurama Road, B").
8. Typo in success toast: "Succesfully".
9. Hard-loading some /qa/eqa/* deep links (provider/schemes, management) in locale en renders a blank page with no console error; reaching the same route via the Main menu (SPA navigation) renders. Intermittent.
10. Cycle wizard Panel step: the per-sample Test picker offers the whole catalogue (755 tests), not the scheme's Assigned Tests.
11. Cycle wizard Cycle step: 'A cycle needs a name.' shows as an error before the user has typed anything; Submission deadline field is clipped at the right edge at 1412px width and its calendar icon overlaps the first digit.
12. Shipments: saving one row reloads the table and discards unsaved edits in every other row (typed courier/tracking/date lost). Save each row before editing the next. DRIVEN.
13. Pack list and Label PDFs print raw enum values (READY_TO_SEND, REFRIGERATED_2_8C); pack list shows Service Location "-" and Created By "-". DRIVEN.
14. Workbench banner keeps "Prep must clear the inventory and QC gate before any panel can be dispatched." after the cycle is Shipped. OBSERVED.
15. Pack list / Label download silently as PDFs (no on-screen confirmation). OBSERVED (files landed in Downloads).
16. SCORING (serious): result intake and scoring are per analyte, not per panel sample. CD4 panel had three samples (targets 185 / 520 / 1080); Enter results offers one box per test, and scoring used only the 1080 target (sealedTargetsByAnalyte keeps the last sample per analyte). The 185 and 520 levels are never scored. DRIVEN (scores CSV target_value 1080) + source EQAProviderScoringServiceImpl.sealedTargetsByAnalyte.
17. Scores column reads "0 unacceptable of 1" before Score cycle has run (looks like a pass). DRIVEN.
18. Send scores says "Scores placed in the FHIR store..." on a cycle whose distribution method is CSV export. DRIVEN.
19. Repeat shipment: no box, courier, tracking or expected-delivery fields for the repeat; Shipments tab still shows the original box SENT; receipt row expected delivery "-". DRIVEN.
20. Follow-up "Record response" takes no text; the lab's response can only be captured in the Resolve notes. DRIVEN.
21. Closed cycle still shows Send repeat / Enter results / Send scores; saving results on a closed cycle returns HTTP 500 (no message). DRIVEN.
22. Cycle history Trigger column shows raw enums (FIRST_SHIPMENT_SENT, ALL_SHIPMENTS_DELIVERED, SCORE_INTAKE); wizard creation logged as "Manual override". OBSERVED.
23. Performance report: "Laboratory" row blank ("-"); "1 values imported." grammar in CSV import. OBSERVED.
24. Enter results modal: CSV label overlaps the bottom of the grid. OBSERVED.
25. Organization Management: State field defaults to "MN" on new organisations and silently carries into EQA "Region" (showed "Lae, MN"); the column holds 2 characters and anything longer returns HTTP 500 with no validation message. DRIVEN (seed orgs corrected to blank state).
26. Participant performance page does not name the scheme it is showing. OBSERVED.
27. PARTICIPANT SCORING (serious, same root as 16): a panel with two samples of one analyte keeps a single participant result. Provider CSV scored 978 against target 1105; This Lab's Follow-Up shows Reported 412 (the other sample) and Target "-". DRIVEN.
28. My Cycles "Cycle" column shows the cycle number (1), not the cycle name. DRIVEN.
29. Validated EQA results do not advance the cycle until a background sweep runs (up to ~5 minutes); page says it advances "once validation completes". DRIVEN.
30. Review & submit: repeated activation returns HTTP 500 "Internal Server Error" instead of "already submitted". Keyboard focus stayed on Review & submit behind the "Submit by hand" modal, so typing a reference (spaces) re-triggered it. DRIVEN.
31. Add Order EQA mode: patient fields show literal "NULL", DOB 01/01/1900 (age 126); Sample Kind "Client sample" on an EQA sample; Result Deadline not pre-filled from the cycle; New cycle dates use mm/dd/yyyy native pickers while the rest of EQA uses dd/mm/yyyy. DRIVEN/OBSERVED.
32. My Programs: tests are not carried over from the chosen scheme; pickers take several seconds to appear; no success toast on Save Enrollment; subtitle still says "Programs". DRIVEN.
33. Analyst Competency counts Failures 0 while the evidence row for the same event reads "Counts against: Failure". OBSERVED.
