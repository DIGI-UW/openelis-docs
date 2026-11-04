p = '/tmp/mq2/1648590851.xhtml'
s = open(p).read()
R = [
 ('ac:original-height="1800" ac:original-width="2880" ac:custom-width="true" ac:alt="Columns - Lot Number, Control Material, Manufacturer, Control Level, Status, Calculation Method and Expiration Date." ac:width="760"><ri:attachment ri:filename="08-qc-control-lots.png" ri:version-at-save="1" />',
  'ac:original-height="446" ac:original-width="1800" ac:custom-width="true" ac:alt="Control Lots list with lot 26541, Lyphochek Assayed Chemistry Control, Normal level, Active, Manufacturer Fixed, expiring 31/03/2027." ac:width="1020"><ri:attachment ri:filename="08-qc-control-lots.png" />'),
 ('Figure 8. Control lots, with control level, calculation method and expiration date.',
  'Figure 8. Control lots in 3.3.0: one active Normal-level lot with manufacturer-fixed mean and standard deviation.'),
 ('The other methods in the list were not exercised for this page.',
  'The other two methods are <em>Rolling Window</em> (recalculate from the most recent N results) and <em>Initial Runs</em> (calculate once from the first N establishment runs); they were not exercised for this page. See <a href="https://uwdigi.atlassian.net/wiki/spaces/OG/pages/1680048146">Receive and activate a control lot</a>.'),
 ('Figures 1, 2 and 4 are new. Part 2 and Part 3 figures are from 3.2.2.0.',
  'Figures 1, 2 and 4 are new; Figure 8 was recaptured on testing on 13 October 2026. Figures 3 and 5 to 7 are from 3.2.2.0: testing has no held results, QC instruments, control results or rule sets yet, so those screens cannot be recaptured with data.'),
]
for a, b in R:
    assert s.count(a) == 1, a[:60]
    s = s.replace(a, b)
open(p, 'w').write(s); print('ok')
