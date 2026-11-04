import importlib.util, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('pub', os.path.join(os.path.dirname(HERE), 'confluence-publish.py'))
pub = importlib.util.module_from_spec(spec); spec.loader.exec_module(pub)
b, a = pub.load_creds()
# 1. pages: drop the expiry known-issue tip
for pid in ['1729134594', '1729167388']:
    p = pub.api(b, a, 'GET', f'/api/v2/pages/{pid}?body-format=storage')
    if str(p['id']) != pid: sys.exit('crossed read ' + pid)
    s = p['body']['storage']['value']
    lis = re.findall(r'<li>(?:(?!</li>).)*one day earlier(?:(?!</li>).)*</li>', s, flags=re.S)
    if len(lis) != 1: sys.exit(f'{pid}: {len(lis)} matching tips')
    s = s.replace(lis[0], '')
    r = pub.api(b, a, 'PUT', f'/api/v2/pages/{pid}', {'id': pid, 'status': 'current', 'title': p['title'],
        'body': {'representation': 'storage', 'value': s},
        'version': {'number': p['version']['number'] + 1, 'message': 'Expiry date note removed (tracked elsewhere)'}})
    print(pid, 'v', r['version']['number'])
# 2. Jira OGC-1549: keep only the tag-filter issue
jb = b[:-len('/wiki')] if b.endswith('/wiki') else b
desc = ("Found 21 Oct 2026 on testing.openelis-global.org (header 3.4.0-SNAPSHOT). Not covered by OGC-1489.\n\n"
        "*Steps:* Main menu > Inventory > Items, set Filter by Tags to \"Central laboratory\".\n\n"
        "*Expected:* the Reorder now banner and the Reorder suggestions dialog list only items carrying the tag, as the board does (or say clearly that they cover all items).\n\n"
        "*Actual:* the board narrows to the tag, but the banner still names items without it (QA_AUTO_1011_REAGENT_157560, QA INV Empty, QA INV Low) and Reorder suggestions (7) lists them too.\n\n"
        "Cited as a known issue on the manual page \"Manage inventory items, lots, counts and reorders\" (https://uwdigi.atlassian.net/wiki/spaces/OG/pages/1729134594).\n\n"
        "(The lot expiry shown one day early, first listed here, is already known to the team and tracked elsewhere; removed 22 Oct.)")
pub.api(jb, a, 'PUT', '/rest/api/2/issue/OGC-1549', {'fields': {
    'summary': '[QA 3.3.0] Inventory items board: the Reorder now banner and Reorder suggestions ignore the tag filter',
    'description': desc}})
j = pub.api(jb, a, 'GET', '/rest/api/2/issue/OGC-1549?fields=summary')
print('OGC-1549:', j['fields']['summary'])
