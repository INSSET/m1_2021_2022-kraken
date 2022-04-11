import sys
sys.path.append("/usr/src/app/gplib")

import gestprojlib as gp

import getopt
import sys
import os
import grp
import gestprojmail

DOMAIN = 'insset.ovh'
GROUP = "l2-2020"
LISTE = "../data/" + GROUP + "/test.csv"
IP_CLASS = "10.5"  # pour le croup l3


# IP_CLASS = " 172.18" # pour le group_name lp


def start(cli_args, cli_opts):
    actions = {
        'create': create,
        'delete': delete,
        'add': ajout,
        'extra': extra,
        'send': send_htpasswd,
        'run': run,
    }
    action = actions.get(cli_args[0], lambda: "Action %s inconnue !" % cli_args[0])
    action(cli_args[1:], cli_opts)
    return


def create(cli_args, cli_opts):
    quoi = {
        'acces': create_acces,
        'vhost': create_vhost,
        'compose': create_compose,
        'container': create_containers,
        'sftp': create_sftp,
        'domain': create_alias_domain,
        'sql': create_userdb_sql,
    }
    quoi.get(cli_args[0], lambda: "create %s inconnue !" % cli_args[0])(cli_opts)


def run(cli_args, cli_opts):
    quoi = {
        'container': run_containers,
    }
    quoi.get(cli_args[0], lambda: "run %s inconnue !" % cli_args[0])(cli_opts)


def delete(cli_args, cli_opts):
    quoi = {
        'group_name': delete_group,
        'vhost': delete_vhost,
        'user': delete_user,
        'container': delete_containers,
        'sftp': delete_sftp,
    }
    quoi.get(cli_args[0], lambda: "delete %s inconnue !" % cli_args[0])(cli_opts)
    return


def ajout(cli_args, cli_opts):
    quoi = {
        'acces': ajout_acces,
        'vhost': create_vhost,
    }
    quoi.get(cli_args[0], lambda: "create %s inconnue !" % cli_args[0])(cli_opts)
    return


def build_compte(cli_opts, liste):
    group = cli_opts['-g']
    if '--skel' in cli_opts:
        gp.create_users(liste, group, skelpath=("../conf/%s" % cli_opts['--skel']))
    else:
        gp.create_users(liste, group)

    if '--sftp' in cli_opts:
        gp.create_sftp_users(liste)
    if '--vhost' in cli_opts:
        print('Vhost => ', end='', flush=True)
        gp.create_vhost(liste)
        print("[ok]")
    if '--compose' in cli_opts:
        gp.create_compose(liste, IP_CLASS, protopath=('../conf/%s' % cli_opts['--compose']))
    return


def extra(cli_args, cli_opts):
    try:
        group = cli_opts['-g']
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
        print("Le group_name n'existe pas ou l'argument -g n'est pas renseigné ")
    return


def create_acces(cli_opts):
    try:
        # Pas de mails étudiants données en entrée
        # (options -i xxx avec xxx fichier csv | mail | liste de mails)
        liste_etudiant_input = cli_opts['-i']
        group = cli_opts['-g']
        try:
            info_grp = grp.getgrnam(group)
            print("Le Groupe %s existe déjà %d " % (info_grp.gr_name, info_grp.gr_gid))
            # sys.exit()
        except KeyError:
            print("Création du group_name %s " % group)

        liste = gp.init_liste(liste_etudiant_input)
        gp.create_group(group)
        build_compte(cli_opts, liste)

    except KeyError as err_key:
        print("Erreur pas d'arguement %s " % err_key)

    return


def create_vhost(cli_opts):
    try:
        group = cli_opts['-g']
        grp.getgrnam(group)
        liste = gp.liste_etudiant_group(group)
        gp.create_vhost(liste)
    except KeyError:
        print("Le group_name n'existe pas ou l'argument -g n'est pas renseigné ")
    return


def create_compose(cli_opts):
    try:
        group = cli_opts['-g']
        grp.getgrnam(group)
        liste = gp.liste_etudiant_group(group)
        if '--compose' in cli_opts:
            gp.create_compose(liste, IP_CLASS, protopath=('../conf/%s' % cli_opts['--compose']))
        else:
            gp.create_compose(liste, IP_CLASS)
    except KeyError:
        print("Le group_name n'existe pas ou l'argument -g n'est pas renseigné ")
    return


