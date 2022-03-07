FROM node:12.19.0-slim as builder

WORKDIR /usr/src/app/adminapp

COPY package*.json ./

RUN set -eux; \
    npm install; \
    npm cache clean --force;

FROM node:12.19.0-slim AS development

WORKDIR /usr/src/app/adminapp

COPY --from=builder /usr/src/app/adminapp ./

CMD ["npm", "run", "serve"]

EXPOSE 3000

FROM node:12.19.0-slim AS production

WORKDIR /usr/src/app/adminapp

COPY --from=builder /usr/src/app/adminapp ./

COPY src/ src/

RUN set -eux; \
    npm run production;

CMD ["npm", "run", "serve"]

EXPOSE 3000


