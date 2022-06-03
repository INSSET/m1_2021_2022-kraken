import csv
import os
import grp
import pwd
import logging
import logging.handlers
import subprocess
import ovh
import time

CONF_PATH = os.path.dirname(__file__)+"/conf"
SENDMAIL = False


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
Ensemble de fonctions utilitaire
=================================================
"""

def silentCommand(command):
    os.system(command + "> /dev/null 2>&1")


def initStudentListFromFile(path):
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

def getSshPortFromPool():

    sshPoolFilePath = "/home/gestproj/ssh-ports-pool.dat"
    sshPoolFile = open(sshPoolFilePath, "r")

    pool = dict()

    for line in sshPoolFile:
        line = line.split("=")
        pool[line[0]] = line[1].replace("\n", "")

    tempPort = int(pool["IND"]) + 1

    if tempPort > int(pool["MAX"]):
        raise Exception("Limite des ports SSH atteinte")

    os.system("rm -f %s && touch %s" % (sshPoolFilePath, sshPoolFilePath))
    sshPoolFile = open(sshPoolFilePath, "w")
    sshPoolFile.write("MIN=%s\nMAX=%s\nIND=%s" % (pool["MIN"], pool["MAX"], tempPort))

    return tempPort

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


"""
=================================================
Ensemble de fonctions de gestion de Docker
=================================================
"""

def executeContainerActionForTheGroup(action, group, type):

    if getDockerComposeCommandByAction(action) == None:
        raise Exception("L'action %s n'existe pas" % action)

    containerBaseDirectory = "/home/gestproj/.docker/"
    groupDirectory = containerBaseDirectory + group + "/"

    if os.path.exists(groupDirectory) == False:
        raise Exception("Le dossier du groupe %s n'existe pas" % group)

    for studentDirectory in os.listdir(groupDirectory):
        studentDirectoryPath = groupDirectory + studentDirectory
        containerCommandExecutor(studentDirectoryPath, studentDirectory, action, type)



def executeContainerActionForAStudent(action, student, group, type):

    if getDockerComposeCommandByAction(action) is None:
        raise Exception("L'action %s n'existe pas" % action)

    containerBaseDirectory = "/home/gestproj/.docker/"
    groupDirectory = containerBaseDirectory + group + "/"

    if os.path.exists(groupDirectory) == False:
        raise Exception("Le dossier du groupe %s n'existe pas" % group)

    studentDirectoryPath = groupDirectory + student
    containerCommandExecutor(studentDirectoryPath, student, action, type)



def containerCommandExecutor(studentDirectoryPath, studentDirectory, action, type):

    if type is None:
        for studentDirectoryContainerPath in os.listdir(studentDirectoryPath):
            os.chdir(studentDirectoryPath + "/" + studentDirectoryContainerPath)
            silentCommand(getDockerComposeCommandByAction(action) % studentDirectory)
            print("%s > Containers %s" % (studentDirectory, action))
    else:
        if type is not None and os.path.exists(studentDirectoryPath + "/" + type):
            studentContainerPath = studentDirectoryPath + "/" + type
            os.chdir(studentContainerPath)
            silentCommand(getDockerComposeCommandByAction(action) % studentDirectory)
            print("%s > Containers %s" % (studentDirectory, action))
        else:
            raise Exception(
                "Le type de container [%s] n'est pas disponible pour l'utilisateur %s (DirectoryNotFound)" % (
                type, studentDirectory))
    return

def getStudentContainerInformations(group, student, container):

    prefix = group + "-" + student.replace(".", "-") + "-" + container
    proc = subprocess.Popen(["docker ps -af \"name=^%s\" --format \"table {{.ID}}|{{.Names}}|{{.Image}}|{{.Ports}}|{{.State}}\"" % prefix], shell=True, stdout=subprocess.PIPE).stdout
    output = proc.read()
    s = output.decode()
    s = s[:s.rfind('\n')]
    info = ''.join(s.splitlines(keepends=True)[1:])
    splitedInformations = list(filter(None, info.split("|")))

    result = dict()
    result['id'] = splitedInformations[0]
    result['image'] = splitedInformations[2]
    result['ports'] = splitedInformations[3]
    result['status'] = splitedInformations[4]
    result['containerName'] = splitedInformations[1]

    return result

def getContainerLogs(containerId):

    proc = subprocess.Popen(["docker logs %s" % containerId], shell=True, stdout=subprocess.PIPE).stdout
    output = proc.read()
    s = output.decode()
    s = s[:s.rfind('\n')]
    return s


def getDockerComposeCommandByAction(action):
    switch = {
        "up": "docker-compose -p %s up -d",
        "down": "docker-compose -p %s down",
        "restart": "docker-compose -p %s restart",
        "rebuild": "docker-compose -p %s up -d --build",
        "nuke": "docker-compose -p %s down -v"
    }

    return switch.get(action, None)


def pushFileOntoAContainer(containerId, source, mode, target):

    if mode != 1 and mode != 0:
        raise Exception("Le mode de push n'est pas connu. Options : 1 ou 0")

    try:
        os.system("docker exec %s su -c \"cat %s %s %s\"" % (containerId, source, mode, target))
    except Exception as exception:
        logger.error(exception)

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

Création User :

    - Créer l'utilisateur via le skell
    - Chown du home
    - Copier le docker-skell pour l'utilisateur dans le .docker du /home/gestproj (ex: [fragan-gourvil-symfony])
    - Modifier les .env des dossier copier avec les informations du l'utilisateur

"""

