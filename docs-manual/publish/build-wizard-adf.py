import json

PAGE = '1648361491'
p = json.load(open('/tmp/page.json'))
assert p['id'] == PAGE, 'GUARD: got page %s, expected %s' % (p['id'], PAGE)
adf = json.loads(p['body']['atlas_doc_format']['value'])
fid = json.load(open('/tmp/fileids.json'))

F2 = '04-wizard-step2-verify.png'
F3 = '05-wizard-step3-connect.png'


def media(fname, alt, caption):
    return {
        "type": "mediaSingle",
        "attrs": {"layout": "center", "width": 760, "widthType": "pixel"},
        "content": [
            {"type": "media", "attrs": {"width": 2880, "height": 1800, "alt": alt,
                                        "id": fid[fname], "collection": "contentId-" + PAGE,
                                        "type": "file"}},
            {"type": "caption", "content": [{"type": "text", "text": caption,
                                             "marks": [{"type": "em"}]}]},
        ],
    }


def text_of(node):
    if node.get('type') == 'text':
        return node.get('text', '')
    return ''.join(text_of(x) for x in (node.get('content') or []))


c = adf['content']

already = [i for i, n in enumerate(c) if n.get('type') == 'mediaSingle'
           and any(m.get('attrs', {}).get('id') in (fid[F2], fid[F3])
                   for m in (n.get('content') or []))]
if already:
    print('ALREADY-PRESENT at', already, '- nothing inserted')
else:
    i_verify = next(i for i, n in enumerate(c)
                    if n.get('type') == 'paragraph'
                    and text_of(n).strip() == 'Then Continue to Connect.')
    i_connect = next(i for i, n in enumerate(c)
                     if n.get('type') == 'paragraph'
                     and text_of(n).startswith('Finish with')
                     and 'Save and finish later' in text_of(n))
    print('anchors: verify-para', i_verify, 'connect-para', i_connect)

    # insert the later one first so the earlier index stays valid
    c.insert(i_connect + 1, media(
        F3,
        'Step 3, Connect: Data flow set to Results only, an empty required Directory field, '
        'the file pattern, Test connection, and the activation readiness notice above the '
        'finish actions.',
        'Step 3 for a FILE analyzer: the connection fields, activation readiness, and the finish actions.'))
    c.insert(i_verify, media(
        F2,
        'Step 2, Verify: step 1 collapsed to a summary, with tests mapped, results mapped, '
        'the control result recognition rules and the current confirmation.',
        'Step 2 presents the analyzer type mappings and control-recognition rules for review.'))

for node in c:
    if node.get('type') != 'table':
        continue
    for row in (node.get('content') or []):
        cells = row.get('content') or []
        if len(cells) == 2 and text_of(cells[0]).strip() == 'Figures':
            cells[1]['content'] = [{"type": "paragraph", "content": [{
                "type": "text",
                "text": "5 attached, 1440×900 at 2x. Steps 1-3 of the wizard are all "
                        "captured; steps 2 and 3 were taken on 22 September 2026."}]}]
            print('provenance Figures row updated')

out = {
    "id": PAGE,
    "status": "current",
    "title": p['title'],
    "version": {"number": p['version']['number'] + 1,
                "message": "Add wizard step 2 (Verify) and step 3 (Connect) figures"},
    "body": {"representation": "atlas_doc_format", "value": json.dumps(adf)},
}
json.dump(out, open('/tmp/page-put.json', 'w'))
print('prepared version', out['version']['number'], '| nodes', len(c))
