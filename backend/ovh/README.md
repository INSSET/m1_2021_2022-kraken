### Fichier de configuration pour accès API ovh
Dans le répertoire conf créer un fichier xxx.conf contenant vos clefs
optenues sur [create tocken](https://eu.api.ovh.com/createToken/)  
Puis initialiser les variables d'environnement avec le nom de votre fichier de conf
```CONF_OVH_FILE="xxx.conf"```

    [default]
    ; general configuration: default endpoint
    endpoint=ovh-eu
    
    [ovh-eu]
    ; configuration specific to 'ovh-eu' endpoint
    application_key=brxxxxxxxxxxx5B
    application_secret=dcxxxxxxxxxxxxxxxxxxxxxxxxNk
    consumer_key=6rxxxxxxxxxxxxxxxxxxxxxxxxxx1Kn

