#!/bin/bash
cd "$(dirname "$0")/.."
python3 confluence-publish.py --page 1648787462 --title "Enter a clinical order" --xhtml order-entry-v4/enter-order.xhtml --images order-entry-v4/img-enter > order-entry-v4/pub2.log 2>&1
python3 confluence-publish.py --page 1655930882 --title "Prepare samples for a clinical order" --xhtml order-entry-v4/prepare-samples.xhtml --images order-entry-v4/img-prepare >> order-entry-v4/pub2.log 2>&1
echo $? > order-entry-v4/pub2.done
