ARG PHP_VERSION=8.1

FROM php:${PHP_VERSION}-fpm

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    libpng-dev \
    libonig-dev \
    libxml2-dev \
    zip \
    unzip

# Clear cache
RUN set -eux; \
    apt-get clean; \
    rm -rf /var/lib/apt/lists/*; \
    docker-php-ext-install pdo_mysql mbstring exif pcntl bcmath gd

# Get latest Composer
COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

WORKDIR /var/www

RUN set -eux; \
    composer create-project symfony/skeleton:"^6.1" html; \
    cd html; \
    composer require webapp

VOLUME /var/www/html

COPY bin/docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod u+x /usr/local/bin/docker-entrypoint.sh

ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
CMD ["php-fpm"]
