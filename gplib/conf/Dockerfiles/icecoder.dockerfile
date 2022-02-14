FROM php

RUN echo "nameserver 193.49.184.5" >> /etc/resolv.conf
RUN apt update -y
RUN apt install zip -y
RUN apt install git -y
RUN git clone https://github.com/icecoder/ICEcoder.git /opt/projet/ICEcoder
WORKDIR /opt/projet

RUN php -r 'include "ICEcoder/classes/Settings.php"; $ref = new ICEcoder\Settings(); $data = $ref->serializedFileData("get", "ICEcoder/lib/template-config-users.php"); array_push($data["bannedFiles"], "ICEcoder"); $data["root"]="/public"; $ref->serializedFileData("set", "ICEcoder/lib/template-config-users.php",$data);'

RUN chown -R www-data: /opt/projet
RUN echo 'www-data:dev' | chpasswd
RUN chsh -s /bin/bash www-data
RUN usermod -d /opt/projet www-data

USER www-data
RUN mkdir /opt/projet/public
CMD php -S 0.0.0.0:8000