# OpenELIS Global: Indonesian translation glossary (id-v1, 2026-10-22)

Used for every Indonesian (Bahasa Indonesia) page of the OpenELIS Confluence documentation. Two layers:

1. **UI labels** (anything the reader must find on screen: menu entries, buttons, field names, column
   headers, statuses, tabs). These are never translated freely. They are copied exactly from the live
   OpenELIS Indonesian interface strings in Transifex (`tx/id-live.json`, from
   `tx-push.py --lang=id --live-json`), even where the string is imperfect, because the reader has to
   match it on screen. Each page's batch carries a `ui` map with the exact strings.
2. **Prose terms** (everything else). These follow the tables below so a term reads the same on every page.

## Rules

- **UI labels.** Bold the Indonesian UI string exactly as the `ui` map gives it. Because screenshots show
  the English interface, the first time a label appears on a page give the English in parentheses and
  italics: **Simpan** (*Save*). After that, Indonesian only.
- **Label that is the same in both languages** (the `ui` map says "same as English", for example **Edit**,
  **Filter**, **Admin**): keep it in bold unchanged, no gloss.
- **Label with no Indonesian string** (not in the `ui` map and clearly an on-screen label): keep the
  English label in bold, unchanged.
- **Menu paths.** "Main menu → Results → Results Entry" becomes "**Menu Utama** → **Hasil** →
  **Entri Hasil**" (UI strings as-is). Arrows and order unchanged.
- **Never translate:** code, routes, URLs, setting and property names (`resultsEntryUnifiedRoute`),
  file names, Jira keys, version numbers, command lines, product names (OpenELIS Global, Confluence,
  Docker, PostgreSQL, OpenMRS, OCL, LOINC, SNOMED CT, WHONET), standard names (ISO 15189,
  21 CFR Part 11, FHIR R4).
- **Seed data in examples** (patient names, lot numbers, site names) stays as captured, so it matches
  the figures.
- **Register:** formal Indonesian, address the reader as *Anda*. Steps in the imperative without
  "silakan": "Klik …", "Masukkan …", "Pilih …", "Buka …". Standard spelling (EYD), Kemenkes laboratory
  usage where it exists.
- **Typography:** no space before `: ; ? !`. Straight double quotes "…" for quoted words. Sentence case
  for headings (only the first word and proper nouns capitalised). Decimal comma in prose numbers
  (2,5 mL), but keep values exactly as the screen shows them.
- **Never write an em dash (—)**, not even where the English has one: use a colon ("Admin — X" becomes
  "Admin: X"), a comma or parentheses.
- **Units and abbreviations** stay as on screen (mm3, g/dL).
- **Bold that is not a screen label** (emphasis, CSV values, folder names) is translated as prose, with
  no English gloss.
