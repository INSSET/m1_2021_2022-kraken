import csv
import os
import grp
import pwd
import logging
import logging.handlers
import subprocess
import ovh

CONF_PATH = os.path.dirname(__file__)+"/conf"
SENDMAIL = False
DOMAIN = 'insset.ovh'


"""
=================================================
Gestion des logs
Les erreurs et autres messages informant l'état 
d'exécusion de la lib sont par défaut envoyé au 
system de gestion syslog (si il existe)
La variable d'environnment LOG_LEVEL permet de 
définir le niveau de log voulu { DEBUG, INFO ... }
par defaut le niveau est ERROR
L'object logger est utilisé pour efectuer les log
=================================================
"""

FORMAT = '%(asctime)s %(message)s'
LOG_LEVEL = logging.ERROR
logging.basicConfig(format=FORMAT)

logger = logging.getLogger('lib')
if 'LOG_LEVEL' in os.environ and hasattr(logging, os.environ['LOG_LEVEL']):
    LOG_LEVEL = os.environ['LOG_LEVEL']
logger.setLevel(LOG_LEVEL)  # si la variable d'env existe on en tient compte

if os.path.exists('/dev/log'):
    sys_handler = logging.handlers.SysLogHandler(address='/dev/log')
    logger.addHandler(sys_handler)  # on utilise le syslog si il existe

"""
=================================================
Ensemble de fonctions de type utilitaire
=================================================
"""


def init_liste(path):
    """
    Sélectionne le reader en fonction de l'extension
    :param path:
    :return:
    """
    filename, file_extension = os.path.splitext(path)
    if file_extension == '.csv':
        return init_liste_etudiant_csv(path)
    elif file_extension == '.txt':
        return init_liste_etudiant_txt(path)


def init_liste_etudiant_csv(nom_fichier_csv):
    """
    Initialise deux tableaux à partir du fichier obtenu en exportant au format CSV les notes sous moodle
    Dans le fichier CSV la colonne 7 contient le mail de l'étudiant. On extrait du ce mail la parti gauche du @
    pour former le login de l'étudiant.
    En remplçant les . par des - dans le login de l'étudiant on obtient le sous domaine
    :param nom_fichier_csv:
    :return:
    """
    liste = []
    num_col = 6  # la 7ème colonne du CSV contient le e-mail de l'étudiant
    with open(nom_fichier_csv, newline='') as csvfile:
        etudiants_reader = csv.reader(csvfile, delimiter=',')
        next(etudiants_reader)
        for etudiant in etudiants_reader:
            mail = etudiant[num_col]
            login = (mail.split('@'))[0]
            # pour éviter de dépasser les 32 caractères du login quand on rajoute sftp. devant
            login = login[0:26]
            liste.append({'email': mail, 'login': login,
                         'domain': login.replace('.', '-')})

    return liste


def init_liste_etudiant_txt(nom_fichier_txt):
    """
    Initialise deux tableaux à partir d'un fichier contenant une liste de mail
    En remplçant les . par des - dans le login de l'étudiant on obtient le sous domaine
    :param nom_fichier_txt:
    :return:
    """
    liste = []
    with open(nom_fichier_txt, newline='') as txtfile:
        for mail in txtfile:
            login = (mail.split('@'))[0]
            # pour éviter de dépasser les 32 caractères du login quand on rajoute sftp. devant
            login = login[0:26]
            testexist = False
            for user in pwd.getpwall():
                if user.pw_name == login:
                    testexist = True
            if not testexist:
                liste.append({'email': mail, 'login': login,
                             'domain': login.replace('.', '-')})

    return liste


def liste_etudiant_group(group):
    """
    Parcours tous les users de /etc/passwd est construit le tableau liste avec ceux qui appartienne au group_name
    indiqué en paramètre
    :param group: nom du groupe system (dans /etc/group_name)
    :return:
    """
    liste = []
    try:
        info_grp = grp.getgrnam(group)
        for user in pwd.getpwall():
            if user.pw_gid == info_grp.gr_gid:
                liste.append({'user': user, 'login': user.pw_name,
                             'domain': user.pw_name.replace('.', '-')})
    except KeyError:
        logger.error("Ref user non trouvé ")

    return liste


