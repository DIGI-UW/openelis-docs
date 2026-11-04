"""Publish French translations built in fr/build/ (plan.json + <en>.json ADF).

Phases (resumable, state in fr/state.json):
  folders  create the French folder tree under the French landing
  pages    create missing French pages (placeholder body) so every twin has an id
  content  per page: copy figures, remap links to French twins, prepend the translation notice,
           write the body, move to the right parent, set Lango + openelis-translation properties, label
  trash    move duplicate French pages to the trash
Usage: python3 fr/fr-publish.py [phase ...] [--only EN_ID ...]
"""
import json, os, sys, re, copy, uuid, datetime, urllib.parse, mimetypes
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from frlib import *

BUILD = lp('build')
STATE = lp('state')
plan = json.load(open(os.path.join(BUILD, 'plan.json')))
state = json.load(open(STATE)) if os.path.exists(STATE) else {'folders': {}, TW: {}, 'done': {}, 'log': []}
def save(): json.dump(state, open(STATE, 'w'), ensure_ascii=False, indent=1)
def log(*a):
    s = ' '.join(str(x) for x in a); print(s, flush=True); state['log'].append(s[:300])

args = sys.argv[1:]
only = set(args[args.index('--only') + 1:]) if '--only' in args else None
phases = [a for a in (args[:args.index('--only')] if '--only' in args else args)] or ['folders', 'pages', 'content']
ROOT = plan.get('root') or plan.get('frRoot')   # translated manual root (twin of 1326972929)
SPACE = get('/api/v2/spaces?keys=OG')['results'][0]['id']
TODAY = datetime.date.today().isoformat()
pages = plan['pages']
for p in pages:
    if p.get(TW): state[TW].setdefault(p['en'], p[TW])
save()

# ---------- folders ----------
def make_folder(title, parent):
    try:
        r = req('POST', '/api/v2/folders', {'spaceId': SPACE, 'title': title, 'parentId': parent})
        return r['id']
    except RuntimeError as e:
        log('folder API failed, using a page:', e)
        r = req('POST', '/api/v2/pages', {'spaceId': SPACE, 'status': 'current', 'title': title, 'parentId': parent,
                 'body': {'representation': 'atlas_doc_format', 'value': json.dumps({'type': 'doc', 'version': 1, 'content': [{'type': 'extension', 'attrs': {'extensionType': 'com.atlassian.confluence.macro.core', 'extensionKey': 'children', 'parameters': {'macroParams': {}}}}]})}})
        return r['id']

if 'folders' in phases:
    F = plan['folders']
    for key in ['EUM', 'ADM'] + [k for k in F if k not in ('EUM', 'ADM')]:
        if key in state['folders']: continue
        title, pk = F[key]
        parent = ROOT if pk == 'ROOT' else state['folders'][pk]
        state['folders'][key] = make_folder(title, parent); save()
        log('folder', key, title, '->', state['folders'][key])

ROOT_KEYS = {'EUM': '1329758211', 'ADM': '257458193'}
def mirror_parent(en):
    """French twin of the English page's current parent (the French tree mirrors the English one)."""
    try: ep = get('/api/v2/pages/%s' % en).get('parentId')
    except RuntimeError: return None
    M = dict(state.get('parentOnly', {}))
    M.update({ROOT_KEYS.get(k, k): v for k, v in state['folders'].items()})
    M.update(state[TW])
    return M.get(ep)

def parent_id(p):
    mp = mirror_parent(p['en'])
    if mp: return mp
    return _plan_parent(p)

def _plan_parent(p):
    k = p['parent']['kind']
    if k == 'id': return p['parent']['id']
    if k == 'folder': return state['folders'][p['parent']['key']]
    return state[TW][p['parent']['en']]

# order so twin parents come first
order, seen = [], set()
byen = {p['en']: p for p in pages}
def visit(p):
    if p['en'] in seen: return
    if p['parent']['kind'] == 'twin' and p['parent']['en'] in byen: visit(byen[p['parent']['en']])
    seen.add(p['en']); order.append(p)
for p in pages: visit(p)

# ---------- pages ----------
def unique_title(t):
    q = '/rest/api/content?' + urllib.parse.urlencode({'spaceKey': 'OG', 'title': t})
    return t if not get(q)['results'] else t + L['titleSuffix']

