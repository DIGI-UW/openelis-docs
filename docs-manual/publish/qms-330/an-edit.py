import importlib.util
s=importlib.util.spec_from_file_location('pub','confluence-publish.py');p=importlib.util.module_from_spec(s);s.loader.exec_module(p)
b,a=p.load_creds(); pid='1648590851'
r=p.api(b,a,'GET','/rest/api/content/'+pid+'?expand=body.storage,version')
v=r['body']['storage']['value']
reps=[
('Captured from <code>analyzers.openelis-global.org</code> on 15 September 2026.</p></blockquote>',
 'Captured from <code>analyzers.openelis-global.org</code> on 15 September 2026. The held-result status and the Analyser import issues page were noted on <code>testing.openelis-global.org</code> (3.3.0-SNAPSHOT) on 12 October 2026.</p></blockquote>'),
('Until then, expect the attention count to stay above zero on any analyzer that ran before its mappings were complete.</p>',
 'Until then, expect the attention count to stay above zero on any analyzer that ran before its mappings were complete.</p><p><strong>Status on 12 October 2026:</strong> OGC-1220 is in Acceptance on <code>testing.openelis-global.org</code> (3.3.0-SNAPSHOT). It could not be re-checked there, because no analyzer on that server was active or had held results.</p>'),
('<hr /><h1>Part 3',
 '<h2>Undelivered analyzer results (3.3.0)</h2><p>In 3.3.0 the Analysers list shows whether OpenELIS is paired with the Analyzer Bridge, and a banner when the Bridge is holding results it could not deliver, for example <em>32 analyzer results were not delivered</em>. <strong>Review undelivered results</strong> opens <strong>Analyser import issues</strong>.</p><p>That page has two parts. The first lists microbiology analyser events that could not be matched or processed; held results are still reviewed in each analyser\'s own results worklist. The second, <strong>Undelivered analyzer results</strong>, lists results the Bridge received but has not delivered, with the analyser (or <em>Unrecognized sender</em> and its address), when it was received, its status, the reason and details, for example <em>The sender matches no saved analyzer connection. Set up the analyzer, then retry.</em> <strong>Retry</strong> sends a result again once its cause is fixed; <strong>Dismiss</strong> hides it and keeps it in the Bridge for audit.</p><p><em>Observed on testing on 12 October 2026, where every undelivered result came from a sender with no saved connection. Retry and Dismiss were not exercised.</em></p><hr /><h1>Part 3'),
]
for o,n in reps:
    c=v.count(o); print(c, o[:50]); assert c==1
    v=v.replace(o,n)
p.api(b,a,'PUT','/rest/api/content/'+pid,{'id':pid,'type':'page','title':r['title'],'version':{'number':r['version']['number']+1,'message':'3.3.0: OGC-1220 status, Undelivered analyzer results (observed)'},'body':{'storage':{'value':v,'representation':'storage'}}})
print('ok', r['version']['number']+1)
