FROM ubuntu:20.04@sha256:9101220a875cee98b016668342c489ff0674f247f6ca20dfc91b91c0f28581ae

# Arguments pour le build
ARG TIMEZONE=Europe/Paris
ARG USER=gestproj
ARG UID=1000
ARG PYTHON_VERSION=python3.8

# Config de la TZ

RUN set -eux; \
    ln -snf /usr/share/zoneinfo/$TIMEZONE /etc/localtime; \
    echo $TIMEZONE > /etc/timezone

# Installation des packages

RUN apt update && apt install -y \
    apache2 \
    openssl \
    openssh-server \
    curl \
    $PYTHON_VERSION \
    python3-pip \
    python-dev \
    git

# Création des dossiers néscessaires
RUN set -eux; \
    apt-get clean; \
    rm -rf /var/lib/apt/lists/*; \
    mkdir /etc/apache2/ssl-certificat; \
    mkdir -p /home/etudiants

WORKDIR /etc/apache2/ssl-certificat

# OpenSSL certification
RUN set -eux; \
    openssl genrsa 2048 > server.key; \
    openssl req -new  \
	-subj "/C=FR/ST=Aisne/L=Saint-quentin/O=INSSET/OU=IT Department/CN=licence-st.u-picardie.fr" \
	-key server.key > server.csr

RUN set -eux; \
    openssl genrsa 2048 > ca.key; \
    openssl req -new -x509 -days 365 \
	-subj "/C=FR/ST=Somme/L=Amiens/O=UPJV/OU=IT Department/CN=licence-st.u-picardie.fr" \
	-key ca.key > ca.crt

RUN set -eux; \
    openssl x509 -req -in server.csr -out server.crt -CA ca.crt -CAkey ca.key -CAcreateserial -CAserial ca.srl; \
    echo "export APACHE_CRT_DIR=\$APACHE_CONFDIR/ssl-certificate" >> /etc/apache2/envvars

RUN a2enmod dav_fs proxy authz_groupfile

# Config SSH pour le sftp

RUN set -eux; \
    groupadd sftp; \
    mkdir -p /run/sshd; \
    echo "\n\
          Match group sftp\n\
          ChrootDirectory %h\n\
          X11Forwarding no\n\
          AllowTcpForwarding no\n\
          ForceCommand internal-sftp\n\
        " >> /etc/ssh/sshd_config

# Installation de Docker

RUN set -eux; \
    curl -sSL https://get.docker.com/ | sh

# Création de répertoire principale pour l'execution des services

RUN set -eux; \
    useradd $USER -u $UID -G sftp,root; \
    mkdir -p /home/$USER/; \
    chown -R $USER:$USER /home/$USER

WORKDIR /home/$USER

# Copie des services & dépendances

COPY --chown=$USER:$USER gplib gplib/
COPY --chown=$USER:$USER api api/
COPY --chown=$USER:$USER cli cli/
COPY --chown=$USER:$USER ovh ovh/

RUN set -eux; \
    pip install -r api/requirements.txt --no-cache-dir; \
    pip install -r cli/requirements.txt --no-cache-dir

# Préparation du volume data dans lequel sera stocké les données

RUN set -eux; \
    ln -s /home/test/lib/gestprojlib.py /usr/lib/$PYTHON_VERSION/gestprojlib.py; \
    mkdir data

# On "expose" le dossier data comme volume pour permettre une persistance des données hors conteneur
VOLUME data

ENV CONF_OVH_PATH=/home/$USER/ovh/conf
ENV CONF_OVH_FILE="Gestproj_12_2021_ovh.conf"
ENV PYTHONPATH=/home/$USER/gplib

EXPOSE 5000

WORKDIR /home/$USER/api

USER $USER

CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0"]