if 'pages' in phases:
    for p in order:
        if only and p['en'] not in only: continue
        if p['en'] in state[TW]: continue
        t = unique_title(p['title'])
        r = req('POST', '/api/v2/pages', {'spaceId': SPACE, 'status': 'current', 'title': t, 'parentId': parent_id(p),
                 'body': {'representation': 'atlas_doc_format', 'value': json.dumps({'type': 'doc', 'version': 1, 'content': [{'type': 'paragraph', 'content': [{'type': 'text', 'text': L['placeholder']}]}]})}})
        state[TW][p['en']] = r['id']; save(); log('created', p['en'], '->', r['id'], t)

# ---------- content ----------
EN2FR = dict(state[TW]); EN2FR.setdefault('1326972929', ROOT)
PAGE_RE = re.compile(r'(/wiki/spaces/[^/]+/pages/|/pages/viewpage\.action\?pageId=|/wiki/x/)(\d+)(/[^?#]*)?')
def remap_url(u):
    m = PAGE_RE.search(u or '')
    if not m or m.group(2) not in EN2FR: return u
    fr = EN2FR[m.group(2)]
    return 'https://uwdigi.atlassian.net/wiki/spaces/oeg/pages/%s' % fr + (u[m.end():] if u[m.end():].startswith('#') else '')

def attachments(pid):
    out = []; u = '/api/v2/pages/%s/attachments?limit=100' % pid
    while u:
        d = get(u); out += d['results']; u = d.get('_links', {}).get('next')
    return out

def upload(fr, title, data, mtype):
    bnd = uuid.uuid4().hex
    body = (('--%s\r\nContent-Disposition: form-data; name="file"; filename="%s"\r\nContent-Type: %s\r\n\r\n' % (bnd, title.replace('"', ''), mtype)).encode()
            + data + ('\r\n--%s\r\nContent-Disposition: form-data; name="minorEdit"\r\n\r\ntrue\r\n--%s--\r\n' % (bnd, bnd)).encode())
    r = req('PUT', '/rest/api/content/%s/child/attachment' % fr, body,
            {'Content-Type': 'multipart/form-data; boundary=' + bnd, 'X-Atlassian-Token': 'nocheck'})
    r = r['results'][0] if 'results' in r else r
    return r['extensions']['fileId']

def set_prop(pid, key, value):
    try:
        cur = get('/rest/api/content/%s/property/%s' % (pid, key))
        req('PUT', '/rest/api/content/%s/property/%s' % (pid, key), {'key': key, 'value': value, 'version': {'number': cur['version']['number'] + 1}})
    except RuntimeError as e:
        if '-> 404' not in str(e): raise
        req('POST', '/rest/api/content/%s/property' % pid, {'key': key, 'value': value})

def lango_value(lang, orig, status):
    names = {LANG_CODE: (L['name'], L['native']), 'en': ('English', 'English')}[lang]
    return {'name': {'value': names[0]}, 'title': names[0], 'tooltip': {'value': 'Switch Language'},
            'icon': 'https://cdn.adapps.it/lango/images/flags/%s.svg' % lang, 'langVersion': 4,
            'lang': {'code': lang, 'name': names[0], 'nativeName': names[1]}, 'originalContentId': orig, 'langStatus': status}

def notice(p, enver):
    return {'type': 'panel', 'attrs': {'panelType': 'note'}, 'content': [{'type': 'paragraph', 'content': [
        {'type': 'text', 'text': L['noticeBefore']},
        {'type': 'text', 'text': p['enTitle'] if LANG_CODE == 'fr' else p['enTitle'].replace(' — ', ': ').replace('—', ':'), 'marks': [{'type': 'link', 'attrs': {'href': 'https://uwdigi.atlassian.net/wiki/spaces/oeg/pages/%s' % p['en']}}]},
        {'type': 'text', 'text': L['noticeAfter'].format(v=enver, d=TODAY)}]}]}