def build_ip(uid, ipclass):
    """
    on remplace l'IP du container en le determinant en fonction de l'UID de l'etudiant
    Exemple :
        pour ipclass = "192.168" et uid = 10023 on aura "192.168.0.23"
        pour ipclass = "192.168" et uid = 10265 on aura "192.168.1.10"
    :param uid: l'identifiant unique de l'utilisateur (forcement supérieur à 10002)
    :param ipclass: les deux premier octect caractérisant la class B (ex : "192.168")
    :return: une ip class IV sous forme de chaîne de caractaires
    """
    ip_base = int(uid) - 10000
    ip_class_b = int(ip_base / 256)
    ip_class_c = ip_base % 256
    ip = "%s.%s.%s" % (ipclass, ip_class_b, ip_class_c)
    return ip


""" 
=================================================
Ensemble de fonctions de création
    - site virtuel
    - compte utilisateur
    - accès sftp utilisateur
    - group
    - le docker-compose associé à chaque compte
=================================================
"""


def create_vhost(liste, default=CONF_PATH+"/sites-available/virtualhost.conf", dirpath="/etc/apache2/sites-enabled",
                 sendpasspath="../data/sendPassword.txt"):
    """
    A partir d'une liste de user et d'un template de virtual host génére les Virualhost
    :param liste:
    :param default:
    :param dirpath:
    :param sendpasspath:
    :return:
    """
    logger.info("start create vhost")
    for etudiant in liste:
        try:
            user_info = pwd.getpwnam(etudiant['login'])
            with open(default, "r") as vhostFileProto:
                cf_v_host = vhostFileProto.read()
                with open("%s/%s-%s.conf" % (dirpath, user_info.pw_uid, etudiant['login'].replace('.', '-')),
                          'w') as vhostFileEtud:
                    cf_v_host = cf_v_host.replace(
                        "{SUBDOMAIN}", etudiant['domain'])
                    cf_v_host = cf_v_host.replace("{LOGIN}", etudiant['login'])
                    cf_v_host = cf_v_host.replace(
                        "{PORT}", str(user_info.pw_uid))
                    cf_v_host = cf_v_host.replace(
                        "{PROJET_DIR}", user_info.pw_dir + '/sftp/Projets')
                    group_info = grp.getgrgid(user_info.pw_gid)
                    cf_v_host = cf_v_host.replace(
                        "{GROUP}", group_info.gr_name)
                    if os.path.exists('/etc/apache2/passwd/' + group_info.gr_name):
                        import secrets
                        import string
                        alphabet = string.ascii_letters + string.digits
                        password = ''.join(secrets.choice(alphabet)
                                           for i in range(8))
                        os.system("htpasswd -b /etc/apache2/passwd/%s %s %s" % (
                            group_info.gr_name, etudiant['login'], password))
                        with open(sendpasspath, 'a+') as file:
                            file.write("%s|%s\n" %
                                       (etudiant['login'], password))
                            file.close()
                        os.system('echo "%s" > %s/sftp/Projets/pass.txt' %
                                  (password, user_info.pw_dir))
                    vhostFileEtud.write(cf_v_host)
                    vhostFileEtud.close()
                vhostFileProto.close()

                if os.path.exists("/etc/apache2/passwd/%s-groups" % group_info.gr_name):
                    with open("/etc/apache2/passwd/%s-groups" % group_info.gr_name, 'a') as file:
                        file.write("%s : %s admin" %
                                   (etudiant['login'], etudiant['login']) + '\n')
                        file.close()
        except KeyError:
            logger.error(
                "Pas d'entrée dans passwd pour l'étudiant %s !", etudiant['login'])
    logger.info("vhost created")
    logger.info("reload apache2")
    os.system('service apache2 reload')
    return


