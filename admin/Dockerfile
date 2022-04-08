FROM node:16-slim as builder_development

ARG USER=admin
ARG UID=1005

RUN set -eux; \
    useradd $USER -u $UID -G www-data,root; \
    chown -R $USER:$USER /home/$USER


WORKDIR /usr/src/app/

COPY --chown=$USER:www-data package*.json ./

USER $USER;

RUN set -eux; \
    npm install; \
    npm cache clean --force;

FROM node:16-slim as development

WORKDIR /usr/src/app/

ARG USER=admin
ARG UID=1000

RUN set -eux; \
    useradd $USER -u $UID -G www-data,root; \
    chown -R $USER:$USER /home/$USER

COPY --from=builder_development /usr/src/app/ ./

RUN mkdir node_modules/.vite && chmod -R 777 node_modules/.vite

EXPOSE 4000

CMD ["npm", "run", "dev"]

FROM node:16-slim@sha256:9b43cdacd070d1b38976a804aec78f03139c600865a3c72501af3bbec8d4bdee as build_vendor

ARG USER=admin
ARG UID=1005

RUN set -eux; \
    useradd $USER -u $UID -G www-data,root; \
    mkdir -p /home/$USER/; \
    chown -R $USER:$USER /home/$USER

WORKDIR /usr/src/app/

COPY --chown=$USER:www-data package*.json ./

RUN set -eux; \
    npm install; \
    npm cache clean --force;

FROM node:16-slim@sha256:9b43cdacd070d1b38976a804aec78f03139c600865a3c72501af3bbec8d4bdee as builder_production

WORKDIR /usr/src/app/

ARG USER=admin
ARG UID=1005

RUN set -eux; \
    useradd $USER -u $UID -G www-data,root; \
    mkdir -p /home/$USER/; \
    chown -R $USER:$USER /home/$USER; \
    chown -R $USER:$USER /usr/src/app/

COPY --chown=$USER:www-data --from=build_vendor /usr/src/app/ ./

COPY --chown=$USER:www-data . .

USER $USER

RUN set -eux; \
    npm run build

FROM nginx:stable-alpine@sha256:26716e37188bd01374360199773bc8ad8736edb7e234a2a1956a13b9800fccc4 as production

COPY --chown=$USER:www-data nginx.conf /etc/nginx/conf.d/default.conf

COPY --chown=$USER:www-data --from=builder_production /usr/src/app/dist /app

COPY --from=builder_production /usr/src/app/dist /app

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]

