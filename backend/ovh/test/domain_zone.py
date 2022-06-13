import ovh

client = ovh.Client(config_file='ovh.conf')

domains = client.get('/domain/zone')
for domain in domains:
    print(domain)

