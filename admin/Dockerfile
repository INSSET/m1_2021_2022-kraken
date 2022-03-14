FROM node:16-slim as builder_development

WORKDIR /usr/src/app/adminapp

COPY package*.json ./

RUN set -eux; \
    npm install; \
    npm cache clean --force;

FROM node:16-slim as development

WORKDIR /usr/src/app/adminapp

COPY --from=builder_development /usr/src/app/adminapp ./

EXPOSE 3000

CMD ["npm", "run", "dev"]

FROM node:16-slim as builder_production

WORKDIR /usr/src/app/adminapp

COPY --from=builder_development /usr/src/app/adminapp ./

COPY . .

RUN set -eux; \
    npm run build;

FROM nginx:stable-alpine as production

COPY nginx.conf /etc/nginx/conf.d/default.conf

COPY --from=builder_production /usr/src/app/adminapp/dist /app

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]

