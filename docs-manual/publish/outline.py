import re, sys
s = open(sys.argv[1]).read()
t = re.sub(r'<h([1-6])[^>]*>', r'\n#H\1 ', s)
t = re.sub(r'<li[^>]*>', r'\n - ', t)
t = re.sub(r'<p[^>]*>', r'\n', t)
t = re.sub(r'<ri:page ri:content-title="([^"]*)"[^>]*/>', r'[T:\1]', t)
t = re.sub(r'href="[^"]*pages/(\d+)[^"]*"', r'>[ID:\1]<', t)
t = re.sub(r'<ac:structured-macro ac:name="([^"]+)"', r'\n[MACRO:\1]<', t)
t = re.sub(r'<[^>]+>', '', t)
out = re.sub(r'\n\s*\n', '\n', t)
a = int(sys.argv[2]) if len(sys.argv) > 2 else 0
b = int(sys.argv[3]) if len(sys.argv) > 3 else 8000
print(len(s), len(out)); print(out[a:b])
