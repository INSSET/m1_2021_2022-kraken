## Utilitaire de gestion de compte en ligne de commande

    docker build -t gestproj/lib ../lib -f Dockerfile

# Documentation
utiliser la cli
```shell
python3 main.py [COMMANDS]
```

- create
    - acces : Crée un groupe a partir d'une liste d'etudiants
    - vhost : Crée des virtual hosts pour les membres du groupe
    - compose : Installe les docker compose des membres du groupe
    - container : Crée les containers pour les membres du groupe (fonction écrite dans la cli mais pas dans la lib gestproj)
    - sftp : Crée des utilisateurs SFTP pour les membres du groupe
    - domain : Crée des domaines(OVH) pour les étudiants de la liste (fonction écrite dans la cli mais pas dans la lib gestproj)
    - sql : Cree un utilisateur SQL pour chaque membres du groupe (fonction écrite dans la cli mais pas dans la lib gestproj)
- delete
    - group : Supprime les utilisateurs du groupe, puis le groupe
    - vhost : Supprime les Virtual Hosts du groupe
    - user : supprime un utilisateur (à partir de son mail)
    - container : supprime les containers du groupe
    - sftp : supprime les utilisateurs SFTP du groupe
- add
    - acces : crée une liste d'utilisateurs et les affecte au groupe
    - vhost : Crée des virtual hosts pour les membres du groupe
- run
    - run containers : lance les containers des membres du groupe
- send : la fonction ne fonctionne pas !