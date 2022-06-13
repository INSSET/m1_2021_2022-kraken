## Utilitaire de gestion de compte en ligne de commande

    docker build -t gestproj/lib ../lib -f Dockerfile

# Documentation
utiliser la cli
```shell
python3 cli.py [COMMANDS]
```

- add
    - group : Crée un groupe a partir d'une liste d'etudiants
    - user : Crée des virtual hosts pour les membres du groupe
- rm
    - group : Supprime un groupe et ses utilisateurs
    - user : Supprime un utilisateur à partir de son adresse mail
- container : Permet d'interagir avec les containers des étudiants
    -> actions possibles : afficher les logs
- student : Permet d'interagir avec les espaces étudiants
    -> actions possibles : update les clés SSH
- ssh : retourne un port ssh pour un container