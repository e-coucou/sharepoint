# sharepoint
Lister les fichiers dans un site SharePoint hébergé sur Microsoft Online


Ce petit script python permet de se connecter à Sharepoint Online, de s'authentifier à un serveur ADFS de Microsoft et au besoin de traverser un proxy d'entreprise.

Le résultat est un fichier format csv de la liste des répertoires/fichiers contenu dans la bibliothèque online.

La syntaxe :

usage: liste_sharepoint.py  [-h] [-p PROXY] [-e EMAIL] [-s SITE] [-u URL] [-d]
                            [-O] [-U USERNAME] [-D DOMAINE] [-P PASSWORD] [-v]
                            bibliotheque

positional arguments:
    bibliotheque          renseignez le nom de la bibliotheque

optional arguments:
    -h, --help                  show this help message and exit
    -p PROXY, --proxy PROXY     si vous etes derriere un proxy =1
    -e EMAIL, --email EMAIL     adresse mail
    -s SITE, --site SITE        adresse sharepoint du serveur -> ex: https://my.sharepoint.com
    -u URL, --url URL           reference relative du site sharepoint : /sites/.../
    -d, --debug                 true en mode DEBUG
    -O, --Outside               true en mode Externe (NO PROXY)
    -U USERNAME, --username     USERNAME username
    -D DOMAINE, --Domaine       DOMAINE Domaine de l'Active Directory
    -P PASSWORD, --Password     PASSWORD password
    -v, --verbose               toutes les infos ...

(c) e-coucou 2015