def createUsers(list, group):
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

    userSkellPath = "/home/gestproj/user-skell"

    logger.info("start create users")
    for student in list:
        try:
            # si le login n'existe pas alors on crée dans le except
            data = pwd.getpwnam(student['login'])
            logging.error("L'étudiant %s existe déjà UID = %d ",
                          student['login'], data.pw_uid)
            continue
        except KeyError:

            # Création de l'utilisateur
            os.system("useradd -d /home/etudiants/%s -K UID_MIN=10002 -m --skel %s --shell %s -N -g %s %s" % (student['login'], userSkellPath, "/bin/bash", group, student['login']))
            os.system("groupadd %s" % student['login'])

            # os.system("chown -R www-data:sftp /home/etudiants/%s/.ssh" % etudiant['login'])
            # met un pass pour activer le compte

            # On set les group à l'utilisateur

            os.system("usermod -p '*' %s" % student['login'])
            os.system("usermod -G %s %s" % (group, student['login']))
            os.system("usermod -G %s %s" % (student['login'], student['login']))
            os.system("mkdir -p /home/gestproj/.docker/%s/%s" % (group, student['login']))

            # On prépare les docker-skell de l'étudiant
            os.system("cd /home/gestproj/docker-skell/ && for file in *; do cp -r $file /home/gestproj/.docker/%s/%s/$file; done" % (group, student['login']))

            sshPort = getSshPortFromPool()
            # On vient remplir les .env avec les variables attendus en fonction du login
            os.system("for file in /home/gestproj/.docker/%s/%s/*; do [ -d \"$file\" ] && find $file -name '.env.example' | xargs -I{} cat {} | sed -e 's/{STUDENT_NAME}/%s/g' -e 's/{STUDENT_NAME_WITH_DASH}/%s/g' -e 's/#//g' -e 's/{STUDENT_GROUP}/%s/g' -e 's/{STUDENT_SSH_PORT}/%s/g' > $file/.env; done" % (group, student['login'], student['login'], student['login'].replace(".", "-"), group, sshPort))

    logger.info("users created")
    return


def updateAndPropagateSshKeys(student, sshKeyFile, isFile = False):

    try:

        userExist = pwd.getpwnam(student)

    except KeyError as exception:
        raise Exception("L'utilisateur %s n'existe pas" % student)


    userBaseHomePath = "/home/etudiants/" + student

    if os.path.exists(userBaseHomePath):

        userAuthorizedKeys = "/home/etudiants/" + student + "/.ssh/authorized_keys"

        if isFile:
            os.system("cat %s >> %s" % (sshKeyFile, userAuthorizedKeys))
        else:
            os.system("echo %s >> %s" % (sshKeyFile, userAuthorizedKeys))

        os.system("chown root:root %s" % userAuthorizedKeys)

    else:
        raise Exception("Le dossier home de l'utilisateur % n'existe pas" % student)



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


def createGroup(group_name):
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
    logger.info("group %s created", group_name)
    return

def deleteGroup(group):
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

                os.system('groupdel ' + user.pw_name)
                os.system("rm -rf /home/etudiants/%s-*" % user.pw_name)
                os.system("rm -rf /home/gestproj/.docker/%s-*" % user.pw_name)

        os.system('groupdel ' + group)
    except KeyError:
        logger.error("Le group_name %s n'existe pas ", group)
    logger.info("group %s deleted ", group)
    return

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

def create_sql(liste, ipclass):
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
