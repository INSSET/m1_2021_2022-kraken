FROM node:16-slim as builder_development

ARG USER=admin
ARG UID=1000

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

USER $USER

CMD ["npm", "run", "dev"]

FROM node:16-slim as builder_production

WORKDIR /usr/src/app/

ARG USER=admin
ARG UID=1000

RUN set -eux; \
    useradd $USER -u $UID -G www-data,root; \
    chown -R $USER:$USER /home/$USER

COPY --chown=$USER:www-data --from=builder_development /usr/src/app/ ./

COPY --chown=$USER:www-data . .

USER $USER

RUN set -eux; \
    npm run build;

FROM nginx:stable-alpine as production

COPY --chown=$USER:www-data nginx.conf /etc/nginx/conf.d/default.conf

COPY --chown=$USER:www-data --from=builder_production /usr/src/app/dist /app

USER $USER

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]

