<details><summary>Changed strings, part 1 of 2 (118)</summary>

| Key | Old | New |
|---|---|---|
| `accession.entry` | Accession Number Entry | Lab Number Entry |
| `activityReportByTestSection` | Activity report By Test Section | Activity report By Lab Unit |
| `admin.labelPresets.fieldKey.SPECIMEN_TYPE` | Specimen Type | Sample Type |
| `admin.programs.questionnaire.question.typeExample.choice` | One option from a fixed list. Example: "Specimen condition". | One option from a fixed list. Example: "Sample condition". |
| `analyzer.connection.field.host.help` | The analyzer's IP address. Optional when the analyzer connects to the Analyzer Bridge. Leave it blank if the analyzer reaches the bridge through NAT or a proxy, and use the instrument system name instead. | The analyzer's IP address. Optional when the analyzer connects to the Analyzer Bridge. Leave it blank if the analyzer reaches the bridge through NAT or a proxy, and use the analyzer system name instead. |
| `analyzer.connection.field.senderId` | Instrument system name | Analyzer system name |
| `analyzer.connection.field.senderId.help` | The name this instrument sends in its messages (ASTM H.5 or HL7 MSH-3), such as the GeneXpert System Name. Needed only when several analyzers share this port and address. | The name this analyzer sends in its messages (ASTM H.5 or HL7 MSH-3), such as the GeneXpert System Name. Needed only when several analyzers share this port and address. |
| `analyzer.filter.testUnit` | Test Unit | Lab Unit |
| `analyzer.importIssues.accession` | Accession number | Lab number |
| `analyzer.placement.instrumentSpecimen` | Instrument sent: {id} | Analyzer sent: {id} |
| `analyzer.placement.patient.match` | Instrument patient {instrument} matches the order's patient. | Analyzer patient {instrument} matches the order's patient. |
| `analyzer.placement.patient.mismatch` | The instrument reported patient {instrument}, but the order's patient is {order}. Add a note saying why before saving. | The analyzer reported patient {instrument}, but the order's patient is {order}. Add a note saying why before saving. |
| `analyzer.placement.patient.noOrderPatient` | The instrument reported patient {instrument}. The order has no patient identifier to compare it with. | The analyzer reported patient {instrument}. The order has no patient identifier to compare it with. |
| `analyzer.placement.redirect.help` | Use this when the instrument misread the specimen ID. The reason is saved with the result. | Use this when the analyzer misread the sample ID. The reason is saved with the result. |
| `analyzer.results.held.assayNotEnabled` | This assay is off in the analyzer's setup, so its result was held. Turn it on in the setup's Assays step if this instrument runs it; the result is retried when the mapping is applied. | This assay is off in the analyzer's setup, so its result was held. Turn it on in the setup's Assays step if this analyzer runs it; the result is retried when the mapping is applied. |
| `analyzer.results.held.instrumentNote` | Instrument note: {note} | Analyzer note: {note} |
| `analyzer.results.instrumentReported` | Instrument reported | Analyzer reported |
| `analyzer.setup.assays.help` | Turn on the assays this instrument runs, as in its own host test code settings. Verify maps only the assays that are on. A result for an assay that is off is held, never lost. | Turn on the assays this analyzer runs, as in its own host test code settings. Verify maps only the assays that are on. A result for an assay that is off is held, never lost. |
| `analyzer.setup.instrument.notListed` | Instrument not listed? | Analyzer not listed? |
| `analyzer.setup.instrument.summary` | Saved instrument details | Saved analyzer details |
| `analyzer.setup.instrument.title` | Instrument | Analyzer |
| `analyzer.setup.instrument.type.helper` | Choose the listed type for your instrument, even if it will only send results. Whether it sends results only or also receives orders is set later, in Connect. | Choose the listed type for your analyzer, even if it will only send results. Whether it sends results only or also receives orders is set later, in Connect. |
| `analyzer.setup.verify.noAssays` | No assay is on for this instrument. Turn on the assays it runs in Assays. | No assay is on for this analyzer. Turn on the assays it runs in Assays. |
| `analyzer.setup.verify.unresolved` | {count, plural, one {# record or value} other {# records or values}} of the assays that are on still need mapping. Map them below, or turn the assay off in Assays if this instrument does not run it. | {count, plural, one {# record or value} other {# records or values}} of the assays that are on still need mapping. Map them below, or turn the assay off in Assays if this analyzer does not run it. |
| `analyzerType.editor.analyzerName` | Instrument name in messages | Analyzer name in messages |
| `analyzerType.editor.newProtocolHelp` | Choose FILE, ASTM, or HL7 and enter the settings supported by the instrument. The protocol is fixed after the first save. | Choose FILE, ASTM, or HL7 and enter the settings supported by the analyzer. The protocol is fixed after the first save. |
| `analyzerType.editor.semantic.sampleId` | Specimen identifier | Sample identifier |
| `analyzerType.editor.testDefinitionsHelp` | List the test codes and result values reported by the instrument. These definitions supply suggestions for matching to the laboratory catalog; they do not create or change laboratory tests. | List the test codes and result values reported by the analyzer. These definitions supply suggestions for matching to the laboratory catalog; they do not create or change laboratory tests. |
| `analyzerType.recognition.condition.prefixValue` | Specimen ID prefix | Sample ID prefix |
| `analyzerType.recognition.condition.specimenPrefix` | Specimen ID starts with | Sample ID starts with |
| `analyzerType.recognition.condition.summary.configuredPattern` | Specimen ID matches a configured pattern | Sample ID matches a configured pattern |
| `analyzerType.recognition.source.specimenId` | Specimen ID | Sample ID |
| `banner.menu.nonconformity` | Non-Conform | Nonconformity |
| `banner.menu.nonconformity.report` | Report Non-Conforming Event | Report Nonconforming Event |
| `banner.menu.nonconformity.view` | View New Non-Conforming Events | View New Nonconforming Events |
| `banner.menu.resultvalidation.bench` | By Bench | By Lab Unit |
| `banner.menu.workplan.unit` | By Test Section | By Lab Unit |
| `barcode.label.info.labNumber` | Accession number | Lab number |
| `barcode.label.info.labnumber` | Accession number | Lab number |
| `barcode.label.info.specimenType` | Specimen Type | Sample Type |
| `barcode.label.specimen` | Specimen label | Sample label |
| `barcode.labels.sample.row` | Specimen labels sample {sampleNumber} | Sample labels sample {sampleNumber} |
| `barcode.print.all.legacy` | Prints {orderCount, plural, one {# order label} other {# order labels}} and {specimenCount, plural, one {# label} other {# labels}} per specimen. | Prints {orderCount, plural, one {# order label} other {# order labels}} and {specimenCount, plural, one {# label} other {# labels}} per sample. |
| `barcode.print.col.accession` | Accession Number | Lab Number |
| `catalog.import.description` | Load test catalog files without editing tests one at a time. Preview checks each file against the catalog as it stands and keeps nothing, so a row that needs a lab unit, specimen or test another file in the same upload creates is listed as skipped until you apply. Apply loads the files in order and saves them with the configuration, so the next restart loads exactly what you applied. | Load test catalog files without editing tests one at a time. Preview checks each file against the catalog as it stands and keeps nothing, so a row that needs a lab unit, sample type or test another file in the same upload creates is listed as skipped until you apply. Apply loads the files in order and saves them with the configuration, so the next restart loads exactly what you applied. |
| `collect.addTests.helper` | Add a test the clinician asked for after the order was entered, or one that only becomes appropriate with the specimen in hand. | Add a test the provider asked for after the order was entered, or one that only becomes appropriate with the sample in hand. |
| `collect.sample.specimenOrigin` | Specimen Origin | Sample Origin |
| `common.accessionNumber` | Accession Number | Lab Number |
| `configuration.testUnit.assign.new.unit` | Assign to test section | Assign to lab unit |
| `configuration.testUnit.confirmation.explain` | This test unit will not be active until at least one test has been assigned to it. | This lab unit will not be active until at least one test has been assigned to it. |
| `configuration.testUnit.create` | Create New Test Unit | Create New Lab Unit |
| `configuration.testUnit.create.duplicate` | An existing test unit with the same name has been found.  Please cancel or use a different name. | An existing lab unit with the same name has been found.  Please cancel or use a different name. |
| `configuration.testUnit.order` | Set Test Unit Order | Set Lab Unit Order |
| `configuration.testUnit.order.explain.limits` | Only test sections with tests assigned may be ordered.  For new sections please assign tests before ordering. | Only lab units with tests assigned may be ordered.  For new lab units please assign tests before ordering. |
| `description.testUnit` | Which section of the lab performs the test. This is also known as a test section. | Which unit of the lab performs the test. This is also known as a lab unit. |
| `eqa.competency.event.ESCALATED_TO_NCE` | Escalated to non-conformity | Escalated to nonconformity |
| `eqa.competency.reason.openEscalation` | An escalated non-conformity raised between {from} and {to} is still open, over {evaluable} assessable samples with {failures} failures. Close the non-conformity to clear the band. | An escalated nonconformity raised between {from} and {to} is still open, over {evaluable} assessable samples with {failures} failures. Close the nonconformity to clear the band. |
| `eqa.competency.reason.repeatedFailure` | {failures} failures in {evaluable} assessable samples between {from} and {to}. This is a performance concern: review the failed results and raise a non-conformity, or dismiss them on triage. | {failures} failures in {evaluable} assessable samples between {from} and {to}. This is a performance concern: review the failed results and raise a nonconformity, or dismiss them on triage. |
| `eqa.competency.rule.openEscalation` | Open non-conformity | Open nonconformity |
| `eqa.participant.infoBody` | Click a Lab No to open standard result entry for that sample. Once validation completes, the cycle advances to Submitted (or Ready to submit if the scheme requires cycle-level review). | Click a Lab Number to open standard result entry for that sample. Once validation completes, the cycle advances to Submitted (or Ready to submit if the scheme requires cycle-level review). |
| `eqa.provider.followups.subtitle` | Laboratories participating in the schemes this lab provides that returned unacceptable results. Follow-up here is correspondence with another lab — it never opens a non-conformity in this lab's own register. | Laboratories participating in the schemes this lab provides that returned unacceptable results. Follow-up here is correspondence with another lab; it never opens a nonconformity in this lab's own register. |
| `eqa.queue.triageHelp` | Escalate if you suspect a real non-conformity. Dismiss with a reason if this is noise — a transcription error, or equipment trouble already documented. Dismissed entries stay linked to the cycle for accreditation trace. | Escalate if you suspect a real nonconformity. Dismiss with a reason if this is noise: a transcription error, or equipment trouble already documented. Dismissed entries stay linked to the cycle for accreditation trace. |
| `esig.context.validateSingle` | Validate and release {test} for accession {accession} | Validate and release {test} for lab number {accession} |
| `field.select.testSection` | Select Test Section | Select Lab Unit |
| `field.testSection` | Test Section | Lab Unit |
| `field.testUnit` | Test Unit | Lab Unit |
| `genericSample.edit.success.accession` | Accession Number: {accessionNumber} | Lab Number: {accessionNumber} |
| `genericSample.order.success.message` | Sample order created successfully with accession number: {accessionNumber} | Sample order created successfully with lab number: {accessionNumber} |
| `genericSample.search.title` | Search by Accession Number | Search by Lab Number |
| `header.label.nonconformityByDate` | Non-conformity Report By Date | Nonconformity Report By Date |
| `heading.labUnit.subtitle` | Configure lab units (lab sections), domain classification, test assignments, and display order. | Configure lab units, domain classification, test assignments, and display order. |
| `helper.testCatalog.basicInfo.sampleTypesMulti` | Select every specimen this test runs on. Configuration is shared across them. | Select every sample type this test runs on. Configuration is shared across them. |
| `instructions.qc.fail.blocks.validation` | When enabled, results covered by an open quality-control failure cannot be accepted in Validation until the non-conformity is closed; they can still be rejected. When disabled, the failure is shown on the row as a warning only. | When enabled, results covered by an open quality-control failure cannot be accepted in Validation until the nonconformity is closed; they can still be rejected. When disabled, the failure is shown on the row as a warning only. |
| `label.audittrail` | Lab No | Lab Number |
| `label.audittrail.labNo.invalidaccessionnumber` | Invalid Accession Number | Invalid Lab Number |
| `label.audittrail.labNo.missing` | Lab No is required! | Lab Number is required! |
| `label.barcode.specimenlabel` | Number of specimen labels per set | Number of sample labels per set |
| `label.checkedWillBeModified` | Checked lab no. will be modified | Checked lab number will be modified |
| `label.referOut.empty.subtitle` | Samples appear here once they are saved. Save the order first to refer specimens out. | Samples appear here once they are saved. Save the order first to refer samples out. |
| `label.referOut.section.description` | Refer specimens to an external lab. Each sample carries its full chain-of-custody metadata. | Refer samples to an external lab. Each sample carries its full chain-of-custody metadata. |
| `label.results.alert.critical.defaultMessage` | This is a critical result. Notify the responsible clinician according to your laboratory procedure. | This is a critical result. Notify the responsible provider according to your laboratory procedure. |
| `label.results.analyzer.none` | Not from an instrument | Not from an analyzer |
| `label.results.critical.banner.notify` | The responsible clinician must be notified. Record that on the Alerts dashboard and log the call below. | The responsible provider must be notified. Record that on the Alerts dashboard and log the call below. |
| `label.results.critical.banner.title` | Critical value — physician notification required | Critical value: provider notification required |
| `label.results.critical.comment.placeholder` | e.g. Physician notified by phone | e.g. Provider notified by phone |
| `label.results.history.event.NCE` | Non-conformity | Nonconformity |
| `label.results.nce.report` | Report Non-Conformity | Report Nonconformity |
| `label.results.order.clinician` | Ordering clinician | Ordering provider |
| `label.results.range` | Reference Range | Normal Range |
| `label.sampleType.disposal.intro` | Free-text reference guidance for disposing of this specimen type. The authoritative, structured handling stays on each test's Storage section and the specimen disposal workflow. | Free-text reference guidance for disposing of this sample type. The authoritative, structured handling stays on each test's Storage section and the sample disposal workflow. |
| `label.search.labno.family` | Search by LabNo or Family Name | Search by Lab Number or Family Name |
| `label.selectTestSectionCatalog` | Select test section to view catalog for that section | Select lab unit to view catalog for that lab unit |
| `label.testCatalog.alerts.field.sampleTypeHelp` | Which specimen this alert watches. Leave unset to watch every sample type this test runs on. | Which sample type this alert watches. Leave unset to watch every sample type this test runs on. |
| `label.testCatalog.alerts.recipient.physician` | Ordering Physician | Ordering Provider |
| `label.testCatalog.override.col.sampleType` | Specimen | Sample Type |
| `label.testCatalog.override.shared` | All specimens (shared) | All sample types (shared) |
| `label.validation.autoValidated.empty` | No auto-validated results for this accession. | No auto-validated results for this lab number. |
| `label.validation.bulk.bodyClear` | {count, plural, one {This # result is} other {These # results are}} in the Clear lane: in range, no recorded QC failure, no non-conformity, not modified, not critical. A result that stops being clear before the release is skipped. | {count, plural, one {This # result is} other {These # results are}} in the Clear lane: in range, no recorded QC failure, no nonconformity, not modified, not critical. A result that stops being clear before the release is skipped. |
| `label.validation.release.scope` | Clearance checks the reference range, result flags, non-conformities, edits after save and critical acknowledgment, and stops any result with a recorded quality-control failure. It does not confirm that quality control was performed. | Clearance checks the normal range, result flags, nonconformities, edits after save and critical acknowledgment, and stops any result with a recorded quality-control failure. It does not confirm that quality control was performed. |
| `label.validation.review.error.qcHold` | Release blocked: a failed QC control holds this result until its non-conformity is closed. | Release blocked: a failed QC control holds this result until its nonconformity is closed. |
| `label.validation.review.normalRange` | Reference range | Normal range |
| `label.validation.review.reject.hint` | Rejecting files a non-conformity event; complete the form to record it. | Rejecting files a nonconformity event; complete the form to record it. |
| `label.validation.review.success.rejected` | Result rejected; the non-conformity event is recorded. | Result rejected; the nonconformity event is recorded. |
| `labno.alt.prefix.use` | Use the same accession number format and pool of available numbers as Order Entry Generation. | Use the same lab number format and pool of available numbers as Order Entry Generation. |
| `menu.accession.validation.range` | By Range of Order Numbers | By Range of Lab Numbers |
| `menu.nonconform.active` | Non-Conformity Menu Active | Nonconformity Menu Active |
| `menu.nonconform.title` | Non-Conformity Menu Management | Nonconformity Menu Management |
| `menu.results.range` | By Range of Order numbers | By Range of Lab numbers |
| `microbiology.case.accessionNumber` | Accession number | Lab number |
| `microbiology.worklist.ast.automaticResultsDetail` | Connected instruments send results directly to the case. Failed or unmatched events are retained in Analyzer Import Issues. | Connected analyzers send results directly to the case. Failed or unmatched events are retained in Analyzer Import Issues. |
| `nce.form.title` | Report Non-Conformity Event | Report Nonconformity Event |
| `nce.inline.title` | Report Non-Conformity Event | Report Nonconformity Event |
| `nce.link.duplicate.warning` | These specimens are already linked to this NCE | These samples are already linked to this NCE |
| `nonconform.label.prescibernamesite` | Prescriber Name and Site | Provider Name and Site |
| `nonconform.view.specimen` | Specimen(s) | Sample(s) |
| `notebook.results.noAccession` | No accession number available for this sample | No lab number available for this sample |
| `notebook.results.none.subtitle` | No results found for the provided accession number. | No results found for the provided lab number. |
| `notebook.samples.none.subtitle` | Search Samples By Patient or Accession Number | Search Samples By Patient or Lab Number |
</details>
