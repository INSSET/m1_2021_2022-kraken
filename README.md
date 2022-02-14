# GestProj
Gestoin du dépôt et test des projets étudiants

## Initialisation server
installer : apache2, openssh-server  
module : dav_fs, proxy, authz_groupfile  
créer repertoire : /home/etudiants  
ajout group : sftp
Créer certificat, et fixer variable APACHE_CRT_DIR dans envars  
ajouter conf dans sshd_config  


    nopass et key ssh
    PasswordAuthentication no
    PermitEmptyPasswords no


    Match group sftp
    ChrootDirectory %h
    X11Forwarding no
    AllowTcpForwarding no
    ForceCommand internal-sftp

## Init image

    docker build -t php/symfony - < ../conf/Dockerfiles/symfony.dockerfile

## Détail du répertoire conf
- Repertoire **email** : il contient les maquettes des mails que l'on peut envoyer aux étudiants
- Repertoire **sites-available** : il contient le prototype du fichier de conf pour le virtualhost de l'étudiant
- repertoire **skel** : arborecence recopiée lors de la création du compte utilisateur (compte normal pas sftp)
- Fichier **adduser.conf** : configuration utiliser par la commande adduser (obsolette on utilise useradd)
- Fichier **docker-compose.yaml** : prototype de la configuration pour les services docker proposé à l'étudiants

## User guide & ref options

    # python3 GestProj.py -i ../data/l2-2020/test.txt -g l2-2020 --all create acces
    # python3 GestProj.py -g l2-2020 --all delete group
    
Exute un docker-compose up pour chaque etudiant du group et démare le daemon sshd
    
    # python3 GestProj.py -g l2-2020 create container
    # python3 GestProj.py -g l2-2020 delete container
    
## Droit sur les dossier pour bon fonctionnement du sftp chroot
Tous les répertoires jusqu'au HOME sftp de l'étudiant doivent apartenir à root avec le mode 755  
Le .ssh et sont contenu doit appartenir au usr et avoir les droits 755 (fichier inclus)


## MYSQL
Le gestionaire de base de données pour les TD et projets et MySQL. 
MySQL est exécuté dans un container à partir de l'image officielle Docker.
Le container est associé au bridge des container étudiants (ex:l3-2020)
avec une adr IP fixe du bridge. On peut aussi ajouter phpmyadmin pour avoir une UI.
Exemple

    docker run --name=mysql -e MYSQL_ROOT_PASSWORD=mysql-pw --network=l3-2020 --ip=10.5.10.1 -d mysql
    docker run --name=phpmyadmin --network=l3-2020 --ip 10.5.10.2 -e PMA_HOST=10.5.10.1 -d phpmyadmin/phpmyadmin

Pour se connecter au serveur et créer des comptes db par exemple

    docker run --rm -ti -v /home/harold/GestProj/data:/data --network=l3-2020 --ip=10.5.10.10 mysql mysql -u root -h 10.5.10.1 -p
    
Pour créer les comptes mysql et les base de données 

    mysql> source/createUserMySQL.sql;

## Pour tester

    $ docker build -t ubuntu/gestproj .
    $ docker run -ti --rm -v /var/run/docker.sock:/var/run/docker.sock -v `pwd`/GestProj:/home/test ubuntu/gestproj
