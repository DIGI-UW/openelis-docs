import importlib.util, json, os, re
HERE=os.path.dirname(os.path.abspath(__file__))
spec=importlib.util.spec_from_file_location('pub',os.path.join(os.path.dirname(HERE),'confluence-publish.py')); pub=importlib.util.module_from_spec(spec); spec.loader.exec_module(pub)
b,a=pub.load_creds()
ids=json.load(open(os.path.join(HERE,'ids.json')))
for k,v in ids.items():
    if k=='Inventory': continue
    p=pub.api(b,a,'GET',f'/api/v2/pages/{v}?body-format=storage')
    body=p['body']['storage']['value']
    labels=[l['name'] for l in pub.api(b,a,'GET',f'/rest/api/content/{v}/label').get('results',[])]
    att=pub.api(b,a,'GET',f'/rest/api/content/{v}/child/attachment?limit=100').get('size')
    print(k,v,p['title'],'v',p['version']['number'],'parent',p.get('parentId'),'len',len(body),'imgs',body.count('<ac:image'),'att',att,'tokens',body.count('{{IMG'),'PH',len(re.findall('PAGE_URL|RECEIVE_PAGE',body)),'emdash',body.count('—'),labels)
