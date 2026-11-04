#!/bin/bash
# Docs UI-drift check, then the bench summary.
# Runs once per base that any live contract points at (read from contracts.json, so a new
# base such as pngtest is picked up automatically). drift-report.json is upserted by section
# id and pruned of rows no contract backs, so the runs accumulate into one clean report.
# Afterwards docs-manual/bench-drift.json is what the Documentation triage bench reads:
#   - drop it on the bench's "Load drift report" button, or
#   - ask Claude "sync the triage bench" (it reads the file from this folder).
export PATH="$HOME/.nvm/versions/node/v24.11.0/bin:$PATH"
cd "$HOME/Documents/OpenELIS QA" || exit 1
rm -f drift.done drift.log
BASES=$(python3 -c "import json;print('\n'.join(sorted({s['base'] for s in json.load(open('docs-manual/contracts.json'))['sections'] if not s.get('retired')})))")
for BASE_URL in $BASES; do
  echo "=== drift check: $BASE_URL ($(date -u +%FT%TZ)) ===" >> drift.log
  # One test walks every section for the base, so it needs far more than the default 120 s.
  BASE="$BASE_URL" npx playwright test --project=docs tests/docs/drift.check.spec.ts --timeout=1800000 >> drift.log 2>&1 \
    || echo "!!! $BASE_URL run failed, see above" >> drift.log
done
[ -f docs-manual/commit-doc-impact.py ] && python3 docs-manual/commit-doc-impact.py >> drift.log 2>&1
python3 docs-manual/bench_summary.py | tee -a drift.log
# French translation freshness (docs spine): writes docs-manual/bench-translations.json
if [ -f docs-manual/fr/translation-freshness.py ]; then
  for L in $(python3 -c "import json;print(' '.join(k for k,v in json.load(open('docs-manual/fr/langs.json')).items() if v.get('home')))"); do
    echo "=== translation freshness: $L ===" >> drift.log
    OE_LANG=$L python3 docs-manual/fr/translation-freshness.py 2>&1 | tee -a drift.log
  done
fi
echo DONE > drift.done
