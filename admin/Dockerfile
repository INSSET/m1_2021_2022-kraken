ARG NODE_VERSION=14

FROM node:${NODE_VERSION}-alpine AS hyrisia_node

WORKDIR /var/www/html

COPY package.json package-lock.json webpack.mix.js ./
COPY resources resources/

RUN set -eux; \
    npm install; \
    npm cache clean --force; \
    mkdir public; \
    npm run production

FROM php:8.1-fpm

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    libpng-dev \
    libonig-dev \
    libxml2-dev \
    zip \
    unzip \
    libpq-dev

# Clear cache
RUN set -eux; \
    apt-get clean; \
    rm -rf /var/lib/apt/lists/*; \
    docker-php-ext-install pdo_mysql mbstring exif pcntl bcmath gd pdo_pgsql pgsql

# Get latest Composer
COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

WORKDIR /var/www/html

ARG USER=webuser

RUN set -eux; \
    useradd $USER -u 1000 -G www-data,root; \
    mkdir -p /home/$USER/.composer; \
    chown -R $USER:$USER /home/$USER

COPY --chown=$USER:www-data composer.json composer.lock artisan .env ./
COPY --chown=$USER:www-data app app/
COPY --chown=$USER:www-data bootstrap bootstrap/
COPY --chown=$USER:www-data database database/
COPY --chown=$USER:www-data config config/
COPY --chown=$USER:www-data lang lang/
COPY --chown=$USER:www-data public public/
COPY --chown=$USER:www-data resources/views resources/views/
COPY --chown=$USER:www-data routes routes/
COPY --chown=$USER:www-data storage storage/
COPY --chown=$USER:www-data --from=hyrisia_node /var/www/html/public public/
COPY docker/php/docker-entrypoint.sh /usr/local/bin/docker-entrypoint

VOLUME /var/www/html

RUN set -eux; \
    composer install; \
    chmod +x /usr/local/bin/docker-entrypoint

ENTRYPOINT ["docker-entrypoint"]
CMD ["php-fpm"]
