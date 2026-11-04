#!/bin/bash
set -euo pipefail
PAGE=1648361491
BASE=https://uwdigi.atlassian.net/wiki
cd "$HOME/Documents/OpenELIS QA/docs-manual/publish"
set -a; . "$HOME/.openelis/confluence.env"; set +a
AUTH=$(printf '%s:%s' "$CONFLUENCE_EMAIL" "$CONFLUENCE_API_TOKEN" | base64)
curl -s -H "Authorization: Basic $AUTH" \
  "$BASE/api/v2/pages/$PAGE?body-format=atlas_doc_format" > /tmp/page.json
python3 build-wizard-adf.py
curl -s -H "Authorization: Basic $AUTH" -H 'Content-Type: application/json' -X PUT \
  --data @/tmp/page-put.json "$BASE/api/v2/pages/$PAGE" > /tmp/put-result.json
python3 -c "import json;d=json.load(open('/tmp/put-result.json'));print('PUT id=',d.get('id'),'| version=',(d.get('version') or {}).get('number'),'| title=',d.get('title'),'| err=',d.get('errors'))"
