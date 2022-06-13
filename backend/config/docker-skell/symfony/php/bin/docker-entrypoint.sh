#!/bin/bash
set -e

service ssh start
/usr/sbin/sshd -D&

if [ ! -d "/var/www/html/vendor" ]; then
  composer create-project symfony/skeleton:"^6.1" /var/www/html
  cd /var/www/html
  composer require webapp
fi

if [ "${1#-}" != "$1" ]; then
	set -- php-fpm "$@"
fi

exec docker-php-entrypoint "$@"