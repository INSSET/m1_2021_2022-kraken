import ovh
import json
import os

PATH = os.environ['CONF_OVH_PATH']
CONF_FILE = os.environ['CONF_OVH_FILE']

client = ovh.Client(config_file=PATH+'/'+CONF_FILE)

result = client.get('/domain/zone/insset.ovh/record',
                    fieldType='CNAME'
                    )

for val in result:
    liste_alias = client.get('/domain/zone/insset.ovh/record/' + str(val))
    # print(json.dumps(liste_alias, indent=4))
    if liste_alias['target'] == 'insset.ovh.':
        print(liste_alias['subDomain'])
