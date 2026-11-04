#!/bin/bash
cd "$HOME/Documents/OpenELIS QA/docs-manual/publish"
/usr/bin/python3 confluence-publish.py --create --space OG --parent 1189609473 \
  --title "Receive and activate a control lot" \
  --xhtml ../qc/qc-lot.xhtml --images ../qc/images-lot > qc-lot-pub.log 2>&1
echo DONE >> qc-lot-pub.log
