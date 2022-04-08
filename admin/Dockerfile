FROM node:16-slim as builder_development

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

FROM node:16-slim as development

WORKDIR /usr/src/app

COPY --from=builder_development /usr/src/app/ ./

EXPOSE 4000

CMD ["npm", "run", "dev"]

FROM node:16-slim as builder_production

WORKDIR /usr/src/app/

ARG USER=admin
ARG UID=1005

RUN set -eux; \
    useradd $USER -u $UID -G www-data,root; \
    mkdir -p /home/$USER/; \
    chown -R $USER:$USER /home/$USER; \
    chown -R $USER:$USER /usr/src/app/

COPY --chown=$USER:www-data --from=builder_development /usr/src/app/ ./

COPY --chown=$USER:www-data . .

USER $USER

RUN set -eux; \
    npm run build

FROM nginx:stable-alpine as production

COPY nginx.conf /etc/nginx/conf.d/default.conf

COPY --from=builder_production /usr/src/app/dist /app

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]