if 'content' in phases:
    for p in order:
        en = p['en']
        if only and en not in only: continue
        if state['done'].get(en) == p['enVersion'] and not only: continue
        fr = state[TW][en]
        b = json.load(open(os.path.join(BUILD, en + '.json')))
        adf = copy.deepcopy(b['adf'])
        enpage = get('/api/v2/pages/%s' % en)
        if enpage['version']['number'] != p['enVersion']:
            log('WARN', en, 'English changed since translation:', p['enVersion'], '->', enpage['version']['number'], '(publishing anyway; tracker will flag it)')
        # figures
        ena = {a.get('fileId'): a for a in attachments(en)}
        frlist = attachments(fr)
        fra = {a['title']: a.get('fileId') for a in frlist}
        frsize = {a['title']: a.get('fileSize') for a in frlist}
        n_up = 0
        def fix_media(n):
            global n_up
            if n.get('type') == 'media' and n.get('attrs', {}).get('collection') == 'contentId-%s' % en:
                a = ena.get(n['attrs']['id'])
                if a:
                    # French figure override: fr/figs/<en page id>/<attachment title> (captured with the French UI)
                    local = lp('figs', en, a['title'])
                    if os.path.exists(local):
                        lsize = os.path.getsize(local)
                        if a['title'] not in fra or frsize.get(a['title']) != lsize:
                            fra[a['title']] = upload(fr, a['title'], open(local, 'rb').read(), mimetypes.guess_type(local)[0] or 'image/png'); n_up += 1
                        n_fr_fig.add(a['title'])
                    elif a['title'] not in fra or frsize.get(a['title']) != a.get('fileSize'):
                        data = req('GET', B + a['downloadLink'] if not a['downloadLink'].startswith('http') else a['downloadLink'], raw=True)
                        fra[a['title']] = upload(fr, a['title'], data, a.get('mediaType') or 'application/octet-stream'); n_up += 1
                    n['attrs']['id'] = fra[a['title']]; n['attrs']['collection'] = 'contentId-%s' % fr
            for m in n.get('marks', []) or []:
                if m['type'] == 'link': m['attrs']['href'] = remap_url(m['attrs'].get('href'))
            if n.get('type') == 'inlineCard' and n.get('attrs', {}).get('url'): n['attrs']['url'] = remap_url(n['attrs']['url'])
            for c in n.get('content', []) or []: fix_media(c)
        n_up = 0; n_fr_fig = set()
        fix_media(adf)
        adf['content'] = [notice(p, p['enVersion'])] + adf['content']
        cur = get('/api/v2/pages/%s' % fr)
        sfx = L['titleSuffix']
        title = cur['title'] if cur['title'].endswith(sfx) and cur['title'][:-len(sfx)] == p['title'] else p['title']
        if title != cur['title']:
            q = '/rest/api/content?' + urllib.parse.urlencode({'spaceKey': 'OG', 'title': title})
            hits = [h for h in get(q)['results'] if h['id'] != fr]
            if hits: title = title + sfx
        req('PUT', '/api/v2/pages/%s' % fr, {'id': fr, 'status': 'current', 'title': title,
            'body': {'representation': 'atlas_doc_format', 'value': json.dumps(adf, ensure_ascii=False)},
            'version': {'number': cur['version']['number'] + 1, 'message': L['versionMsg'].format(v=p['enVersion'], en=en)}})
        want = parent_id(p)
        if cur.get('parentId') != want:
            try: req('PUT', '/rest/api/content/%s/move/append/%s' % (fr, want))
            except RuntimeError as e: log('WARN move', fr, e)
        set_prop(fr, 'adapps-lango-lang', lango_value(LANG_CODE, en, 'current'))
        try: get('/rest/api/content/%s/property/adapps-lango-lang' % en)
        except RuntimeError: set_prop(en, 'adapps-lango-lang', lango_value('en', en, 'primary'))
        set_prop(fr, 'openelis-translation', {'sourceId': en, 'sourceVersion': p['enVersion'], 'sourceTitle': p['enTitle'], 'lang': LANG_CODE,
                                              'translatedAt': TODAY, 'method': 'claude', 'glossary': L['glossary'], 'scope': p['scope'],
                                              'frenchFigures': sorted(n_fr_fig), 'figuresCapturedAt': TODAY if n_fr_fig else None})
        try: req('POST', '/rest/api/content/%s/label' % fr, [{'prefix': 'global', 'name': L['label']}])
        except RuntimeError as e: log('WARN label', e)
        state['done'][en] = p['enVersion']; save()
        log('content', en, '->', fr, 'figures uploaded', n_up, 'french figures', len(n_fr_fig), title[:50])

if 'trash' in phases:
    for pid in plan['trash']:
        try: req('DELETE', '/api/v2/pages/%s' % pid); log('trashed', pid)
        except RuntimeError as e: log('WARN trash', pid, e)
log('DONE', ' '.join(phases))
save()
