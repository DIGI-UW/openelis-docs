"""ADF <-> translatable segments.

extract(adf) -> (skeleton, segments)
  segments: list of {"id": "s12", "kind": "p|alt|title|attr", "text": markup}
  Inline runs are serialised to a small markup:
    <b>..</b> strong, <i>..</i> em, <u>..</u> underline, <s>..</s> strike,
    <code>..</code> code (content must stay verbatim), <a n="3">..</a> link,
    <m n="4">..</m> any other mark set (textColor etc.), <x n="5"/> non-text inline node,
    <br/> hard break. &, <, > are escaped as &amp; &lt; &gt;.
rebuild(skeleton, translations) -> adf
"""
import json, copy, re, html

INLINE = {'text', 'hardBreak', 'emoji', 'inlineCard', 'date', 'mention', 'status', 'placeholder', 'inlineExtension', 'mediaInline'}
SIMPLE = {'strong': 'b', 'em': 'i', 'underline': 'u', 'strike': 's', 'code': 'code'}
TAG2MARK = {v: k for k, v in SIMPLE.items()}


def _esc(t):
    return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def serialise(nodes, store):
    """nodes: inline node list. store: list collecting opaque objects (links, other marks, inline nodes)."""
    out = []
    for n in nodes:
        t = n.get('type')
        if t == 'text':
            s = _esc(n['text'])
            marks = n.get('marks', [])
            simple = [m for m in marks if m['type'] in SIMPLE]
            other = [m for m in marks if m['type'] not in SIMPLE and m['type'] != 'link']
            link = [m for m in marks if m['type'] == 'link']
            # innermost first: code/b/i..., then other, then link outermost
            for m in sorted(simple, key=lambda m: list(SIMPLE).index(m['type']), reverse=True):
                tg = SIMPLE[m['type']]
                s = '<%s>%s</%s>' % (tg, s, tg)
            if other:
                store.append({'marks': other}); s = '<m n="%d">%s</m>' % (len(store) - 1, s)
            if link:
                store.append({'marks': link}); s = '<a n="%d">%s</a>' % (len(store) - 1, s)
            out.append(s)
        elif t == 'hardBreak':
            out.append('<br/>')
        else:
            store.append({'node': n}); out.append('<x n="%d"/>' % (len(store) - 1))
    s = ''.join(out)
    # merge adjacent identical simple tags: </b><b>
    for tg in ['b', 'i', 'u', 's', 'code']:
        s = s.replace('</%s><%s>' % (tg, tg), '')
    return s


TOK = re.compile(r'<(/?)(b|i|u|s|code|a|m)(?: n="(\d+)")?>|<x n="(\d+)"/>|<br/>|[^<]+|<', re.S)


def parse(markup, store):
    nodes = []
    stack = []  # list of mark dicts
    for mt in TOK.finditer(markup):
        tok = mt.group(0)
        if mt.group(2):
            closing, tg, n = mt.group(1), mt.group(2), mt.group(3)
            if not closing:
                if tg in TAG2MARK:
                    stack.append([{'type': TAG2MARK[tg]}])
                else:
                    stack.append(copy.deepcopy(store[int(n)]['marks']))
            else:
                if stack: stack.pop()
                else: raise ValueError('unbalanced close in: ' + markup[:200])
        elif mt.group(4):
            nodes.append(copy.deepcopy(store[int(mt.group(4))]['node']))
        elif tok == '<br/>':
            nodes.append({'type': 'hardBreak'})
        else:
            txt = html.unescape(tok) if tok != '<' else '<'
            if not txt: continue
            marks = [m for ms in stack for m in ms]
            # dedupe by type, ADF requires unique mark types
            seen = set(); mk = []
            for m in marks:
                if m['type'] in seen: continue
                seen.add(m['type']); mk.append(m)
            # code mark cannot combine with most marks except link
            if any(m['type'] == 'code' for m in mk):
                mk = [m for m in mk if m['type'] in ('code', 'link')]
            node = {'type': 'text', 'text': txt}
            if mk: node['marks'] = mk
            if nodes and nodes[-1].get('type') == 'text' and nodes[-1].get('marks') == node.get('marks'):
                nodes[-1]['text'] += txt
            else:
                nodes.append(node)
    if stack: raise ValueError('unclosed tag in: ' + markup[:200])
    return nodes


def is_text_block(n):
    c = n.get('content')
    return bool(c) and n.get('type') not in ('codeBlock',) and all(x.get('type') in INLINE for x in c)


def extract(adf):
    sk = copy.deepcopy(adf)
    segs = []
    stores = {}

    def add(kind, text, store=None):
        sid = 's%d' % len(segs)
        segs.append({'id': sid, 'kind': kind, 'text': text})
        if store is not None: stores[sid] = store
        return sid

    def walk(n):
        t = n.get('type')
        if t == 'codeBlock':
            return
        if t == 'media' and n.get('attrs', {}).get('alt'):
            n['attrs']['alt'] = {'$seg': add('alt', _esc(n['attrs']['alt']))}
        if t == 'expand' and n.get('attrs', {}).get('title'):
            n['attrs']['title'] = {'$seg': add('attr', _esc(n['attrs']['title']))}
        if t in ('extension', 'bodiedExtension') :
            return
        if is_text_block(n):
            store = []
            m = serialise(n['content'], store)
            if re.sub(r'<[^>]+>', '', m).strip() and re.search(r'[A-Za-z]', re.sub(r'<code>.*?</code>', '', m)):
                n['content'] = {'$seg': add('p', m, store), '$store': store}
            return
        for c in n.get('content', []) or []:
            walk(c)

    walk(sk)
    return sk, segs


def rebuild(sk, tr, segs_by_id=None):
    adf = copy.deepcopy(sk)
    missing = []

    def get(sid):
        if sid in tr: return tr[sid]
        missing.append(sid)
        return segs_by_id[sid]['text'] if segs_by_id else ''

    def walk(n):
        a = n.get('attrs') or {}
        for k in ('alt', 'title'):
            if isinstance(a.get(k), dict) and '$seg' in a[k]:
                a[k] = html.unescape(re.sub(r'<[^>]+>', '', get(a[k]['$seg'])))
        c = n.get('content')
        if isinstance(c, dict) and '$seg' in c:
            n['content'] = parse(get(c['$seg']), c['$store'])
            return
        for x in c or []:
            walk(x)

    walk(adf)
    return adf, missing


def tags(m):
    """Signature used to validate a translation keeps the same structure."""
    t = re.findall(r'<(/?)(b|i|u|s|code|a|m)(?: n="(\d+)")?>|<x n="(\d+)"/>|(<br/>)', m)
    a = sorted([x[2] for x in t if x[1] in ('a', 'm') and not x[0]] + [x[3] for x in t if x[3]])
    codes = re.findall(r'<code>(.*?)</code>', m, re.S)
    return a, sorted(codes)


def check(src, dst):
    sa, sc = tags(src); da, dc = tags(dst)
    errs = []
    if sa != da: errs.append('placeholders differ %s vs %s' % (sa, da))
    if sc != dc: errs.append('code spans changed')
    try:
        parse(dst, [{'marks': [], 'node': {'type': 'text', 'text': 'x'}}] * 999)
    except Exception as e:
        errs.append('parse: %s' % e)
    return errs
