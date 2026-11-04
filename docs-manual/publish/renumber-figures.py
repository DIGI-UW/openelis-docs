import re, sys
src, out = sys.argv[1], sys.argv[2]
s = open(src).read()
# collect caption locations in order: ac:caption blocks and <em>Figure N. ...</em> paragraphs
items = []
for m in re.finditer(r'<ac:caption[^>]*>(.*?)</ac:caption>', s, re.S):
    items.append((m.start(1), m.end(1), 'cap'))
for m in re.finditer(r'<em>Figure (\d+)\. ', s):
    items.append((m.start(), m.end(), 'em', int(m.group(1))))
items.sort()
oldmap = {}
n = 0
plan = []
for it in items:
    n += 1
    if it[2] == 'em':
        oldmap[it[3]] = n
    plan.append((it, n))
# apply from end
for it, num in reversed(plan):
    a, b = it[0], it[1]
    if it[2] == 'em':
        s = s[:a] + '<em>Figure %d. ' % num + s[b:]
    else:
        inner = s[a:b]
        if re.search(r'Figure \d+\.', inner):
            continue
        inner2 = re.sub(r'^(\s*<p[^>]*>\s*(?:<em>)?)', lambda m: m.group(1) + 'Figure %d. ' % num, inner, count=1)
        if inner2 == inner:
            inner2 = 'Figure %d. ' % num + inner
        s = s[:a] + inner2 + s[b:]
# fix cross-references "in Figure N" outside captions (old em numbers)
def xref(m):
    k = int(m.group(2))
    return m.group(1) + 'Figure %d' % oldmap.get(k, k)
s = re.sub(r'((?:in|see|from|to) )Figure (\d+)(?!\.)', xref, s)
open(out, 'w').write(s)
print('captions', n, 'oldmap', oldmap)
