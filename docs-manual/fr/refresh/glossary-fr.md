# OpenELIS Global: French translation glossary (fr-v1, 2026-10-09)

Used for every French page of the OpenELIS Confluence documentation. Two layers:

1. **UI labels** (anything the reader must find on screen: menu entries, buttons, field names, column
   headers, statuses, tabs). These are never translated freely. They are copied exactly from the
   OpenELIS French interface (`frontend/src/languages/fr.json` in DIGI-UW/OpenELIS-Global-2, develop),
   even where that string is imperfect, because the reader has to match it on screen.
2. **Prose terms** (everything else). These follow the table below so a term reads the same on every page.

## Rules

- **UI labels.** Bold the French UI string exactly as `fr.json` gives it. Because screenshots show the
  English interface, the first time a label appears on a page give the English in parentheses and
  italics: **Enregistrer** (*Save*). After that, French only.
- **Label with no French string** (the key is untranslated in `fr.json`, so a French interface shows the
  English text): keep the English label in bold, unchanged. Example: **Prepare Samples**, **Sample check**.
- **Menu paths.** "Main menu → Results → Results Entry" becomes "Menu principal → **Résultats** →
  **Saisie des résultat**" (UI strings as-is). Arrows and order unchanged.
- **Never translate:** code, routes, URLs, setting and property names (`resultsEntryUnifiedRoute`),
  file names, Jira keys, version numbers, command lines, product names (OpenELIS Global, Confluence,
  Docker, PostgreSQL, OpenMRS, OCL, LOINC, SNOMED CT), standard names (ISO 15189, 21 CFR Part 11, FHIR R4).
- **Seed data in examples** (patient names, lot numbers, site names) stays as captured, so it matches
  the figures.
- **Register:** *vous*, imperative for steps ("Cliquez sur…", "Saisissez…"). Neutral, international
  French usable in West/Central Africa, Madagascar, Haiti.
- **Typography:** non-breaking space before `: ; ? !` and inside « guillemets ». Sentence case for
  headings. Decimal comma in prose numbers, but keep values exactly as the screen shows them.
- **Units and abbreviations** stay as on screen (mille/mm3, g/dL).
- **Bold that is not a screen label** (emphasis, CSV values, folder names) is translated as prose, with
  no English gloss.
