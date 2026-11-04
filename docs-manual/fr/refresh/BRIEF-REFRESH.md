# Refresh brief: update stale French pages (only the changed segments)

KIT is the folder holding this brief; ROOT is the working folder named by whoever sent you here.

Read `KIT/TRANSLATOR.md` first and follow it, with these differences:

- Your batch is `ROOT/work/batchNN.json`. Each page lists ONLY the segments whose English
  changed since the last French translation. The rest of the page is already in French and is kept.
- `context` maps a segment id to the French text of the segment just before it on the page. Use it to keep
  the same terms, register and style as the existing French. Do not translate the context.
- Title: if `titleChanged` is false, output `frTitle` unchanged. If true, translate the new English `title`
  (the old French title is in `frTitle` for reference; if only punctuation changed, keep `frTitle` with the
  same punctuation change, for example "Admin — X" became "Admin: X" so "Admin — Y" becomes "Admin : Y").
- Output: `ROOT/out/<page>.json` as `{"page": ..., "title": ..., "segs": {"sN": ...}}`
  with every listed segment id. Validate with
  `python3 KIT/validate.py ROOT/work/batchNN.json` until it prints OK.

Settled terms since the glossary was written (they override it):
- Lab order = **demande** (demande clinique, demande environnementale). Never "ordonnance" or "commande" for a
  lab order; "commande" only for inventory purchase orders. The UI now says "Demande", so quote the `ui` map.
- Test = analyse (but the screen name "Catalogue de tests" stays as the UI shows it). Sample = échantillon.
- QC = CQ, EQA = EEQ, NCE = ENC. Provider (clinician) = prescripteur. Sex = sexe.
- QC control levels High/Low = Haut / Bas; result flags High/Low = Élevé / Faible.
- Straight apostrophe ' only in your own text. Never use em dashes (—) of your own.
- These pages show English screenshots, so keep the English gloss in italics after the first bold UI label.
