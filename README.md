# Gestoproj

Gestoin du dépôt et test des projets étudiants

![GitHub Workflow Status](https://img.shields.io/github/workflow/status/INSSET/m1_2021_2022-kraken/admin.yaml) ![GitHub release (latest by date)](https://img.shields.io/github/v/release/NSSET/m1_2021_2022-kraken?color=#56C230)

## Sommaire

* [Installation](#Installation)
* [Backend](#Backend)
* [Interface Admin](#Interface Admin)
* [Interface etudiants](#Interface etudiants)


## Installation

### Premier lancement

Vous devez avoir `docker` et `docker-compose` d'installer sur votre machine. A la racine du dossier, lancez la commande suivante :  

```shell
docker-compose -d
```

Cette commande permet de de lancer l'ensemble des services décrits dans les fichiers `docker-compose.*.yml` en mode détaché (cf. [références docker-compose](https://docs.docker.com/compose/reference/)).

### Architecture des services

Voici un schéma de décomposition des intéractions & dépendances entre les différents services :

```
  
 [Service]                       [Service]                                      [Service]
 Admin UI <---------+--> Backend{API, Lib, CLI, API OVH} ----> Prometheus ----> Grafana
                    |                   |                      [Service]    
           Requests | Responses         |
                    |                   |
 Students UI <------+                +------+
 [Service]                           | HOST |
                                     +------+
```

Les services suivants : **Admin UI** - **Students UI** et le **Backend** sont déclarés dans le fichier `docker-compose.yml`. Les autres services considérés comme "non essentiels" (qui ne néscessitent pas de MAJ régulière) sont définis dans le fichier
`docker-compose.override.yml`.

### Environnement de développement

Pour facilité le développement, les différents services qui disposent d'interfaces (Admin, Students, Grafana, etc...) sont "chachés" derrière un reverse-proxy Nginx vous permettant ainsi de définir
des domaines locaux pour y avoir accès.

## Backend

## Interface Admin

## Interface etudiants