- **Operating-system controls** (a file dialog's Open button) are written in normal French: **Ouvrir**.
- **When `fr.json` matches the wrong key** (for example "OK" giving "D'ACCORD", "On" giving "Le"), use the
  string the screen actually shows; if unsure keep the English label.

## Page furniture

| English | French |
|---|---|
| How-to | Guide pratique |
| Concept | Concept |
| Reference | Référence |
| At a glance | En bref |
| Purpose | Objectif |
| You'll end up with | Résultat obtenu |
| Who does this | Qui s'en charge |
| Before you start | Avant de commencer |
| Where | Où |
| Steps | Étapes |
| Field reference | Description des champs |
| Tips | Conseils |
| Not yet available | Pas encore disponible |
| Not yet documented | Pas encore documenté |
| Provenance | Provenance |
| Verified by … · Date … · Instance … · OpenELIS version … | Vérifié par … · Date … · Instance … · Version d'OpenELIS … |
| Part of: | Fait partie de : |
| Using an older release? The previous version of this page is … | Vous utilisez une version antérieure ? La version précédente de cette page est … |
| Status: draft, unverified | Statut : brouillon, non vérifié |
| This step has not yet been verified on a live instance. Confirm before publishing. | Cette étape n'a pas encore été vérifiée sur une instance réelle. À confirmer avant publication. |
| Access is set by user permissions and can be configured by your administrator. | L'accès dépend des droits de l'utilisateur et peut être configuré par votre administrateur. |
| Figure caption "The … screen" | « L'écran … » |

## Roles

| English | French |
|---|---|
| reception staff | personnel d'accueil |
| lab staff | personnel de laboratoire |
| analyst | technicien (analyste) |
| validator | biologiste validateur |
| lab administrator | administrateur de laboratoire |
| administrator | administrateur |
| system administrator | administrateur système |
| field staff | agents de terrain |
| pathologist | pathologiste |
| implementer | équipe de mise en œuvre |

## Laboratory and OpenELIS terms (prose)

| English | French (prose) | Note |
|---|---|---|
| order (lab order) | demande d'analyse | UI calls it **Ordonnance** / **Demande d'examen**; quote the UI label when referring to the screen |
| clinical / environmental / vector order | demande clinique / environnementale / vectorielle | never "ordonnance environnementale" in prose |
| order entry | saisie des demandes | |
| electronic order | demande électronique | |
| batch order entry | saisie des demandes par lot | |
| lab number, accession number | numéro de laboratoire | |
| sample | échantillon | |
| specimen (vector, individual organism) | spécimen | |
| sample type | type d'échantillon | |
| sample item | élément d'échantillon | |
| aliquot | aliquote | |
| collection | prélèvement | |
| sample check / QA review | contrôle de l'échantillon / revue assurance qualité | UI labels as on screen |
| test | analyse | "test" only inside UI labels that use it |
| test catalog(ue) | catalogue de tests | matches UI **Catalogue de tests** |
| panel | panel d'analyses | UI label **Panneau** quoted as-is |
| lab unit, test section | unité de laboratoire | |
| method | méthode | |
| result | résultat | |
| result entry | saisie des résultats | |
| validate / release results | valider / libérer les résultats | |
| retest | reprise d'analyse | UI **Retester** |
| reference range / normal range | intervalle de référence | |
| critical range / value | valeur critique | |
| valid range | plage valide | |
| reflex test | analyse réflexe | |
| calculated value test | analyse calculée | |
| work plan | plan de travail | |
| report | rapport | |
| non-conforming event (NCE) | événement non conforme (ENC) | |
| corrective and preventive action (CAPA) | action corrective et préventive (CAPA) | |
| quality control (QC) | contrôle qualité (CQ) | |
| control lot | lot de contrôle | |
| EQA / proficiency testing | évaluation externe de la qualité (EEQ) / essais d'aptitude | |
| referral (send-out) | envoi à un laboratoire de référence | |
| referral lab | laboratoire de référence | |
| storage, disposal | stockage, élimination | |
| holding time | délai de conservation | |
| compliance standard | norme de conformité | |
| compliance certificate | certificat de conformité | Indonesian title *Sertifikat Hasil Uji* kept as is |
| pool, pooling | pool, regroupement | |
| deconvolution | déconvolution | |
| field survey | enquête de terrain | |
| entomological indices | indices entomologiques | |
| program, questionnaire | programme, questionnaire | |
| dictionary entry | entrée du dictionnaire | |
| provider (requesting clinician) | prescripteur | UI label **Prestataire** quoted as-is |
| organization | structure (organisation) | UI **Organisation** |
| sampling site | site de prélèvement | |
| patient | patient | UI **Patiente** quoted only when it is the menu label |
| user account, role, permission | compte utilisateur, rôle, droit d'accès | |
| electronic signature | signature électronique | |
| audit trail | piste d'audit | |
| lab notebook | cahier de laboratoire | UI **Carnet de notes** |
| analyzer | analyseur (automate) | UI **Analyseur** |
| analyzer bridge | passerelle d'analyseurs (Analyzer Bridge) | |
| dashboard | tableau de bord | |
| settings, configuration | paramètres, configuration | |
| search index | index de recherche | |
| non-working days | jours non ouvrés | |
| turnaround time (TAT) | délai de rendu des résultats (TAT) | |
| barcode, label preset | code-barres, modèle d'étiquette | |
| upgrade, backup, restore | mise à niveau, sauvegarde, restauration | |
| high availability, failover | haute disponibilité, basculement | |
| server, workstation | serveur, poste de travail | |
| deployment | déploiement | |
| release | version | |
| draft | brouillon | |
| AMR (antimicrobial resistance) | RAM (résistance aux antimicrobiens) | |
| standby server | serveur de secours | |
| primary server | serveur primaire | |
| promote (a standby) | promouvoir | |
| fence (a node) | isoler | |
| rejoin | réintégrer | |
| switchover / failback | bascule planifiée / retour arrière | |
| snapshot | copie instantanée | |
| replication slot, WAL | slot de réplication, WAL | kept in English |
| configuration folder names (`tests`, `sample-types`) | unchanged | they are file paths |

## Known weaknesses in the French UI strings (report upstream, quote as-is in the docs)

- `banner.menu.patient` = "Patiente" (should be "Patient")
- `banner.menu.results.unified` = "Saisie des résultat" (should be "Saisie des résultats")
- `sideNav.label.qa` = "Quality Assurance" (untranslated)
- `sidenav.label.order.prepare` = "Prepare Samples", `sidenav.label.order.sampleCheck` = "Sample check" (untranslated)
- Order is rendered three ways: "Ordonnance", "Commande", "Demande d'examen"
- `Panel` = "Panneau" (literal)
- `Test` (bare) = "Analyses" (plural)
- "How many pools?" = "Combien de piscines ?", "Save Pools" = "Pools de sauvegarde" (vector deconvolution)
- "Male" / "Female" = "Mâle" / "Femelle" (ranges); should be "Homme" / "Femme"
- "Position" = "Poste"; "Add Standard" = "Ajouter un étalon" (should be "Ajouter une norme")
- "Review" = "Critique"; "Reporter & Event Context" = "Journaliste et contexte de l'événement"
- "Retest All Tests" = "Rejeter tous les résultats"; "Lab No" = "laboratoire non"
- "Show on patient report" = "Afficher dans le dossier du patient"; "Refer this test" = "Consultez cette analyse"
- "Not from an instrument" = "Pas de manière directe"; "Show deactivated" = "Affichage désactivé"
- "Global Menu Management" = "Titre global"; "Preview Mapping" = "Soumettre un message d'exemple"
- "Sample Acceptance Checklist" = "Exemple de liste de contrôle pour l'acceptation des échantillons"
- "Accepted by technician" and many result-entry, pathology and work plan labels have no French string
