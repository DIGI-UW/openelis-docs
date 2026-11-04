#!/bin/bash
set -euo pipefail
PAGE=1648361491
BASE=https://uwdigi.atlassian.net/wiki
SRC="$HOME/Documents/OpenELIS QA/docs-media/analyzer-wizard"
set -a; . "$HOME/.openelis/confluence.env"; set +a
AUTH=$(printf '%s:%s' "$CONFLUENCE_EMAIL" "$CONFLUENCE_API_TOKEN" | base64)
H=(-H "Authorization: Basic $AUTH")

echo '--- existing attachments ---'
curl -s "${H[@]}" "$BASE/rest/api/content/$PAGE/child/attachment?limit=200" > /tmp/att-before.json
python3 -c "import json;d=json.load(open('/tmp/att-before.json'));print([(r['title'], r['id']) for r in d['results']])"

for f in 04-wizard-step2-verify.png 05-wizard-step3-connect.png; do
  EX=$(python3 -c "import json,sys;d=json.load(open('/tmp/att-before.json'));m={r['title']:r['id'] for r in d['results']};print(m.get('$f',''))")
  if [ -n "$EX" ]; then URL="$BASE/rest/api/content/$PAGE/child/attachment/$EX/data"; else URL="$BASE/rest/api/content/$PAGE/child/attachment"; fi
  echo "uploading $f -> $URL"
  curl -s "${H[@]}" -H 'X-Atlassian-Token: nocheck' -F "file=@$SRC/$f" -X POST "$URL" > /tmp/up-$f.json
  head -c 160 /tmp/up-$f.json; echo
done

echo '--- fileIds ---'
curl -s "${H[@]}" "$BASE/rest/api/content/$PAGE/child/attachment?limit=200" > /tmp/att-after.json
python3 -c "
import json
d=json.load(open('/tmp/att-after.json'))
out={r['title']: r.get('extensions',{}).get('fileId') for r in d['results']}
json.dump(out, open('/tmp/fileids.json','w'), indent=1)
print(json.dumps(out, indent=1))
"
