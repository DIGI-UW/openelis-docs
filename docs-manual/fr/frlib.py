"""Shared Confluence REST helpers for the French translation pipeline (runs on Casey's Mac)."""
import os, json, base64, urllib.request, urllib.parse, time
env = dict(l.strip().split('=',1) for l in open(os.path.expanduser('~/.openelis/confluence.env')) if '=' in l)
env = {k:v.strip().strip('"').strip("'") for k,v in env.items()}
AUTH = base64.b64encode((env['CONFLUENCE_EMAIL']+':'+env['CONFLUENCE_API_TOKEN']).encode()).decode()
B = 'https://uwdigi.atlassian.net/wiki'
HERE = os.path.dirname(os.path.abspath(__file__))
def req(method, u, body=None, headers=None, raw=False):
    h = {'Authorization':'Basic '+AUTH,'Accept':'application/json'}
    if headers: h.update(headers)
    data = None
    if body is not None and not isinstance(body,(bytes,bytearray)):
        data = json.dumps(body).encode(); h.setdefault('Content-Type','application/json')
    elif body is not None: data = body
    r = urllib.request.Request(u if u.startswith('http') else B+u, data=data, method=method, headers=h)
    for i in range(4):
        try:
            with urllib.request.urlopen(r) as resp:
                b = resp.read()
                return b if raw else (json.loads(b) if b else {})
        except urllib.error.HTTPError as e:
            if e.code in (429,500,502,503) and i < 3: time.sleep(2*(i+1)); continue
            raise RuntimeError('%s %s -> %s %s' % (method, u, e.code, e.read()[:500].decode('utf8','replace')))
get = lambda u: req('GET', u)
def page(pid, fmt='atlas_doc_format'):
    return get('/api/v2/pages/%s?body-format=%s' % (pid, fmt))
def lango(pid):
    try: return get('/rest/api/content/%s/property/adapps-lango-lang' % pid)
    except RuntimeError as e:
        if '-> 404' in str(e): return None
        raise
def cql(q, expand='version,ancestors'):
    out=[]; u='/rest/api/content/search?'+urllib.parse.urlencode({'cql':q,'limit':100,'expand':expand})
    while u:
        d=get(u); out+=d['results']; u=d['_links'].get('next')
    return out

# ---- language config (fr, id, es). Pick with OE_LANG=<code> (default fr). Not LANG: that is the system locale.
LANG_CODE = os.environ.get('OE_LANG', 'fr')
L = json.load(open(os.path.join(HERE, 'langs.json')))[LANG_CODE]
TW = L['twinKey']           # key of the English->translation map in the state file ('fr' for French, 'tr' otherwise)
def lp(key, *more):
    """Per-language path in fr/ for a langs.json key (state, build, scope, baseline, treePlan, figs)."""
    return os.path.join(HERE, L[key], *more)
