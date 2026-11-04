#!/bin/bash
cd "$HOME/Documents/OpenELIS QA/docs-manual/publish"
/usr/bin/python3 confluence-publish.py --create --space OG --parent 1189609473 \
  --title "Statistical QC — overview and daily review" \
  --xhtml ../qc/qc-overview.xhtml --images ../qc/images-overview > qc-overview-pub.log 2>&1
echo DONE >> qc-overview-pub.log