- **Operating-system controls** (a file dialog's Open button) are written in normal Indonesian: **Buka**.
- **English IT terms** common in Indonesian (server, plugin, file, log) stay as they are, in plain text.
  Where the table gives an Indonesian term with the English in parentheses (pencadangan (backup)),
  use that form on first use on a page, then the Indonesian term only.

## Page furniture

| English | Indonesian |
|---|---|
| How-to | Panduan langkah |
| Concept | Konsep |
| Reference | Referensi |
| At a glance | Sekilas |
| Purpose | Tujuan |
| You'll end up with | Hasil akhir |
| Who does this | Siapa yang melakukan |
| Before you start | Sebelum memulai |
| Where | Lokasi |
| Steps | Langkah-langkah |
| Field reference | Keterangan kolom |
| Tips | Tips |
| Not yet available | Belum tersedia |
| Not yet documented | Belum didokumentasikan |
| Provenance | Asal-usul |
| Provenance tags DRIVEN / OBSERVED only | DIUJI / HANYA DIAMATI |
| Verified by … · Date … · Instance … · OpenELIS version … | Diverifikasi oleh … · Tanggal … · Instans … · Versi OpenELIS … |
| Part of: | Bagian dari: |
| Using an older release? The previous version of this page is … | Menggunakan rilis yang lebih lama? Versi sebelumnya dari halaman ini adalah … |
| Status: draft, unverified | Status: draf, belum diverifikasi |
| This step has not yet been verified on a live instance. Confirm before publishing. | Langkah ini belum diverifikasi pada instans yang berjalan. Pastikan sebelum dipublikasikan. |
| Access is set by user permissions and can be configured by your administrator. | Akses ditentukan oleh izin pengguna dan dapat dikonfigurasi oleh administrator Anda. |
| Figure caption "The … screen" | "Layar …" |
| legacy page (older manual) | halaman versi lama |

## Roles

| English | Indonesian |
|---|---|
| reception staff | petugas penerimaan sampel |
| lab staff | petugas laboratorium |
| analyst | analis |
| validator | validator |
| lab administrator | administrator laboratorium |
| administrator | administrator |
| system administrator | administrator sistem |
| field staff | petugas lapangan |
| pathologist | dokter spesialis patologi |
| implementer | tim implementasi |

## Laboratory and OpenELIS terms (prose)

| English | Indonesian (prose) | Note |
|---|---|---|
| order (lab order) | pemesanan pemeriksaan, then pemesanan | matches UI **Pemesanan**; "permintaan" only where the UI label says it |
| clinical / environmental / vector order | pemesanan klinis / lingkungan / vektor | UI **Tambah Pemesanan Klinis** etc. |
| order entry | entri pemesanan | |
| electronic order | pemesanan elektronik | |
| batch order entry | entri pemesanan batch | |
| lab number, accession number | nomor registrasi | UI **Nomor Registrasi** / **No. Registrasi** |
| sample | sampel | |
| specimen (vector, individual organism) | spesimen | |
| sample type | jenis sampel | |
| sample item | item sampel | |
| aliquot | alikuot | |
| collection | pengambilan sampel | |
| sample check | pengecekan sampel | UI **Pengecekan sampel** |
| QA review | tinjauan QA | UI **Tinjauan QA** |
| test | pemeriksaan | |
| test catalog(ue) | katalog pemeriksaan | |
| panel | panel pemeriksaan | |
| lab unit, test section | instalasi lab | |
| method | metode | |
| result | hasil | |
| result entry | entri hasil | |
| validate / release results | memvalidasi / merilis hasil | UI **Validasi**, release = rilis |
| retest | pemeriksaan ulang | |
| reference range / normal range | rentang rujukan | |
| critical range / value | nilai kritis | |
| valid range | rentang valid | |
| reflex test | pemeriksaan refleks | |
| calculated value test | pemeriksaan nilai terkalkulasi | |
| work plan | rencana kerja | |
| report | laporan | |
| triage | triase | |
| "Clear" lane (triage) | tanpa temuan | quote the UI label when it is on screen |
| non-conforming event (NCE) | kejadian tidak sesuai (KTS) | UI says **Ketidaksesuaian** |
| corrective and preventive action (CAPA) | tindakan perbaikan dan pencegahan (CAPA) | |
| quality assurance | pemantapan mutu | UI **Pemantapan Mutu** |
| quality control (QC) | QC (kontrol mutu) on first use, then QC | UI keeps **QC** |
| control lot | lot kontrol | |
| EQA / proficiency testing | pemantapan mutu eksternal (PME) / uji profisiensi | UI **PME** |
| EQA scheme | program PME | |
| referral (send-out) | rujukan ke laboratorium lain | UI **Dirujuk keluar** |
| referral lab | laboratorium rujukan | |
| storage, disposal | penyimpanan, pemusnahan | |
| holding time | masa simpan | |
| compliance standard | standar kepatuhan | |
| compliance certificate | sertifikat kepatuhan | Indonesian title *Sertifikat Hasil Uji* kept as is |
| pool, pooling | pool, penggabungan sampel (pooling) | |
| deconvolution | dekonvolusi | |
| field survey | survei lapangan | |
| entomological indices | indeks entomologi | |
| program, questionnaire | program, kuesioner | |
| dictionary entry | entri kamus | |
| provider (requesting clinician) | dokter pengirim | UI label **Penyelenggara** quoted as-is |
| organization | organisasi | |
| sampling site | tempat pengambilan sampel | UI **Tempat Pengambilan Sampel** |
| site (the lab installation) | situs | |
| patient | pasien | |
| user account, role, permission | akun pengguna, peran, izin akses | |
| electronic signature | tanda tangan elektronik | |
| audit trail | jejak audit | |
| lab notebook | buku catatan laboratorium | UI **Notebook** |
| analyzer | alat analisis (analyzer) | UI **Alat** |
| analyzer bridge | Analyzer Bridge | product component name |
| dashboard | dasbor | |
| settings, configuration | pengaturan, konfigurasi | |
| search index | indeks pencarian | |
| non-working days | hari libur | |
| turnaround time (TAT) | waktu penyelesaian (TAT) | UI **Waktu Penyelesaian** |
| barcode | kode batang | UI says **Kode QR**; quote it as-is |
| label preset | preset label | UI **Pengaturan Label** |
| upgrade, backup, restore | pembaruan versi (upgrade), pencadangan (backup), pemulihan (restore) | |
| high availability, failover | ketersediaan tinggi (high availability), failover | |
| server, workstation | server, komputer kerja | |
| deployment | penerapan | |
| release (software version) | rilis | |
| draft | draf | |
| AMR (antimicrobial resistance) | resistansi antimikroba (AMR) | |
| standby server | server cadangan (standby) | |
| primary server | server utama | |
| promote (a standby) | mempromosikan | |
| fence (a node) | mengisolasi | |
| rejoin | bergabung kembali | |
| switchover / failback | peralihan terencana / pengembalian (failback) | |
| snapshot | snapshot | |
| replication slot, WAL | replication slot, WAL | kept in English |
| configuration folder names (`tests`, `sample-types`) | unchanged | they are file paths |

## Known weaknesses in the Indonesian UI strings (quote as-is in the docs, report upstream)

- Barcode is rendered **Kode QR** (a QR code is one kind of barcode).
- Provider (requesting clinician) is **Penyelenggara** (literally "organizer").
- Order is rendered both **Pemesanan** and **Permintaan** (for example **Berdasarkan Permintaan** under
  Results, **Konfigurasi Entri Permintaan**).
- **Edit Order** under Generic Sample is **Edit Sampel**; **Create Order** there is **Penerimaan Sampel**.
- **Site Information** is **Pengaturan Informasi Aplikasi**.
