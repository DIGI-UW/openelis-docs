import importlib.util, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('pub', os.path.join(os.path.dirname(HERE), 'confluence-publish.py'))
pub = importlib.util.module_from_spec(spec); spec.loader.exec_module(pub)
b, a = pub.load_creds()
R = {
 '1729429517': [
   ('<li>Known issue OGC-1529 (being fixed): when a printed result is corrected but the correction is not yet validated, printing can issue a new version that leaves that result out. Validate the correction before you reprint.</li>', ''),
   ('This is a known issue on the instance documented here.', 'This is a known issue on the instance documented here (OGC-1550).'),
   ("Check your server's time zone setting if they differ at your site.", "Check your server's time zone setting if they differ at your site. Reported as OGC-1550."),
   ('the Subject column shows a number in place of the national ID.', 'the Subject column shows a number in place of the national ID (OGC-1550).'),
 ],
 '1729724423': [('Resend creates a new row rather than updating the old one, so a message can appear more than once.', 'Resend creates a new row rather than updating the old one, so a message can appear more than once (OGC-1551).')],
 '1729134594': [('Known issue: the ', 'Known issue (OGC-1549): the '), ('Known issue: on the test server the expiry', 'Known issue (OGC-1549): on the test server the expiry')],
 '1729167388': [('Known issue: on the test server the ', 'Known issue (OGC-1549): on the test server the ')],
 '1729462279': [('<strong>Known issue:</strong>', '<strong>Known issue (OGC-1548):</strong>'), ('is cut off; scroll the table sideways to reach it.', 'is cut off; scroll the table sideways to reach it (OGC-1552).')],
 '1729789973': [('listed on the worklist (OGC-1525).', 'listed on the worklist (OGC-1525, OGC-1553).'), ('rather than plain descriptions.', 'rather than plain descriptions (OGC-1553).'), ('although it was filled in (Outpatient).', 'although it was filled in (Outpatient) (OGC-1553).')],
}
for pid, reps in R.items():
    p = pub.api(b, a, 'GET', f'/api/v2/pages/{pid}?body-format=storage')
    if str(p['id']) != pid: sys.exit('crossed read ' + pid)
    s = p['body']['storage']['value']
    for old, new in reps:
        n = s.count(old)
        if n != 1: sys.exit(f'{pid}: {n} matches for {old[:50]!r}')
        s = s.replace(old, new)
    if '—' in s: sys.exit(pid + ' em dash')
    r = pub.api(b, a, 'PUT', f'/api/v2/pages/{pid}', {'id': pid, 'status': 'current', 'title': p['title'],
        'body': {'representation': 'storage', 'value': s},
        'version': {'number': p['version']['number'] + 1, 'message': 'Known issues cite their Jira tickets'}})
    print(pid, 'v', r['version']['number'])
