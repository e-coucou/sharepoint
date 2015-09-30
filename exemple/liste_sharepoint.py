# -*- coding: utf-8 -*-
""" e-coucou 2015 """
import requests, lxml, json, urllib, sys, argparse, getpass, time
from lxml import html,etree
from requests_ntlm import HttpNtlmAuth

DEBUG = 0
OUTSIDE = 0
level = 0
g_cnt = 0
g_file = 0
g_size = 0
#----------------
def aff(str,val):
    print '-  >>',str,val
    return
def reponse(rep,code):
	print '#',code,'########################################################'
	print 'cde : ----'
	print rep.request.url
	for hh in rep.request.headers:
		print hh,'=',rep.request.headers[hh]
	print 'rep : ----'
	print rep.history
	if rep.history:
		for rp in rep.history:
			print rp.status_code, rp.url
			print '/'
			print rp.cookies
			print rp.content
	print '[',rep.status_code,']'
	print '  -- headers  --'
	for hh in rep.headers:
		print hh,'=',rep.headers[hh]
	print '  -- cookies  --'
	for cc in rep.cookies:
		print cc,'='
	print '  - -url  --'
	print rep.url
	return

def decode_folder(session,source,level,folder):
    global g_cnt
    try:
        xml = lxml.etree.fromstring(source)
    except:
        sys.stdout('#')
        sys.stdout.flush()
        print source  
    nsmap = {'atom': 'http://www.w3.org/2005/Atom','d': 'http://schemas.microsoft.com/ado/2007/08/dataservices','m': 'http://schemas.microsoft.com/ado/2007/08/dataservices/metadata'}
    cnt=0
    for m in xml.xpath("//atom:entry/atom:content/m:properties", namespaces=nsmap):
		cnt = cnt + 1
		g_cnt = g_cnt + 1
		N = m.find('d:Name', namespaces=nsmap)
		L = m.find('d:ServerRelativeUrl', namespaces=nsmap)
		I = m.find('d:ItemCount', namespaces=nsmap)
		U = m.find('d:UniqueId', namespaces=nsmap)
		rep = urllib.quote(L.text.encode('windows-1252'))
		ligne = 'd;'+urllib.unquote(folder.encode("windows-1252"))+';"'+N.text.encode('windows-1252')+'";"'+args.site+rep+'";'+I.text+';'+U.text+';'+rep+'\n'
		fo.write(ligne)
		recurse_dir(session,rep,level)
    return
def read_files(session,folder,level):
    global g_file, g_size
    url = args.site + args.url +"_api/Web/GetFolderByServerRelativeUrl('"+folder+"')/files"
    requete = session.get(url, proxies=p, verify=True,allow_redirects=True, headers = h, cookies = c)
    xml = lxml.etree.fromstring(requete.content)
    nsmap = {'atom': 'http://www.w3.org/2005/Atom','d': 'http://schemas.microsoft.com/ado/2007/08/dataservices','m': 'http://schemas.microsoft.com/ado/2007/08/dataservices/metadata'}
    for m in xml.xpath("//atom:entry/atom:content/m:properties", namespaces=nsmap):
        g_file = g_file + 1
        N = m.find('d:Name', namespaces=nsmap)
        #        L = m.find('atom:id', namespaces=nsmap)
        L = m.find('d:ServerRelativeUrl', namespaces=nsmap)
        I = '1'
        U = m.find('d:UniqueId', namespaces=nsmap)
        rep = urllib.quote(L.text.encode('utf-8'))
        z = m.find('d:Length', namespaces=nsmap)
        ligne = 'f;'+urllib.unquote(folder)+';"'+N.text.encode('windows-1252')+'";"'+args.site+rep+'";'+I+';'+U.text+';'+rep+';'+z.text+'\n'
        try:
            g_size = g_size + int(z.text)
        except:
            sys.stdout.write('#')
        fo.write(ligne)
        sys.stdout.write('.')
        sys.stdout.flush()
    return
def recurse_dir(session,folder,level):
    sys.stdout.write('-')
    sys.stdout.flush()
    level = level + 1
    read_files(session,folder,level)
    url = args.site + args.url +"_api/Web/GetFolderByServerRelativeUrl('"+folder+"')/folders"

    try:
	    requete = session.get(url, proxies=p, verify=True,allow_redirects=True, headers = h, cookies = c)
    except:
        sys.stdout.write('#')
        sys.stdout.flush()
        print url
    decode_folder(session,requete.content,level,folder)
    level = level - 1
    return level
