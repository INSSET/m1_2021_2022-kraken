FROM ubuntu:20.04

# Global update
RUN apt update -y

ENV TZ = Europe/Paris

# Timezone setup
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime
RUN echo $TZ > /etc/timezone

# Apache installation
RUN apt install -y apache2 openssl

RUN mkdir /etc/apache2/ssl-certificat
WORKDIR /etc/apache2/ssl-certificat

# OpenSSL certification
RUN openssl genrsa 2048 > server.key
RUN openssl req -new  \
	-subj "/C=FR/ST=Aisne/L=Saint-quentin/O=INSSET/OU=IT Department/CN=licence-st.u-picardie.fr" \
	-key server.key > server.csr
RUN openssl genrsa 2048 > ca.key
RUN openssl req -new -x509 -days 365 \
	-subj "/C=FR/ST=Somme/L=Amiens/O=UPJV/OU=IT Department/CN=licence-st.u-picardie.fr" \
	-key ca.key > ca.crt
RUN openssl x509 -req -in server.csr -out server.crt -CA ca.crt -CAkey ca.key -CAcreateserial -CAserial ca.srl
RUN echo "export APACHE_CRT_DIR=\$APACHE_CONFDIR/ssl-certificate" >> /etc/apache2/envvars

RUN a2enmod dav_fs proxy authz_groupfile

RUN apt install -y openssh-server

RUN mkdir -p /run/sshd
RUN echo "\n\
Match group sftp\n\
  ChrootDirectory %h\n\
  X11Forwarding no\n\
  AllowTcpForwarding no\n\
  ForceCommand internal-sftp\n\
" >> /etc/ssh/sshd_config

RUN mkdir -p /home/etudiants

RUN apt install -qy curl
RUN curl -sSL https://get.docker.com/ | sh
RUN groupadd sftp

RUN adduser test

# env pour faire tourner les libs
WORKDIR /home/test

RUN apt install -y python3
RUN apt update -y
RUN apt install -y python3-pip

# Le numéro de version de python est à changer en fonction de la version de python installée
RUN ln -s /home/test/lib/gestprojlib.py /usr/lib/python3.8/gestprojlib.py
RUN pip install click

RUN python3 -m pip install --upgrade pip
RUN apt install -y git
RUN pip install -e git+https://github.com/ovh/python-ovh.git#egg=ovh

COPY requirements.txt ./

RUN pip install -r requirements.txt

ENV CONF_OVH_PATH=/home/test/ovh/conf
ENV CONF_OVH_FILE="Gestproj_12_2021_ovh.conf"

ENV PYTHONPATH=/home/test/gplib

EXPOSE 5000

WORKDIR /usr/src/app

