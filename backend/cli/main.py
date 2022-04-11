import sys
sys.path.append("/usr/src/app/gplib")

import gestprojlib as gp

import getopt
import sys
import os
import grp
import gestprojmail
import click

DOMAIN = 'insset.ovh'
GROUP = "l2-2020"
LISTE = "../data/" + GROUP + "/test.csv"
IP_CLASS = "10.5"  # pour le group l3


# IP_CLASS = " 172.18" # pour le group_name lp


@click.group()
def start():
    pass

@click.group()
def create():
    pass

@click.group()
def delete():
    pass

@click.group()
def add():
    pass

@click.group()
def run():
    pass


###------------------------------------ CREATE COMMANDS -----------------------------------------###

@click.command(name='acces')
@click.argument('group')
@click.argument('liste_etudiant_input')
@click.option('--sftp', is_flag=True, help='add this option to create sftp users')
@click.option('--vhost', is_flag=True, help='add this option to create vhosts')
@click.option('--skel')
@click.option('--compose')
def create_acces(group, liste_etudiant_input, sftp, vhost, skel, compose):

    """Cree un groupe a partir d'une liste d'etudiants

    group: nom du groupe
    liste_etudiant_input : fichier csv ou liste d'adresses mails

    """
    cli_opts = {'sftp' : sftp, 'vhost' : vhost, 'skel' : skel, 'compose' : compose}
    try:
        info_grp = grp.getgrnam(group)
        click.echo("Le Groupe %s existe deja %d " % (info_grp.gr_name, info_grp.gr_gid))
        sys.exit()
    except KeyError:
        click.echo("Creation du group_name %s " % group)

    liste = gp.init_liste(liste_etudiant_input)
    gp.create_group(group)

    build_compte(cli_opts, group, liste)

@click.command(name='vhost')
@click.argument('group')
def create_vhost(group):
    """Cree des virtual hosts pour les membres du groupe
    
    group: nom du groupe
    """
    try:
        grp.getgrnam(group)
        liste = gp.liste_etudiant_group(group)
        gp.create_vhost(liste)
    except KeyError:
        print("Le group_name n'existe pas ou l'argument -g n'est pas renseigne ")
    return

@click.command(name='compose')
@click.argument('group')
@click.option('--compose')
def create_compose(group, compose):
    try:
        grp.getgrnam(group)
        liste = gp.liste_etudiant_group(group)
        if (compose):
            gp.create_compose(liste, IP_CLASS, protopath=('../conf/%s' % compose))
        else:
            gp.create_compose(liste, IP_CLASS)
    except KeyError:
        print("Le group_name n'existe pas")
    return

@click.command(name='container')
@click.argument('group')
def create_containers(group):
    """Cree des containers pour les membres du groupe
    
    group: nom du groupe
    """
    try:
        grp.getgrnam(group)  # juste pour tester l'existance du group_name
        grp_sftp = grp.getgrnam('sftp')
        liste = gp.liste_etudiant_group(group)
        for etud in liste:
            os.chdir(etud['user'].pw_dir)
            os.system('docker-compose up -d')
            os.system("docker exec %s groupadd -f -g %s sftp" % (etud['user'].pw_name, grp_sftp.gr_gid))
            os.system("docker exec %s useradd -d /opt/projet --shell /bin/bash -u %s -g sftp %s" % (
                etud['user'].pw_name, etud['user'].pw_uid, etud['user'].pw_name))
            os.system(
                'docker exec %s bash -c \'echo "%s:dev" | chpasswd\'' % (etud['user'].pw_name, etud['user'].pw_name))
            os.system("docker exec %s chown -R %s /opt/projet" % (etud['user'].pw_name, etud['user'].pw_name))
            os.system("rm /home/etudiants/%s/.ssh/known_hosts" % etud['user'].pw_name)
    except KeyError:
        print("Le group_name n'existe pas")
    return

@click.command(name='sftp')
@click.argument('group')
def create_sftp(group):
    """Cree des acces SFTP pour les membres du groupe
    
    group: nom du groupe
    """
    try:
        grp.getgrnam(group)
        liste = gp.liste_etudiant_group(group)
        gp.create_sftp_users(liste, group)
    except KeyError:
        print("Le group_name n'existe pas")
    return