def create_users(liste, group, skelpath=CONF_PATH+"/skel", shell="/bin/bash"):
    """
    A partir d'une liste d'identifiant utilisateur on ajoute un compte user
    Ce user sera celui de l'étudiant sur le serveur pour accéder à son container
    L'id du user est le premier libre au-dessus de 10002,
    :param liste:
    :param group: group_name auquel appartiendra le user
    :param skelpath: le template de fichiers contenu dans le home
    :param shell: le shell lancé à la connexion
    :return:
    """

    logger.info("start create users")
    for etudiant in liste:
        try:
            # si le login n'existe pas alors on crée dans le except
            data = pwd.getpwnam(etudiant['login'])
            logging.error("L'étudiant %s existe déjà UID = %d ",
                          etudiant['login'], data.pw_uid)
            continue
        except KeyError:
            os.system("useradd -d /home/etudiants/%s -K UID_MIN=10002 -m --skel %s --shell %s -N -g %s %s" % (
                etudiant['login'], skelpath, shell, group, etudiant['login']))
            # os.system("chown -R www-data:sftp /home/etudiants/%s/.ssh" % etudiant['login'])
            # met un pass pour activer le compte
            os.system("usermod -p '*' %s" % etudiant['login'])
            os.system("usermod -G %s %s" % (group, etudiant['login']))
            os.system("chown root:root /home/etudiants/%s" % etudiant['login'])
    logger.info("users created")
    return


def create_sftp_users(liste, shell="/bin/bash"):
    """
    Similaire à create_users, la fonction crée à partir d'une liste de user des comptes dont le login est
    sftp.user avec un uid supérieur à 10002. Le group_name est, par contre, toujours 'sftp'.
    Le repertoire home
    :param liste:
    :param shell:
    :return:
    """

    logger.info("start create sftp user account")
    for etudiant in liste:
        try:
            data = pwd.getpwnam("sftp.%s" % etudiant['login'])
            logging.error("L'étudiant sftp.%s existe déjà UID = %d ",
                          etudiant['login'], data.pw_uid)
            continue
        except KeyError:
            os.system("useradd -d /home/etudiants/%s/sftp -K UID_MIN=10002 --shell %s -N -g %s sftp.%s" % (
                etudiant['login'], shell, 'sftp', etudiant['login']))
            # met un pass pour activer le compte
            os.system("usermod -p '*' sftp.%s" % etudiant['login'])
            os.system("mkdir -p /home/etudiants/%s/sftp/Projets" %
                      etudiant['login'])
            os.system("mkdir -p /home/etudiants/%s/sftp/.ssh" %
                      etudiant['login'])
            os.system("chown root:root /home/etudiants/%s/sftp" %
                      etudiant['login'])
            os.system("chown sftp.%s:sftp /home/etudiants/%s/sftp/Projets" %
                      (etudiant['login'], etudiant['login']))
            os.system("chown sftp.%s:sftp /home/etudiants/%s/sftp/.ssh" %
                      (etudiant['login'], etudiant['login']))
            os.system("chmod 775 /home/etudiants/%s/sftp/Projets" %
                      etudiant['login'])
    logger.info("sftp accounts created")
    return


def create_group(group_name):
    """
    Création du group portant le nom (group_name), c'est la première fonction exécutée généralement
    Ensuite, il y a création de deux fichiers :
        /etc/apache2/passwd/(group-name)
        /etc/apache2/passwd/(group-name)-groups
    Le premier permettant un accès à tous les sites de ce groupe avec les identifiants Login:admin Pass:admin.insset
    Le deuxième contiendra les accès individualisés pour chaque utilisateur
    :param group_name:
    :return:
    """

    logger.info("create group %s", group_name)
    try:
        data = grp.getgrnam(group_name)
        logging.error("Le group_name %s existe déjà GID = %d ",
                      group_name, data.gr_gid)
    except KeyError:
        os.system('groupadd -K GID_MIN=10000 ' + group_name)
        if not os.path.exists('/etc/apache2/passwd/'):
            os.mkdir('/etc/apache2/passwd/')
        # variante de création avec l'instruction subprocess.run(...)
        # run(['htpasswd', '-c'], input="/etc/apache2/passwd/%s admin #admin#" % group_name , encoding='ascii')
        os.system(
            "htpasswd -bc /etc/apache2/passwd/%s admin admin.insset" % group_name)
        os.system("touch /etc/apache2/passwd/%s-groups" % group_name)
    logger.info("group %s created", group_name)
    return


