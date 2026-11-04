#!/bin/bash
cd "$(dirname "$0")/.."
python3 confluence-publish.py --create --space OG --parent 1189609473 --title "Complete the sample check for a clinical order" --xhtml order-entry-v4/sample-check.xhtml --images order-entry-v4/img-check > order-entry-v4/pub1.log 2>&1
echo $? > order-entry-v4/pub1.done
