# Load env
ARG APP_ENV=dev
FROM node:13.7-alpine as base

ENV HOST 0.0.0.0

WORKDIR /app

RUN mkdir /app/node_modules

## add user
RUN addgroup -S user && adduser -S user -G user
RUN chown -R user:user /app/node_modules && chmod -R 755 /app/node_modules

# Install Dockerize
# https://github.com/jwilder/dockerize
RUN apk add --no-cache openssl
ENV DOCKERIZE_VERSION v0.6.1
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz

# Install dev env
FROM base as dev-install

# Install prod env
FROM base as prod-install

COPY package.json /app/

RUN apk add python make g++

RUN yarn install

COPY ./ /app/

FROM ${APP_ENV}-install as postinstall
FROM base as cleanup

WORKDIR /app
COPY --from=postinstall /app/ /app/

FROM cleanup as dev-prefinal

RUN apk add python make g++

COPY dev-entrypoint.sh /docker-entrypoint.sh

CMD ["yarn", "dev"]

FROM cleanup as prod-prefinal

COPY docker-entrypoint.sh /docker-entrypoint.sh

# Configure folder ownership
RUN chown -R user:user /app && chmod -R 755 /app

CMD ["yarn", "start"]

FROM ${APP_ENV}-prefinal as final

RUN chmod a+x /docker-entrypoint.sh

# switch to non-root user
USER user

ENTRYPOINT ["/docker-entrypoint.sh"]
