p = '/tmp/land3/1326972929.xhtml'
s = open(p).read()
R = [
 ('<ac:link-body>Work plans</ac:link-body></ac:link></p></td><td><p>Build work lists for a lab unit, a technician or a test. Older format.</p>',
  '<ac:link-body>Print a work plan</ac:link-body></ac:link></p></td><td><p>List the tests waiting in a lab unit, test, panel or priority, and print the work plan. In review.</p>'),
 ('<ac:link-body>Label and store samples (shared stage)</ac:link-body></ac:link></p></td><td><p>Print order and specimen labels and assign each sample a storage location. In review.</p>',
  '<ac:link-body>Label and store environmental and vector samples</ac:link-body></ac:link></p></td><td><p>Print order and sample labels and assign storage for environmental and vector orders. In review.</p>'),
 ('<ac:link-body>Complete QA review (shared stage)</ac:link-body></ac:link></p></td><td><p>Run the sample acceptance checks on each specimen and submit the order into testing.</p>',
  '<ac:link-body>Complete the sample check for an environmental or vector order</ac:link-body></ac:link></p></td><td><p>Run the acceptance checklist on each sample and release the order for testing. In review.</p>'),
]
for a, b in R:
    assert s.count(a) == 1, a[:50]
    s = s.replace(a, b)
open(p, 'w').write(s); print('ok')
