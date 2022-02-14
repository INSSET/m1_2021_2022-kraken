import click
import os
import ovh
import json
import gestprojlib as gp

PATH = os.environ['CONF_OVH_PATH']
CONF_FILE = os.environ['CONF_OVH_FILE']

client = ovh.Client(config_file=PATH+'/'+CONF_FILE)


@click.group()
def cli():
    pass


@cli.command()
@click.argument("domaine")
def liste(domaine):
    result = client.get('/domain/zone/'+domaine+'/record',
                    fieldType='CNAME'
                    )
    for val in result:
        liste_alias = client.get('/domain/zone/'+domaine+'/record/' + str(val))
        # print(json.dumps(liste_alias, indent=4))
        if liste_alias['target'] == domaine+'.':
            print(liste_alias['subDomain'])


@cli.command()
@click.argument("name")
@click.argument("domaine")
def add(name, domaine):
    result = client.post('/domain/zone/'+domaine+'/record',
                         fieldType='CNAME',
                         subDomain=name,
                         target=domaine+'.',
                         ttl=None,
                         )
    click.echo(json.dumps(result, indent=4))
    result = client.post('/domain/zone/'+domaine+'/refresh')
    click.echo(json.dumps(result, indent=4))


@cli.command()
@click.argument("input_file", type=click.Path(exists=True), nargs=1)
@click.argument("domaine")
def add(input_file, domaine):
    info_etudiants = gp.init_liste_etudiant_txt(input_file)
    for etudiant in info_etudiants:
        result = client.post('/domain/zone/'+domaine+'/record',
                             fieldType='CNAME',
                             subDomain=etudiant['domain'],
                             target=domaine+'.',
                             ttl=None,
                             )
        click.echo(json.dumps(result, indent=4))
    result = client.post('/domain/zone/'+domaine+'/refresh')
    click.echo(json.dumps(result, indent=4))


@cli.command()
def zone():
    domains = client.get('/domain/zone')
    for domain in domains:
        click.echo(domain)


@cli.command()
@click.argument("sous_domaine")
@click.argument("domaine")
def info(sous_domaine, domaine):
    result = get_id_sub(sous_domaine, domaine)
    click.echo(json.dumps(result, indent=4))


@cli.command()
@click.argument("sous_domaine")
@click.argument("domaine")
def delete(sous_domaine, domaine):
    result = get_id_sub(sous_domaine, domaine)
    for id_sub in result:
        client.delete('/domain/zone/' + domaine + '/record/' + str(id_sub))
        click.echo(sous_domaine+"( "+str(id_sub)+" ) suprimé")
    client.post('/domain/zone/'+domaine+'/refresh')


@cli.command()
@click.argument("input_file", type=click.Path(exists=True), nargs=1)
@click.argument("domaine")
def delete(input_file, domaine):
    info_etudiants = gp.init_liste_etudiant_txt(input_file)
    for etudiant in info_etudiants:
        result = get_id_sub(etudiant['domain'], domaine)
        for id_sub in result:
            client.delete('/domain/zone/' + domaine + '/record/' + str(id_sub))
            click.echo(etudiant['domain']+"( "+str(id_sub)+" ) suprimé")
    client.post('/domain/zone/'+domaine+'/refresh')


def get_id_sub(sub, dom):
    result = client.get('/domain/zone/' + dom + '/record',
                        fieldType='CNAME',
                        subDomain=sub,
                        )
    return result


if __name__ == '__main__':
    cli()