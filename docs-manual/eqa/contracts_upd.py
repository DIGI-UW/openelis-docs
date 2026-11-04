import json,shutil,os,datetime
os.chdir(os.path.expanduser('~/Documents/OpenELIS QA/docs-manual'))
shutil.copy('contracts.json','contracts.json.bak-20260923-pre-eqa')
d=json.load(open('contracts.json')); S=d['sections']
B='https://pngtest.openelis-global.org'
common=dict(base=B,capturedVersion='3.2.2.0',capturedDate='2026-09-23',jiraEpic='OGC-608',featureDoc='OGC-1235',frs='pending',captureSpec='pending',uiPaths=['frontend/src/components/eqa'])
prov=dict(id='eqa-provider',title='EQA provider: run a proficiency testing scheme',confluencePageId='1669562408',manualDoc='Confluence 1669562408 (draft under 1189609473)',captures='cowork session eqa-capture/provider (37 figures)',**common,
 routes=[
  {'path':'/qa/eqa/management','anchors':['Scheme Administration','EQA Schemes','System Settings','Add Scheme','Scheme Name','Scheme type','Enrolled Participants']},
  {'path':'/qa/eqa/participants','anchors':['Participants','Select Program']},
  {'path':'/qa/eqa/provider/schemes','anchors':['EQA schemes we provide','Active schemes','Open cycles','Enrolled participants','Follow-ups open','New cycle','Performance']},
  {'path':'/qa/eqa/provider/cycles/1/workbench','anchors':['Cycle history','Prep','Shipments','Receipts & scoring','Report comments']},
  {'path':'/qa/eqa/provider/follow-ups','anchors':['Participant follow-up','Participant','Cycle','Status','Notified','Response']},
  {'path':'/qa/eqa/provider/schemes/8/performance','anchors':['Participant performance','Laboratory','Pass rate (last 4)','Most recent','Open follow-ups']}],
 notes='Verified on pngtest (EQA V2 deployed there; not on testing at capture). Seed data: scheme 8 CPHL National CD4 Count EQA, cycle 1 2026 Round 4 (closed), orgs 28-33. Locale en only: en-US and other locales still carry V1 Program wording. Hard-loaded /qa/eqa deep links intermittently render blank (defect 9), which can false-positive this check.')
part=dict(id='eqa-participant',title='EQA participant: take part in a proficiency testing scheme',confluencePageId='1671987213',manualDoc='Confluence 1671987213 (draft under 1189609473)',captures='cowork session eqa-capture/participant (21 figures)',**common,
 routes=[
  {'path':'/qa/eqa/my-programs','anchors':['My EQA Schemes','Enroll in Scheme','Scheme Name','Provider','Lab Unit(s)','Test panels']},
  {'path':'/qa/eqa/my-cycles','anchors':['My EQA Cycles','New cycle','Active cycles','Ready to submit','Awaiting scores','Open EQA-linked NCE']},
  {'path':'/qa/eqa/lab-performance/coverage','anchors':['Coverage','Recent Cycles','Acceptance rate (12 mo)','On-time submission rate','Accredited tests without EQA']},
  {'path':'/qa/eqa/follow-up-queue','anchors':["This Lab's Follow-Up",'Auto-NCE policy active.','Items queued','In-house failures']},
  {'path':'/qa/eqa/analyst-competency','anchors':['Analyst Competency','Analysts assessed','Competent','Under review','Not competent']}],
 notes='Verified on pngtest. Seed: scheme 9 Asia-Pacific CD4 Proficiency Programme (International PT, external provider), cycle 2 2026 Round 3 (APC-26-3), scored; org 34 APCPP as referring site. Add Order EQA mode route /SamplePatientEntry?isEQA=true&cycleId=2 not registered (needs a Planned cycle to be meaningful).')
S=[s for s in S if s['id'] not in ('eqa-provider','eqa-participant')]
for s in S:
    if s['id']=='eqa':
        s['retired']=True
        s['notes']=('RETIRED 2026-09-23: EQA V1 routes. Superseded by eqa-provider and eqa-participant (EQA V2, OGC-608). '+s.get('notes','')).strip()
S+= [prov,part]
d['sections']=S
json.dump(d,open('contracts.json','w'),indent=2,ensure_ascii=False)
print(len(S),[s['id'] for s in S if s['id'].startswith('eqa')])
# drift spec: skip retired
p='../tests/docs/drift.check.spec.ts'; t=open(p).read()
old='sections.filter((s: any) => host(s.base) === host(BASE))'
if old in t and '!s.retired' not in t:
    shutil.copy(p,p+'.bak-20260923')
    t=t.replace(old,'sections.filter((s: any) => !s.retired && host(s.base) === host(BASE))'); open(p,'w').write(t); print('spec patched')