def create_compose(liste, ipclass, protopath='../conf/docker-compose.yaml', composepath='docker-compose.yaml'):
    """

    :param liste:
    :param ipclass:
    :param protopath:
    :param composepath:
    :return:
    """
    logger.info("Install Docker Compose")
    for etudiant in liste:
        try:
            user_info = pwd.getpwnam(etudiant['login'])

            ip_container = build_ip(user_info.pw_uid, ipclass)
            # personalisation du fichier .bashrc
            with open(user_info.pw_dir + '/.bash_profile', 'r+') as rc:
                content = rc.read()
                content = content.replace("{IP}", ip_container)
                content = content.replace("{USER}", user_info.pw_name)

                rc.seek(0, 0)
                rc.write(content)
                rc.close()

            # os.system('cp ' + user_info.pw_dir + '/.bashrc ' + user_info.pw_dir + '/.bash_profile')
            os.system("chown root:root %s/.bash_profile" % user_info.pw_dir)

            with open(protopath, 'r') as dockerComposeFileProto:
                compose_yaml = dockerComposeFileProto.read()
                with open(user_info.pw_dir + '/' + composepath, 'w') as dockerComposeEtud:
                    compose_yaml = compose_yaml.replace(
                        "{PORT}", str(user_info.pw_uid))
                    # compose_yaml = compose_yaml.replace("{GROUP}", grp.getgrgid( user_info.pw_gid ).gr_name)
                    # ___________________________________________________________
                    # !!!!!! gros problème d'affectation réseau à résoudre !!!!!
                    # ___________________________________________________________
                    compose_yaml = compose_yaml.replace("{GROUP}", 'l3-2020')
                    compose_yaml = compose_yaml.replace("{IP}", ip_container)
                    compose_yaml = compose_yaml.replace(
                        "{PROJET_DIR}", user_info.pw_dir + '/sftp/Projets')
                    compose_yaml = compose_yaml.replace(
                        "{LOGIN}", etudiant['login'])
                    dockerComposeEtud.write(compose_yaml)
                    dockerComposeEtud.close()
                dockerComposeFileProto.close()
        except KeyError:
            logger.error("[Erreur] L'étudiant %s n'existe pas",
                         etudiant['login'])
    logger.info("docker comose installed")
    return


def sup_group(group):
    """
    Suprime tous les utilisateurs appartenant à se groupe, en comparant
    le n° du groupe de tous les utilisateurs et on supprime quand il y a
    correspondance. Pour finir, on supprime le groupe quand il est vide
    :param group:
    :return:
    """

    logger.info("delete group %s", group)
    try:
        info_grp = grp.getgrnam(group)
        for user in pwd.getpwall():
            if user.pw_gid == info_grp.gr_gid:
                msg = subprocess.check_output(["userdel", "-f", "--remove", user.pw_name],
                                              stderr=subprocess.STDOUT,
                                              text=True)
                if not msg.isspace():
                    logger.info(msg.strip())
        os.system('groupdel ' + group)
    except KeyError:
        logger.error("Le group_name %s n'existe pas ", group)
    logger.info("group %s deleted ", group)
    return