def create_containers(cli_opts):
    try:
        group = cli_opts['-g']
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
        print("Le group_name n'existe pas ou l'argument -g n'est pas renseigné ")
    return


def run_containers(cli_opts):
    try:
        group = cli_opts['-g']
        grp.getgrnam(group)  # juste pour tester l'existance du group_name
        liste = gp.liste_etudiant_group(group)
        for etud in liste:
            os.chdir(etud['user'].pw_dir)
            os.system('docker-compose up -d')
    except KeyError:
        print("Le group_name n'existe pas ou l'argument -g n'est pas renseigné ")
    return


def create_sftp(cli_opts):
    try:
        group = cli_opts['-g']
        grp.getgrnam(group)
        liste = gp.liste_etudiant_group(group)
        gp.create_sftp_users(liste, group)
    except KeyError:
        print("Le group_name n'existe pas ou l'argument -g n'est pas renseigné ")

    return


def create_alias_domain(cli_opts):
    """
    Ajoute tous les sous domaine étudiants à la zone DOMAIN (normalement insset.ovh)
    :return:
    """
    try:
        liste_etudiant_input = cli_opts['-i']
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
        print("Le group_name n'existe pas ou l'argument -g n'est pas renseigné ")

    return


def create_userdb_sql(cli_opts):
    try:
        group = cli_opts['-g']
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
        print("Le group_name n'existe pas ou l'argument -g n'est pas renseigné ")

    return


def delete_group(cli_opts):
    try:
        group = cli_opts['-g']
        if '--vhost' in cli_opts:
            gp.sup_vhost(group)
        if '--sftp' in cli_opts:
            gp.sup_sftp_users(group)
        gp.sup_group(group)
    except KeyError as err_key:
        print("pas de group_name spécifié (-g) %s " % err_key)
    return


def delete_user(cli_opts):
    try:
        email_etudiant = cli_opts['-i']
        gp.sup_user(email_etudiant)
    except KeyError:
        print("indiquez avec l'option -i l'email de l'étudiant que vou voulez supprimer (-i "
              "prenom.nom@etud.u-picardie.fr )")
    return


def delete_vhost(cli_opts):
    try:
        group = cli_opts['-g']
        gp.sup_vhost(group)
    except KeyError as err_key:
        print("pas de group_name spécifié (-g) %s " % err_key)
    return


def delete_containers(cli_opts):
    try:
        group = cli_opts['-g']
        grp.getgrnam(group)
        liste = gp.liste_etudiant_group(group)
        for etud in liste:
            os.chdir(etud['user'].pw_dir)
            os.system('docker-compose down')
            if os.path.exists("rm %s/.ssh/known_hosts" % etud['user'].pw_dir):
                os.system("rm %s/.ssh/known_hosts" % etud['user'].pw_dir)
    except KeyError:
        print("Le group_name n'existe pas ou l'argument -g n'est pas renseigné ")
    return


def ajout_acces(cli_opts):
    try:
        # Pas de mails étudiants données en entrée
        # (options -i xxx avec xxx fichier csv | mail | liste de mails)
        liste_etudiant_input = cli_opts['-i']
        group = cli_opts['-g']
        try:
            grp.getgrnam(group)
            liste = gp.init_liste(liste_etudiant_input)
            gp.create_users(liste, group)
            build_compte(cli_opts, liste)
        except KeyError:
            print("Le group_name %s n'existe pas ! " % group)
    except KeyError as err_key:
        print("Erreur pas d'arguement %s " % err_key)

    return


def send_htpasswd(cli_args, cli_opts):
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


def delete_sftp(cli_opts):
    try:
        group = cli_opts['-g']
        gp.sup_sftp_users(group)
    except KeyError as err_key:
        print("pas de group_name spécifié (-g) %s " % err_key)
    return


if __name__ == "__main__":

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'g:i:', ['sftp', 'vhost', 'skel=', 'compose='])
        info = {}
        for o, a in opts:
            info[o] = a
        start(args, info)

    except getopt.GetoptError as err:
        print(err)
