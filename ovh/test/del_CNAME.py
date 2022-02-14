import ovh
import json
import os

PATH = os.environ['CONF_OVH_PATH']
CONF_FILE = os.environ['CONF_OVH_FILE']

client = ovh.Client(config_file=PATH+'/'+CONF_FILE)

result = client.delete('/domain/zone/insset.ovh/record/5141695871')

# Pretty print
print(json.dumps(result, indent=4))