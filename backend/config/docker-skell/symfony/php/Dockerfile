ARG PHP_VERSION=8.1

FROM php:${PHP_VERSION}-fpm

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    libpng-dev \
    libonig-dev \
    libxml2-dev \
    openssh-server \
    zip \
    unzip \
    nano

# Clear cache
RUN set -eux; \
    apt-get clean; \
    rm -rf /var/lib/apt/lists/*; \
    docker-php-ext-install pdo_mysql mbstring exif pcntl bcmath gd

# Get latest Composer
COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

RUN set -eux; \
    echo "PasswordAuthentication no" >> /etc/ssh/sshd_config; \
    echo "PermitRootLogin without-password" >> /etc/ssh/sshd_config

WORKDIR /var/www

COPY bin/docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod u+x /usr/local/bin/docker-entrypoint.sh

ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
CMD ["php-fpm"]