def sup_vhost(group):
    """

    :param group:
    :return:
    """
    try:
        info_grp = grp.getgrnam(group)
        for user in pwd.getpwall():
            if user.pw_gid == info_grp.gr_gid:
                os.system("rm /etc/apache2/sites-enabled/%s-%s.conf" %
                          (user.pw_uid, user.pw_name.replace('.', '-')))

        if os.path.exists('/etc/apache2/passwd/' + group):
            os.remove('/etc/apache2/passwd/' + group)

        if os.path.exists("/etc/apache2/passwd/%s-groups" % group):
            os.remove("/etc/apache2/passwd/%s-groups" % group)
    except KeyError:
        logger.error("Le group_name %s n'existe pas ", group)


def sup_user(email):
    """
    Supprime un utilisateur à partir de son email
    :param email:
    :return:
    """
    login = (email.split('@'))[0]
    # pour éviter de dépasser les 32 caractères du login quand on rajoute sftp. devant
    login = login[0:26]
    try:
        user = pwd.getpwnam(login)
        msg = subprocess.check_output(
            ["userdel", "-f", "--remove", user.pw_name], stderr=subprocess.STDOUT, text=True)
        if not msg.isspace():
            logger.info(msg)
        if os.path.exists("/etc/apache2/sites-enabled/%s-%s.conf" % (user.pw_uid, user.pw_name.replace('.', '-'))):
            os.system("rm /etc/apache2/sites-enabled/%s-%s.conf" %
                      (user.pw_uid, user.pw_name.replace('.', '-')))
    except KeyError:
        logger.error("Compte étudiant inexistant %s ", login)

    return


def sup_sftp_users(group):
    """

    :param group:
    :return:
    """
    try:
        info_grp = grp.getgrnam(group)
        for user in pwd.getpwall():
            if user.pw_gid == info_grp.gr_gid:
                os.system("userdel -f sftp.%s" % user.pw_name)

    except KeyError:
        logger.error("Le group_name %s n'existe pas ", group)


def create_containers(liste, grp_sftp):
    for etud in liste:
        os.chdir(etud['user'].pw_dir)
        os.system('docker-compose up -d')
        os.system("docker exec %s groupadd -f -g %s sftp" %
                  (etud['user'].pw_name, grp_sftp.gr_gid))
        os.system("docker exec %s useradd -d /opt/projet --shell /bin/bash -u %s -g sftp %s" % (
            etud['user'].pw_name, etud['user'].pw_uid, etud['user'].pw_name))
        os.system(
            'docker exec %s bash -c \'echo "%s:dev" | chpasswd\'' % (etud['user'].pw_name, etud['user'].pw_name))
        os.system("docker exec %s chown -R %s /opt/projet" %
                  (etud['user'].pw_name, etud['user'].pw_name))
        os.system("rm /home/etudiants/%s/.ssh/known_hosts" %
                  etud['user'].pw_name)


def create_domains(liste):
    client = ovh.Client(config_file='ovh/ovh.conf')
    for etudiant in liste:
        un_domain = etudiant['login'].replace('.', '-')
        result = client.post('/domain/zone/' + DOMAIN + '/record',
                             fieldType='CNAME',
                             subDomain=un_domain,
                             target=DOMAIN + '.',
                             ttl=None,
                             )
        #print(result['subDomain'] + '=' + str(result['id']))


def create_sql(liste):
    with open("../data/createUserMySQL.sql", 'w') as sql_file:
        for etud in liste:
            with open("/home/etudiants/%s/sftp/Projets/pass.txt" % etud['user'].pw_name, "r") as pass_file:
                password = pass_file.read().strip()
                pass_file.close()
                ip = build_ip(etud['user'].pw_uid, ipclass)
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


def delete_containers(liste):
    for etud in liste:
        os.chdir(etud['user'].pw_dir)
        os.system('docker-compose down')
        if os.path.exists("rm %s/.ssh/known_hosts" % etud['user'].pw_dir):
            os.system("rm %s/.ssh/known_hosts" % etud['user'].pw_dir)


def run_containers(liste):
    for etud in liste:
        os.chdir(etud['user'].pw_dir)
        os.system('docker-compose up -d')
