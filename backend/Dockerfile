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
    openssh-server \
    nano \
    curl \
    $PYTHON_VERSION \
    python3-pip \
    python-dev \
    git

RUN curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
RUN chmod +x /usr/local/bin/docker-compose

# Création des dossiers néscessaires

RUN set -eux; \
    apt-get clean; \
    rm -rf /var/lib/apt/lists/*; \
    mkdir -p /home/etudiants

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
COPY --chown=$USER:$USER config/docker-skell docker-skell/
COPY --chown=$USER:$USER config/user-skell user-skell/
COPY --chown=$USER:$USER config/ssh-ports-pool.dat ssh-ports-pool.dat

RUN set -eux; \
    pip install -r api/requirements.txt --no-cache-dir; \
    pip install -r cli/requirements.txt --no-cache-dir; \
    pip install -r ovh/requirements.txt --no-cache-dir; \
    mkdir .docker; \
    echo alias gp=\'python3 /home/$USER/cli/cli.py \' >> /root/.bashrc

# Préparation du volume data dans lequel sera stocké les données

RUN set -eux; \
    ln -s /home/test/lib/gestprojlib.py /usr/lib/$PYTHON_VERSION/gestprojlib.py

ENV CONF_OVH_PATH=/home/$USER/ovh/conf
ENV CONF_OVH_FILE="Gestproj_12_2021_ovh.conf"
ENV PYTHONPATH=/home/$USER/gplib

COPY docker-entrypoint.sh /usr/local/bin
RUN chmod u+x /usr/local/bin/docker-entrypoint.sh

EXPOSE 5000

WORKDIR /home/$USER/cli

CMD ["/usr/local/bin/docker-entrypoint.sh"]
