import os, json, base64, urllib.request
env = dict(l.strip().split('=',1) for l in open(os.path.expanduser('~/.openelis/confluence.env')) if '=' in l)
env = {k:v.strip().strip('"').strip("'") for k,v in env.items()}
A = base64.b64encode((env['CONFLUENCE_EMAIL']+':'+env['CONFLUENCE_API_TOKEN']).encode()).decode()
B='https://uwdigi.atlassian.net/wiki'
def call(method,path,data=None):
    req=urllib.request.Request(B+path,data=None if data is None else json.dumps(data).encode(),method=method,
        headers={'Authorization':'Basic '+A,'Content-Type':'application/json','Accept':'application/json'})
    try:
        r=urllib.request.urlopen(req); t=r.read().decode(); return r.status,(json.loads(t) if t else {})
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:400]
U='https://uwdigi.atlassian.net/wiki/spaces/OG/pages/'
def t(x, marks=None):
    d={'type':'text','text':x}
    if marks: d['marks']=marks
    return d
def L(x, pid, folder=False): return t(x,[{'type':'link','attrs':{'href':('https://uwdigi.atlassian.net/wiki/spaces/OG/folder/' if folder else U)+pid}}])
S=[{'type':'strong'}]; EM=[{'type':'em'}]
def p(*c): return {'type':'paragraph','content':list(c)}
def h(n,x): return {'type':'heading','attrs':{'level':n},'content':[t(x)]}
def ul(items): return {'type':'bulletList','content':[{'type':'listItem','content':[p(*i)]} for i in items]}
EN=lambda: t(' (en anglais)',EM)
def fr(title,pid,desc): return [L(title,pid), t(' — '+desc)]
def en(title,pid,desc): return [L(title,pid), EN(), t(' — '+desc)]
doc={'type':'doc','version':1,'content':[
 h(1,'Manuel de l\'utilisateur'),
 p(t('Pour le personnel de laboratoire (techniciens, biologistes, pathologistes) et pour les administrateurs qui configurent OpenELIS Global au quotidien.')),
 h(2,'Comment lire ce manuel'),
 ul([[t('Les pages en français sont des traductions des pages anglaises vérifiées. Quand une page n\'est pas encore traduite, le lien mène à la version anglaise, signalée '),t('(en anglais)',EM),t('.')],
     [t('Les termes suivent ceux de l\'interface française d\'OpenELIS. Si une traduction ne correspond pas à ce que vous voyez à l\'écran, fiez-vous à l\'écran et signalez-le (voir '),t('Aide',S),t(' plus bas).')],
     [t('Vous utilisez une version antérieure d\'OpenELIS ? Les anciennes pages du manuel sont conservées dans '),L('Versions précédentes','1679458382',True),t('.')]]),
 h(2,'Utilisateurs du laboratoire'),
 h(3,'Résultats et rapports'),
 ul([en('Enter and save results','1439072277','saisir les résultats depuis la liste de travail.'),
     en('Validate and release results','1441202177','vérifier les résultats saisis et les publier.'),
     en('Run reports','1440841744','produire les rapports.'),
     en('Find an existing order','1440350210','retrouver une demande.'),
     en('Track sample storage and disposal','1440677908','suivre le stockage et l\'élimination des échantillons.'),
     en('Create aliquots from a sample','1440940035','créer des aliquotes.')]),
 h(3,'Surveillance environnementale et vectorielle'),
 ul([en('The three domains & the shared order wizard','1428881409','les domaines clinique, environnemental et vectoriel et l\'assistant de saisie commun.'),
     fr('Surveillance environnementale — aperçu du processus','1643085838','de la demande par site de prélèvement au certificat de conformité.'),
     fr('Saisir une demande environnementale','1642299440','enregistrer une demande liée à un site de prélèvement.'),
     fr('Générer un certificat de conformité','1641840681','produire le certificat pour un échantillon évalué.'),
     fr('Surveillance des vecteurs — aperçu du processus','1641775218','de la demande de piégeage à l\'identification des espèces.'),
     fr('Saisir une commande de vecteur','1642233901','enregistrer une demande vectorielle.'),
     fr('Identifier les espèces vectrices et déconvoluer un échantillon composite','1641873444','identification et déconvolution des pools.'),
     fr('Enregistrer les indices de l\'enquête « Vector Field »','1642299535','saisir les indices de terrain.'),
     fr('Révision complète par l\'assurance qualité (phase partagée)','1641447513','la dernière étape avant la saisie des résultats.')]),
 h(2,'Administrateurs'),
 h(3,'Gestion du catalogue de tests'),
 ul([fr('Gestion du catalogue de tests — aperçu du flux de travail','1642922075','point de départ pour configurer les tests.'),
     fr('Rechercher et filtrer les tests dans le catalogue','1643380778','trouver un test.'),
     fr('Modifier les informations de base d\'un test (domaine, AMR, statut)','1643511817','nom, domaine, statut.'),
     fr('Configurer les types d\'échantillons et les composants des résultats d\'un test','1642659893','échantillons et résultats.'),
     fr('Définir les plages de référence et critiques','1643937795','valeurs normales et critiques.'),
     fr('Associer des méthodes à une analyse','1643806721','méthodes.'),
     fr('Configurer le stockage et l\'élimination des échantillons','1642987528','conservation.'),
     fr('Ajouter un test aux panneaux','1643380737','panels.'),
     fr('Définir l\'ordre d\'affichage des tests au sein d\'un type d\'échantillon','1643511855','ordre d\'affichage.'),
     fr('Mettre en correspondance une analyse avec des codes terminologiques','1643380801','codes LOINC et autres.'),
     fr('Gérer les modèles d’étiquettes','1643905025','étiquettes.'),
     fr('Liste de contrôle d\'acceptation de l\'échantillon','1643675652','critères d\'acceptation.')]),
 h(3,'Configuration du système'),
 ul([fr('Signatures électroniques','1642922003','exiger une signature pour certaines actions.'),
     en('Admin — Manage user accounts','1187840003','comptes et rôles.'),
     en('Admin — Configure site information','1439432709','informations du site.'),
     en('Admin — Choose the lab number format','1439170565','format du numéro de laboratoire.'),
     en('Admin — Manage dictionary entries','1438973976','listes de valeurs.'),
     en('Admin — Configure test notifications','1439072261','notifications par test.'),
     en('Admin — Manage non-working days','1439334404','jours non ouvrés.'),
     en('Admin — Manage providers','1439203334','prescripteurs.'),
     en('Admin — Manage organizations','1437892659','organisations.'),
     en('Admin — Edit application properties','1439367188','propriétés de l\'application.'),
     en('Admin — Configure logging','1438908431','journalisation.'),
     en('Admin — Configure result reporting to external systems','1439596548','envoi des résultats.'),
     en('Admin — Configure the navigation menu','1160282114','menu de navigation.'),
     en('Admin — Rebuild the search index','1438973960','index de recherche.'),
     en('Admin — Define reflex testing rules','1439137808','tests réflexes.'),
     en('Admin — Define calculated value tests','1438842886','valeurs calculées.'),
     en('Admin — Configure compliance standards & holding times','1427931149','normes de conformité.'),
     en('Admin — Vector Surveillance Reference Data','1427144728','données de référence vectorielles.')]),
 h(2,'Aide'),
 ul([[t('Dans votre laboratoire : votre administrateur OpenELIS.')],
     [t('Communauté : '),t('OpenELIS Talk',[{'type':'link','attrs':{'href':'https://talk.openelis-global.org'}}]),t('.')],
     [t('Une erreur de traduction ? Laissez un commentaire sur la page concernée.')]]),
 p(t('Version anglaise : ',EM),L('📖 User Manual','1326972929'))
]}
PID='1641447437'
s,pg=call('GET','/api/v2/pages/%s?body-format=atlas_doc_format'%PID)
assert s==200 and pg['id']==PID
json.dump(pg,open('/tmp/relrev/fr-landing-before-v%s.json'%pg['version']['number'],'w'))
body={'id':PID,'status':'current','title':pg['title'],'body':{'representation':'atlas_doc_format','value':json.dumps(doc,ensure_ascii=False)},
      'version':{'number':pg['version']['number']+1,'message':'Hand-built French landing: links French pages by ID, English where not yet translated, and Versions précédentes'}}
s,r=call('PUT','/api/v2/pages/%s'%PID,body); print('put',s,str(r)[:300] if s!=200 else r['version']['number'])
