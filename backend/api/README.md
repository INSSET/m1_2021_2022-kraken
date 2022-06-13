## Déploiement
Via GitHub avec un git clone et un clef de déploiement  
Lancement du service dans un virtual env

    python3 -m venv /home/ui_user/env_run

    export PYTHONPATH=$PYTHONPATH:{gestprojpath}/lib

## Développement

    docker build -t gestproj/api -f Dockerfile ..