def get_folder(session,folder):
	global fo
	name= folder+'.csv'
	fo = open(name,'w')
	fo.write('type;repertoire;nom;lien;id;qte;rel_url;taille\n')
	print '-- lecture de repertoire / bibliotheque'
	bibli = args.url+folder
	level = recurse_dir(s,bibli,0)
	print
	print '- total de repertoires :',g_cnt
	print '- total de fichiers :',g_file
	print '- soit : ', g_cnt+g_file,'elements'
	fo.close()
	return
def get_token():
    global s, p, h, c
    print '--------------------------------------------------------------------------'
    print '- Start login ...'
    print '-'
    u = args.site + args.url+ urllib.quote(args.bibliotheque)
    if OUTSIDE :
        p= ''
        aff('NO PROXY : Outside mode enable.','')
    h = {'User-Agent' : 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.2.11) Gecko/20101012 Firefox/3.6.11'}
    h1 = { 'Connection' : 'keep-alive' , 'Upgrade-Insecure-Requests' : '1' , 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36' , 'Accept-Encoding' : 'gzip, deflate, sdch', 'Accept-Language' : 'fr-FR,fr;q=0.8,en-US;q=0.6,en;q=0.4'}
    h3 = { 'Accept' : 'application/json, text/javascript, */*; q=0.01', 'X-Requested-With' : 'XMLHttpRequest' }
        
    if VERBOSE : aff('First url to', args.site)
    try:
        r = s.get(u, proxies=p, verify = True,allow_redirects=True, headers= h1)
    except:
	    return 0
    if DEBUG : reponse(r,1)
    if r.status_code == 404 : return 2
    r2 = s.get(r.url, proxies=p, verify=True,allow_redirects=True, headers = h1 ) #, cookies = c)
    if DEBUG : reponse(r2,2)
    b = r2.content
    tree = lxml.html.fromstring(b)
    elements = tree.get_element_by_id('cred_hidden_inputs_container')
    ctx = elements[0].value
    flowtoken = elements[1].value
    l = "https://login.microsoftonline.com/common/userrealm/?user="+args.email+"&api-version=2.1&stsRequest="+ctx+"&checkForMicrosoftAccount=true"
    if VERBOSE :
        aff('Get info from redirect to login.microsoftonline.com.','')
        aff('CTX ->',ctx)
        aff('Flowtoken ->',flowtoken)
        aff('url : ',l)
        aff('Get STS url from microsoft online (json response)','')
    h1.update(h3)
    c = {}
    r3 = s.get(l, proxies=p, verify=True,allow_redirects=True , headers = h1 , cookies=c)
    if DEBUG : reponse(r3,3)
    #-- debug
    try:
        j = json.loads(r3.content)
        ad = j['AuthURL']+ "&popupui="
        if VERBOSE : aff('URL OK in json reply.','')
    except:
        aff('URL ERREUR:',ad)
    c = {}
    if OUTSIDE :
        if VERBOSE : aff('get SAML token','')
        r4 = s.get(ad, proxies=p, verify=True,allow_redirects=True, headers = h, cookies = c)
    else:
        if VERBOSE : aff('get NTLM token','')
        r4 = s.get(ad, proxies=p, verify=True,allow_redirects=True, auth = auth, headers = h, cookies = c)
    if DEBUG: reponse(r4,4)
    if OUTSIDE :
    # connexion à partir du username/password : le même que le proxy
    # on assume le fait que le Proxy et l'AD sont synchronisés et sont dans le même DOMAINE
        b = r4.content
        tree = lxml.html.fromstring(b)
        vs = tree.get_element_by_id("__VIEWSTATE").value #
        ev = tree.get_element_by_id("__EVENTVALIDATION").value #
        db = tree.xpath('//input/@value')[2]
        # Peut etre ajouter le nom de domaine au username
        data = '__VIEWSTATE='+urllib.quote(vs)+'&__EVENTVALIDATION='+urllib.quote(ev)+'&__db='+db+'&ctl00%24ContentPlaceHolder1%24UsernameTextBox='+urllib.quote(auth.username)+'&ctl00%24ContentPlaceHolder1%24PasswordTextBox='+urllib.quote(auth.password)+'&ctl00%24ContentPlaceHolder1%24SubmitButton=Connexion'
        h1.update({'Content-Type' : 'application/x-www-form-urlencoded'})
        if VERBOSE: aff('data : ', data)
        p1 = s.post(ad, data = data, allow_redirects=True, cookies=c, headers = h1)
    else:
        p1 = s.post(r4.url, allow_redirects=True, auth=auth, cookies=c, headers = h1) # no data car NTLM
        if VERBOSE : aff('POST Credentials to STS ','')
    if OUTSIDE :
        tree = lxml.html.fromstring(p1.content)
    else:
        tree = lxml.html.fromstring(r4.content)
    wa = tree.xpath('//input/@value')[0]
    wresult = tree.xpath('//input/@value')[1]
    wctx = tree.xpath('//input/@value')[2]
    data = 'wa='+wa+'&wresult='+urllib.quote(wresult)+'&wctx='+urllib.quote(wctx)
    if VERBOSE :
        aff('cookies : AUTH --------------->>>','')
        aff('MSIAuth:',p1.cookies['MSISAuth'])
        aff('Get SAML token to microsoft login.srf in order to get rtFa et FedAuth','')
    mic="https://login.microsoftonline.com/login.srf"
    if VERBOSE : print mic
    p2 = s.post(mic, data = data, auth=auth, allow_redirects=True, headers = h1, cookies=c)
    tree = lxml.html.fromstring(p2.content)
    t = tree.xpath('//input/@value')[0]
    data = 't='+urllib.quote(t)
    if VERBOSE :
        aff('SAML Token from Microsoft Online',data)
    ad = args.site+'/_forms/default.aspx?apr=1&wa=wsignin1.0'
    p3 = s.post(ad, data = data, allow_redirects=True, headers = h1, cookies=c)
    if VERBOSE :
        aff('Get rtFa & FedAuth session token to identify next requests','')
        aff(p3.status_code, p3.history)
        aff('rtFa =',p3.cookies['rtFa'])
        aff('FedAuth =',p3.cookies['FedAuth'])
        aff('Successfull Authentication','')
        aff('-------------------------------------------------------------- <fin> -','')
    return 1
def get_args():
    global auth, p
    global args
    global DEBUG, OUTSIDE, VERBOSE
    parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser(description='Liste les bibliotheques SharePoint dans un fichier csv')
    parser.add_argument("bibliotheque",help="renseignez le nom de la bibliotheque")
    parser.add_argument("-p","--proxy",default='proxy.my-org.local:8080',help="si vous etes derriere un proxy =1")
    parser.add_argument("-e","--email",default='first.name@my-org.com',help="adresse mail")
    parser.add_argument("-s","--site",default='https://my-org.sharepoint.com',help="adresse sharepoint du serveur -> ex: https://my.sharepoint.com")
    parser.add_argument("-u","--url",default='/sites/team/',help="reference relative du site sharepoint : /sites/.../")
    parser.add_argument("-d","--debug",default=False,action="store_true", help="=1 en mode DEBUG" )
    parser.add_argument("-O","--Outside",default= False , action="store_true" ,help="=1 en mode Externe")
    parser.add_argument("-U","--username",default="eric",help="username")
    parser.add_argument("-D","--Domaine",default="MYORG",help="Domaine de l'Active Directory")
    parser.add_argument("-P","--Password",default="",help="password")
    parser.add_argument("-v","--verbose",default=False,action="store_true",help="toutes les infos ...")
    args = parser.parse_args()
    Password = args.Password
    if args.Password == "" :
        Password = getpass.getpass(prompt="Entrez votre mot de passe Windows")
    proxy = args.username+':'+Password+'@'+args.proxy
    p={'http': 'http://'+proxy , 'https':'https://'+proxy}
    auth = HttpNtlmAuth(args.Domaine+'\\'+args.username,Password)
    OUTSIDE = args.Outside
    DEBUG = args.debug
    VERBOSE = args.verbose
    if VERBOSE :
        #		print auth.username, auth.password
        print '--------------------------------------------------------------------------'
        aff('Arguments ...','')
        aff('Username      :',args.Domaine+'/'+args.username)
        aff('eMail         :',args.email)
        aff('Site https    :',args.site)
        aff('proxy : ',proxy)
        aff('Bibliotheques :',args.bibliotheque)
    return

if __name__ == "__main__":
    get_args()
    s = requests.Session()
    t0 = time.time()
    token = get_token()
    if token == 1 :
		t1 = time.time()
		get_folder(s,urllib.quote(args.bibliotheque))
		tf=time.time()
		print '- résolution authentication : {0:.2f} secondes'.format(t1-t0)
		print '- scanning Bibliotheque en {0:.2f} secondes'.format(tf-t1)
		print '- pour une taille de {0:.1f} Mo'.format(g_size/1000000.0)
		print '-\n- by e-coucou 2015'
    elif token == 2 :
    	print '404: file not found (bibliotheque, url)'
    elif token == 0 :
	    print 'Erreur: invalid request (proxy, site)'