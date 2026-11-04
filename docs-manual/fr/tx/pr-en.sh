#!/bin/bash
set -e
export PATH=/opt/homebrew/bin:/usr/local/bin:$PATH
HERE="$(cd "$(dirname "$0")" && pwd)"
W=$(mktemp -d /tmp/oe-en.XXXX)
git clone -q --depth 1 --branch develop https://github.com/DIGI-UW/OpenELIS-Global-2.git "$W/repo"
cd "$W/repo"
git checkout -q -b chore/i18n-english-terms
git apply --3way "$HERE/english-terms.patch"
git add -A
git commit -q -F "$HERE/pr-en-commit.txt"
git push -q -u origin chore/i18n-english-terms
URL=$(gh pr create -R DIGI-UW/OpenELIS-Global-2 --base develop --head chore/i18n-english-terms --title "chore(i18n): standardize English terms (Lab Number, Lab Unit, Provider, Sample, Analyzer)" --body-file "$HERE/pr-en-body.md")
echo "PR: $URL"
gh pr comment "$URL" --body-file "$HERE/pr-en-comment-1.md" >/dev/null
gh pr comment "$URL" --body-file "$HERE/pr-en-comment-2.md" >/dev/null
echo DONE
