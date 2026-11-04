import json

PAGE = '1648361491'
p = json.load(open('/tmp/verify.json'))
assert p['id'] == PAGE, 'GUARD: got %s' % p['id']
adf = json.loads(p['body']['atlas_doc_format']['value'])

ALT = {
    '4d43c640-b8b1-4740-b338-89af3e9e43ab': 'Wizard step 2, Verify: analyzer type mappings and control rules',
    'cb461023-cd0f-4436-a0b5-f40a738bd5c5': 'Wizard step 3, Connect: connection fields and finish actions',
}

n = 0
for node in adf['content']:
    if node.get('type') != 'mediaSingle':
        continue
    for m in (node.get('content') or []):
        if m.get('type') == 'media' and m['attrs'].get('id') in ALT:
            m['attrs']['alt'] = ALT[m['attrs']['id']]
            n += 1
print('set alt on', n, 'media nodes')

out = {
    "id": PAGE, "status": "current", "title": p['title'],
    "version": {"number": p['version']['number'] + 1, "message": "Alt text for the step 2 and 3 figures"},
    "body": {"representation": "atlas_doc_format", "value": json.dumps(adf)},
}
json.dump(out, open('/tmp/page-put.json', 'w'))
print('prepared version', out['version']['number'])
