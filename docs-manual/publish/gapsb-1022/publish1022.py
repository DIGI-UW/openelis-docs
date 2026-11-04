#!/usr/bin/env python3
"""Fork B, 22 Oct 2026: assemble figures and publish six pages serially, verifying each write."""
import importlib.util, json, os, re, shutil, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
PUB = os.path.join(os.path.dirname(HERE), 'confluence-publish.py')
spec = importlib.util.spec_from_file_location('pub', PUB)
pub = importlib.util.module_from_spec(spec); spec.loader.exec_module(pub)
b, a = pub.load_creds()
M = 'docs-media/'
IMGS = {
 'img-notif': {'n01-triggers.png': 'gapsb-notif/01-triggers.png', 'n02-templates.png': 'gapsb-notif/03-templates.png',
   'n03-channels.png': 'gapsb-notif/04-channels.png', 'n04-channel-email-edit.png': 'gapsb-notif/05-channel-email-edit.png',
   'n05-channel-sms-edit.png': 'gapsb-notif/06-channel-sms-edit.png', 'n06-channel-whatsapp-edit.png': 'gapsb-notif/07-channel-whatsapp-edit.png',
   'n07-delivery-settings.png': 'gapsb-notif/08-delivery-settings.png', 'n08-delivery-saved.png': 'gapsb-notif/09-delivery-saved.png'},
 'img-header': {'r01-printed-report-config-before.png': 'gapsb-rpt/01-printed-report-config-before.png',
   'r02-edit-site-name.png': 'gapsb-rpt/02-edit-site-name.png', 'r03-edit-header-left-image.png': 'gapsb-rpt/03-edit-header-left-image.png',
   'r04-printed-report-config-after.png': 'gapsb-rpt/04-printed-report-config-after.png'},
 'img-inv': {'g01-manage-tags.png': 'gapsb-inv/01-manage-tags.png', 'g02-receive-from-row.png': 'gapsb-fix/04-receive-from-row.png',
   'g03-received-lot-pending-qc.png': 'gapsb-fix/05-received-lot-pending-qc.png', 'g04-edit-lot.png': 'gapsb-fix2/01-edit-lot.png',
   'g05-update-qc-status.png': 'gapsb-fix2/02-update-qc-status.png', 'g06-lot-qc-passed.png': 'gapsb-fix2/03-zn-lot-passed.png',
   'g07-mark-as-ordered.png': 'gapsb-fix/01-mark-as-ordered.png', 'g08-marked-on-order.png': 'gapsb-fix/02-marked.png',
   'g09-count-confirmed.png': 'gapsb-inv/06-confirm-count.png', 'g10-import-applied.png': 'gapsb-inv/08-import-applied.png',
   'g11-alerts-low-stock.png': 'gapsb-inv/10-alerts-low-stock.png'},
 'img-recv': {'g12-delivery-received.png': 'gapsb-inv/09-delivery-received.png'},
 'img-none': {},
}
for d, m in IMGS.items():
    os.makedirs(os.path.join(HERE, d), exist_ok=True)
    for dst, src in m.items():
        shutil.copyfile(os.path.join(ROOT, M, src), os.path.join(HERE, d, dst))
shutil.copyfile(os.path.join(HERE, 'r05-report-header-printed.png'), os.path.join(HERE, 'img-header', 'r05-report-header-printed.png'))

JOBS = [  # page id, expected parent, xhtml, image dir, new page?
 ('1734017045', '1680441357', 'notif.xhtml', 'img-notif', True),
 ('1732739089', '1680441354', 'header.xhtml', 'img-header', True),
 ('1729134594', '1729363970', 'invitems.xhtml', 'img-inv', False),
 ('1729167388', '1729363970', 'invrecv.xhtml', 'img-recv', False),
 ('1729429517', '1679589479', 'rpq.xhtml', 'img-none', False),
 ('1729724423', '1679589479', 'sent.xhtml', 'img-none', False),
]
only = sys.argv[1:]
for pid, parent, x, imgdir, new in JOBS:
    if only and pid not in only: continue
    body = open(os.path.join(HERE, x)).read()
    if '—' in body or '&mdash;' in body: sys.exit(f'{x}: em dash')
    for t in re.findall(r'\{\{IMG:([^}]+)\}\}', body):
        if not os.path.exists(os.path.join(HERE, imgdir, t)): sys.exit(f'{x}: missing {t}')
    pre = pub.api(b, a, 'GET', f'/api/v2/pages/{pid}')
    if str(pre.get('parentId')) != parent: sys.exit(f'{pid}: parent {pre.get("parentId")} != {parent}')
    out = subprocess.run([sys.executable, PUB, '--page', pid, '--xhtml', os.path.join(HERE, x), '--images', os.path.join(HERE, imgdir)],
                         capture_output=True, text=True)
    print(out.stdout.strip()[-300:], out.stderr.strip()[-400:])
    if out.returncode: sys.exit(f'{pid}: publish failed')
    chk = pub.api(b, a, 'GET', f'/api/v2/pages/{pid}?body-format=storage')
    if str(chk['id']) != pid or str(chk.get('parentId')) != parent: sys.exit(f'{pid}: crossed write or moved')
    sv = chk['body']['storage']['value']
    if new:
        pub.api(b, a, 'POST', f'/rest/api/content/{pid}/label', [{'prefix': 'global', 'name': 'doc-in-review'}])
    labels = [l['name'] for l in pub.api(b, a, 'GET', f'/rest/api/content/{pid}/label').get('results', [])]
    att = [r['title'] for r in pub.api(b, a, 'GET', f'/rest/api/content/{pid}/child/attachment?limit=200').get('results', [])]
    refs = re.findall(r'ri:filename="([^"]+)"', sv)
    missing = [r for r in refs if r not in att]
    print('OK', pid, chk['title'], 'v', chk['version']['number'], 'parent', chk.get('parentId'), 'imgs', len(refs),
          'missing-att', missing, 'tokens', sv.count('{{IMG'), 'wip', 'Work in progress' in sv, labels)
