#!/bin/sh
set -e

if [ "${1#-}" != "$1" ]; then
	set -- php-fpm "$@"
fi

if [ "$1" = 'php-fpm' ]; then

    composer install

    until php artisan db:alive; do
            echo "Waiting for MySQL to be ready..."
            sleep 1
    done

    php artisan key:generate

    php artisan migrate:fresh && php artisan db:seed

    chmod -R 777 storage/

fi

exec docker-php-entrypoint "$@"