@click.command(name='domain')
@click.argument('liste_etudiant_input')
def create_domain(liste_etudiant_input):
    """Cree des domaines pour les utilisateurs de la liste
    
    liste_etudiant_input : fichier csv ou liste d'adresses mails
    """
    try:

        liste = gp.init_liste(liste_etudiant_input)

        import ovh
        client = ovh.Client(config_file='ovh/ovh.conf')

        for etudiant in liste:
            un_domain = etudiant['login'].replace('.', '-')
            result = client.post('/domain/zone/' + DOMAIN + '/record',
                                 fieldType='CNAME',
                                 subDomain=un_domain,
                                 target=DOMAIN + '.',
                                 ttl=None,
                                 )
            print(result['subDomain'] + '=' + str(result['id']))
    except KeyError:
        print("Le group_name n'existe pas ou l'argument -g n'est pas renseigne ")

    return

@click.command(name='sql')
@click.argument('group')
def create_sql(group):
    """Cree un utilisateur SQL pour chaque membres du groupe
    
    group: nom du groupe
    """
    try:

        grp.getgrnam(group)  # juste pour tester l'existance du group_name
        liste = gp.liste_etudiant_group(group)
        with open("../data/createUserMySQL.sql", 'w') as sql_file:
            for etud in liste:
                with open("/home/etudiants/%s/sftp/Projets/pass.txt" % etud['user'].pw_name, "r") as pass_file:
                    password = pass_file.read().strip()
                    pass_file.close()
                    ip = gp.build_ip(etud['user'].pw_uid, IP_CLASS)
                    name = etud['user'].pw_name
                    sql = """
                    CREATE USER '%s'@'10.5.10.2' IDENTIFIED WITH caching_sha2_password BY '%s';
                    CREATE USER '%s'@'%s' IDENTIFIED WITH caching_sha2_password BY '%s';
                    CREATE DATABASE IF NOT EXISTS `%s`;
                    GRANT ALL ON `%s`.* TO '%s'@'10.5.10.2';
                    GRANT ALL ON `%s`.* TO '%s'@'%s';
                    """ % (name, password, name, ip, password, name, name, name, name, name, ip)
                    sql_file.write(sql)
            sql_file.close()

    except KeyError:
        print("Le group_name n'existe pas")
    return

###------------------------------------ DELETE COMMANDS -----------------------------------------###

@click.command(name='group')
@click.argument('group')
@click.option('--sftp', is_flag=True, help='add this option to delete sftp users')
@click.option('--vhost', is_flag=True, help='add this option to delete vhosts')
def delete_group(group, vhost, sftp):
    """Supprime un groupe
    
    group: nom du groupe
    """
    try:

        if vhost:
            gp.sup_vhost(group)
        if sftp:
            gp.sup_sftp_users(group)
        gp.sup_group(group)
    except KeyError as err_key:
        print("pas de group_name specifie %s " % err_key)
    return

@click.command(name='vhost')
@click.argument('group')
def delete_vhost(group):
    """Supprime les vhosts du groupe
    
    group: nom du groupe
    """
    try:
        gp.sup_vhost(group)
    except KeyError as err_key:
        print("pas de group_name specifie (-g) %s " % err_key)
    return

@click.command(name='user')
@click.argument('email_etudiant')
def delete_user(email_etudiant):
    """Supprime un etudiant a partir de son email
    
    email_etudiant: adresse mail de l'etudiant
    """
    try:

        gp.sup_user(email_etudiant)
    except KeyError:
        print("indiquez l'email de l'etudiant que vous voulez supprimer"
              "prenom.nom@etud.u-picardie.fr )")
    return

@click.command(name='container')
@click.argument('group')
def delete_containers(group):
    """Supprime les containers du groupe
    
    group: nom du groupe
    """
    try:
        grp.getgrnam(group)
        liste = gp.liste_etudiant_group(group)
        for etud in liste:
            os.chdir(etud['user'].pw_dir)
            os.system('docker-compose down')
            if os.path.exists("rm %s/.ssh/known_hosts" % etud['user'].pw_dir):
                os.system("rm %s/.ssh/known_hosts" % etud['user'].pw_dir)
    except KeyError:
        print("Le group_name n'existe pas")
    return

@click.command(name='sftp')
@click.argument('group')
def delete_sftp(group):
    """Supprime les sftp pour les utilisateurs du groupe
    
    group: nom du groupe
    """
    try:
        gp.sup_sftp_users(group)
    except KeyError as err_key:
        print("pas de group_name specifie  %s " % err_key)
    return

