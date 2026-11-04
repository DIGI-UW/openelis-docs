#!/bin/bash
# Opens the PR that removes unused en.json keys. Run from docs-manual/fr/tx.
set -e
export PATH=/opt/homebrew/bin:/usr/local/bin:$PATH
HERE="$(cd "$(dirname "$0")" && pwd)"
W=$(mktemp -d /tmp/oe-trim.XXXX)
git clone -q --depth 1 --branch develop https://github.com/DIGI-UW/OpenELIS-Global-2.git "$W/repo"
cd "$W/repo"
BASE=$(git hash-object frontend/src/languages/en.json)
if [ "$BASE" != "cde8205a54cc39a2a98d3d6fdd2d5fcb390c6799" ]; then echo "STOP: en.json changed on develop since the audit ($BASE)"; exit 2; fi
git checkout -q -b chore/i18n-remove-unused-keys
cp "$HERE/en.trimmed.json" frontend/src/languages/en.json
git add frontend/src/languages/en.json
git commit -q -F "$HERE/commit-msg.txt"
git push -q -u origin chore/i18n-remove-unused-keys
URL=$(gh pr create -R DIGI-UW/OpenELIS-Global-2 --base develop --head chore/i18n-remove-unused-keys --title "chore(i18n): remove 1,652 unused keys from en.json" --body-file "$HERE/pr-body.md")
echo "PR: $URL"
gh pr comment "$URL" --body-file "$HERE/pr-comment-1.md" >/dev/null
gh pr comment "$URL" --body-file "$HERE/pr-comment-2.md" >/dev/null
SAM=$(gh api repos/DIGI-UW/OpenELIS-Global-2/pulls/4365 --jq .user.login)
gh pr edit "$URL" --add-reviewer "$SAM" >/dev/null && echo "review requested: $SAM" || echo "review request failed for $SAM"
echo DONE
