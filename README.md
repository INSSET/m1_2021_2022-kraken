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
  * [Iteration 2](#Interation_2)


## Installation

### Premier lancement

Vous devez avoir `docker` et `docker-compose` d'installer sur votre machine. A la racine du dossier, lancez la commande suivante :  

```shell
docker-compose -f docker-compose.dev.yml -f docker-compose.override.yml up -d --build
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
    - <em>Create/Refacto API endpoints</em> assignée à **Micke Niepceron**.
    - <em>Write API tests</em> assigné à **Micke Niepceron**.
    - <em>Create the components for the admin interface</em> assignée à **Thibaut Picart**.
- ID 181514415, <em>API Design</em>, assignée à **Laurent Cusimano**.
- ID 181263538, <em>Creating the continuous integration</em>.
  - <em>Dockerfile admin</em> assignée à **Fragan Gourvil**.
  - <em>Dockerfile students</em> assignée à **Fragan Gourvil**.
  - <em>Dockerfile backend</em> assignée à **Fragan Gourvil**.
  - <em>Sonarqube</em> assignée à **Fragan Gourvil**.
- ID 181263594, <em>As an administrator I want to modifiy the group list</em>.
    - <em>Create/Refacto API endpoints</em> assignée à **Micke Niepceron**.
    - <em>Write API tests</em> assignée à **Micke Niepceron**.
    - <em>Create the components for the admin interface</em> assignée à **Tanguy Paquet**.
- ID 181252403, <em>Refactoring the CLI source code</em> assignée à **Jérémy Krzeczowski**.
### Itération 2
Pour commencer la première itération qui se déroule du 11 avril 2022 au 16 mai 2022, les éléments du backlog suivant ont été retenus :
- Reliquats de l'itération 1, à savoir les tâches : 
  - ID 181263594, <em>As an administrator I want to modifiy the group list</em>.
  - ID 181265103, <em>As an administrator, I want to display all students by group</em>.
- ID 181263518, <em>As an administrator I want to be able to update students list</em> assignée à **Micke Niepceron**.
  - <em>Create/Refacto API endpoints</em> assignée à **Micke Niepceron**.
  - <em>Write API tests</em> assigné à **Micke Niepceron**.
  - <em>Create the components for the admin interface</em> assignée à **Tanguy Paquet**.
- ID 181854424, <em>As a developper I want to access API Documentation</em> assignée à **Laurent Cusimano**.
- ID,181264576, <em>Change SSH authentification</em> assignée à **Laurent Cusimano**.
- ID 181854744, <em>Ajouter fonctions de gestions dans la lib gestproj</em> assignée à **Jérémy Krzeczowski**.
- ID 181854420, <em>As a front dev, i need wireframes</em> assignée à **Fragan Gourvil**.
- ID 181854404, <em>As a developer I want to use SonarQube</em> assignée à **Fragan Gourvil**.
- ID 181263543, <em>Create the continuous deployment script</em> assignée à **Fragan Gourvil**.
- ID 181265034, <em>As an administrator, I want to be able to monitor every students' containers</em> assignée à **Micke Niepceron**.
  - <em>Create/Refacto API endpoints</em> assignée à **Micke Niepceron**.
  - <em>Write API tests</em> assigné à **Micke Niepceron**.
  - <em>Create the components for the admin interface</em> assignée à **Thibaut Picart**.

### Itération 3
Pour commencer la troisière itération qui se déroule du 16 avril 2022 au 17 juin 2022, les éléments du backlog suivant ont été retenus :
- ID 181854424, <em>As a developper I want to access API Documentation (auto generated swagger)</em> assignée à **Laurent Cusimano**.
- ID 181264576, <em>Change SSH authentification</em> assignée à **Laurent Cusimano**.
- ID 181263543, <em>Create the continuous deployment script</em> assignée à **Fragan Gourvil**.
- ID 181253513, <em>As a student, i want to upload a public key</em> assignée à **Thibaut Picart**.
  - <em>Create/Refacto API endpoints</em> assignée à **Micke Niepceron**.
  - <em>Write API tests</em> assigné à **Micke Niepceron**.
- ID 181253565, <em>As a student, I want to update my public key</em> assignée à **Thibaut Picart**.
  - <em>Create/Refacto API endpoints</em> assignée à **Micke Niepceron**.
  - <em>Write API tests</em> assigné à **Micke Niepceron**.
- ID 181263528, <em>As a administrator I want to be able to modify the DNS</em> assignée à **Fragan Gourvil**.
- ID 181263622, <em>As a administrator I want to update the students Dockerfile</em> assignée à **Jérémy Krzeczowski**.
- ID 181263502, <em>As an administrator I want to be able to interact with the student spaces</em> assignée à **Jérémy Krzeczowski**.
- ID 181263804, <em>As an administrator, I want to be able to add a late student</em> assignée à **Tanguy Paquet**.
  - <em>Create/Refacto API endpoints</em> assignée à **Micke Niepceron**.
  - <em>Write API tests</em> assigné à **Micke Niepceron**.
- ID 181265034, <em>As an administrator, I want to be able to monitor every students' containers</em> assignée à **Micke Niepceron**.
  - <em>Create the components for the admin interface</em> assignée à **Thibaut Picart**.
  - <em>Create the components for the user interface</em> assignée à **Fragan Gourvil**.
