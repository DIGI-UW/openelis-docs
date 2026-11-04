#!/bin/bash
cd "$HOME/Documents/OpenELIS QA/docs-manual/publish"
/usr/bin/python3 confluence-publish.py --page 1679949842 \
  --xhtml ../programs-v2/programs-v2.xhtml --images ../programs-v2/images > programs-pub.log 2>&1
echo DONE >> programs-pub.log
