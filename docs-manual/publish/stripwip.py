import re,sys
p=sys.argv[1]; s=open(p).read()
n=len(s)
s=re.sub(r'<ac:structured-macro ac:name="note"[^>]*>(?:(?!</ac:structured-macro>).)*?Work in progress\..*?</ac:structured-macro>','',s,count=1,flags=re.S)
open(p,'w').write(s); print('removed',n-len(s))
