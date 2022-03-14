# Gestoproj

Gestoin du dépôt et test des projets étudiants

![GitHub Workflow Status](https://img.shields.io/github/workflow/status/INSSET/m1_2021_2022-kraken/admin.yaml) ![GitHub release (latest by date)](https://img.shields.io/github/v/release/NSSET/m1_2021_2022-kraken?color=#56C230)

## Sommaire

* [Installation](#Installation)
* [Backend](#Backend)
* [Interface Admin](#Interface Admin)
* [Interface etudiants](#Interface etudiants)
* [Sprint](#Sprint)
  * [Iteration 1](#Interation_1)


## Installation

### Premier lancement

Vous devez avoir `docker` et `docker-compose` d'installer sur votre machine. A la racine du dossier, lancez la commande suivante :  

```shell
docker-compose up -d
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

## Sprint
### Itération 1
Pour commencer la première itération qui se déroule du 14 mars 2022 au 10 avril 2022, les éléments du backlog suivant ont été retenus :
- ID 181265103, <em>As an administrator, I want to display all students by group</em>.
    - <em>Create/Refacto API endpoints</em> assigné à **Micke Niepceron**.
    - <em>Write API tests</em> assigné à **Micke Niepceron**.
    - <em>Create the components for the admin interface</em> assigné à **Thibaut Picart**.
- ID 181514415, <em>API Design</em>, assigné à **Laurent Cusimano**.
- ID 181263538, <em>Creating the continuous integration</em>.
  - <em>Dockerfile admin</em> assigné à **Fragan Gourvil**.
  - <em>Dockerfile students</em> assigné à **Fragan Gourvil**.
  - <em>Dockerfile backend</em> assigné à **Fragan Gourvil**.
  - <em>Sonarqube</em> assigné à **Fragan Gourvil**.
- ID 181263594, <em>As a administrator I want to modifiy the group list</em>.
    - <em>Create/Refacto API endpoints</em> assigné à **Micke Niepceron**.
    - <em>Write API tests</em> assigné à **Micke Niepceron**.
    - <em>Create the components for the admin interface</em> assigné à **Tanguy Paquet**.
- ID 181252403, <em>Refactoring the CLI source code</em> assigné à **Jérémy Krzeczowski**.