###------------------------------------ ADD COMMANDS -----------------------------------------###

@click.command(name='acces')
@click.argument('group')
@click.argument('liste_etudiant_input')
@click.option('--sftp', is_flag=True, help='add this option to create sftp users')
@click.option('--vhost', is_flag=True, help='add this option to create vhosts')
@click.option('--skel')
@click.option('--compose')
def add_acces(group, liste_etudiant_input, sftp, vhost, skel, compose):
    cli_opts = {'sftp' : sftp, 'vhost' : vhost, 'skel' : skel, 'compose' : compose}
    # (options -i xxx avec xxx fichier csv | mail | liste de mails)
    try:
        grp.getgrnam(group)
        liste = gp.init_liste(liste_etudiant_input)
        gp.create_users(liste, group)
        build_compte(cli_opts, group, liste)
    except KeyError:
        print("Le group_name %s n'existe pas ! " % group)
    return

###------------------------------------ EXTRA COMMANDS -----------------------------------------###

@click.command()
@click.argument('group')
def extra(group):
    try:

        grp.getgrnam(group)
        liste = gp.liste_etudiant_group(group)

        for etud in liste:
            # os.system("cp %s/.bash_profile %s/.bashrc" % (etud['user'].pw_dir, etud['user'].pw_dir) )
            os.system("chown -R www-data: %s/sftp/Projets" % etud['user'].pw_dir)
            # os.system("rm %s/.ssh/known_hosts" % etud['user'].pw_dir)
            # os.system("chown www-data:sftp /home/sftp/sftp.%s/.ssh/authorized_keys" % etud['user'].pw_name)
            # print("chown www-data:sftp /home/sftp/sftp.%s/.ssh/authorized_keys" % etud['user'].pw_name)

            print("ok")
        sys.exit()

        # remplace un element dans le bash_profile de chaque users
        # for etud in liste:
        #     with open(etud['user'].pw_dir + '/.bash_profile', "r+") as file:
        #         content = file.read()
        #         file.seek(0, 0)
        #         file.write(content.replace('dev@', 'www-data@'))
        #         file.close()
    except KeyError:
        print("Le groupe n'existe pas")
    return

###------------------------------------ SEND COMMANDS -----------------------------------------###

@click.command(name='send')
def send_htpasswd():

    with open('data/sendPassword.txt', 'r') as file:
        line = file.readline()
        while line:
            log, password = line.split('|')
            gestprojmail.sendAccesViaEmail(info={
                'adr': log + '@etud.u-picardie.fr',
                'domain': log.replace('.', '-'),
                'user': log,
                'password': password
            })
            line = file.readline()
        file.close()
    return

###------------------------------------ RUN COMMANDS -----------------------------------------###

@click.command(name='container')
@click.argument('group')
def run_containers(group):
    """Lance les containers du groupe
    
    group: nom du groupe
    """
    try:

        grp.getgrnam(group)  # juste pour tester l'existance du group_name
        liste = gp.liste_etudiant_group(group)
        for etud in liste:
            os.chdir(etud['user'].pw_dir)
            os.system('docker-compose up -d')
    except KeyError:
        print("Le group_name n'existe pas")
    return


def build_compte(cli_opts, group, liste):
    if cli_opts['skel']:
        gp.create_users(liste, group, skelpath=("../conf/%s" % cli_opts['skel']))
    else:
        gp.create_users(liste, group)

    if cli_opts['sftp']:
        gp.create_sftp_users(liste)

    if cli_opts['vhost']:
        print ("Vhost => ", end='')
        gp.create_vhost(liste)
        print("[ok]")
    if cli_opts['compose']:
        gp.create_compose(liste, IP_CLASS, protopath=('../conf/%s' % cli_opts['compose']))
    return

start.add_command(create)
start.add_command(delete)
start.add_command(add)
start.add_command(extra)
start.add_command(send_htpasswd)
start.add_command(run)

create.add_command(create_acces)
create.add_command(create_vhost)
create.add_command(create_compose)
create.add_command(create_containers)
create.add_command(create_sftp)
create.add_command(create_domain)
create.add_command(create_sql)

delete.add_command(delete_group)
delete.add_command(delete_vhost)
delete.add_command(delete_user)
delete.add_command(delete_containers)
delete.add_command(delete_sftp)

add.add_command(add_acces)
add.add_command(create_vhost)

run.add_command(run_containers)

if __name__ == "__main__":
    start()
