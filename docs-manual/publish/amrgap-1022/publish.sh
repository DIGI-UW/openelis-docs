#!/bin/bash
set -e
cd "$HOME/Documents/OpenELIS QA"
P=docs-manual/publish/amrgap-1022; I=$P/img; mkdir -p $I
cp docs-media/amrgap-admin/01-add-program.png $I/08-program-new.png
cp docs-media/amrgap-admin/02-program-list.png $I/09-program-list.png
cp docs-media/amrgap-case/01-case-program-order-detail.png $I/10-program-on-case.png
cp docs-media/amrgap-admin/03-molecular-mappings.png $I/11-molecular-mappings.png
cp docs-media/amrgap-admin/04-molecular-mapping-dialog.png $I/12-molecular-mapping-dialog.png
cp docs-media/amrgap-admin/05-patient-origins.png $I/13-patient-origins.png
cp docs-media/amrgap-case/01-case-program-order-detail.png $I/13-case-info-program.png
cp docs-media/amrgap-case/02-add-reading.png $I/14-add-reading.png
cp docs-media/amrgap-case/03-record-outcome.png $I/15-record-outcome.png
cp docs-media/amrgap-case/04-culture-positive.png $I/16-culture-positive.png
cp docs-media/amrgap-case/05-subculture-dialog.png $I/17-subculture-dialog.png
cp docs-media/amrgap-extra/01-subculture-card.png $I/18-subculture-card.png
cp docs-media/amrgap-case/06-extend-incubation.png $I/19-extend-incubation.png
cp docs-media/amrgap-case/07-incubation-extended.png $I/20-incubation-extended.png
cp docs-media/amrgap-critical/01-critical-form.png $I/21-critical-form.png
cp docs-media/amrgap-critical/02-critical-logged.png $I/22-critical-logged.png
cp docs-media/amrgap-extra/02-whonet-csv-generated.png $I/15-whonet-csv-generated.png
for id in 1729167362 1729789973 1729331248; do
  echo "== $id"
  python3 docs-manual/publish/confluence-publish.py --page $id --xhtml $P/$id.xhtml --images $I 2>&1 | tail -4
done
for id in 1729167362 1729789973 1729331248; do cp $P/$id.orig.xhtml $P/$id.before.xhtml; done
python3 scratch/amrgap/amrgap_fetch.py 1729167362 1729789973 1729331248 2>&1 | tail -3
touch amrgap-pub.done
