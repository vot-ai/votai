# Warning! This Dockerfile uses BuildKit features. Read about it here https://github.com/moby/buildkit

# Load environment
ARG APP_ENV=dev
FROM python:3.8.1-slim-buster as base

# Configure environment
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install runtime dependencies
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y gcc libpq-dev
RUN apt-get clean

# Set Workdir
WORKDIR /app

## add user
RUN addgroup --system user && adduser --system --group user
RUN mkdir /prometheus_tmp
RUN chown -R user:user /prometheus_tmp && chmod -R 755 /prometheus_tmp

# Create venv
RUN pip install -U setuptools pip
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Running global install
FROM base as install

# copy app and install python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# Prod postinstall
FROM install as prod-postinstall

COPY ./ /app/

RUN python manage.py collectstatic --noinput

# Configure user ownership
RUN chown -R user:user /app && chmod -R 755 /app

# Dev Postinstall
FROM install as dev-postinstall

# Cleanup stage
FROM ${APP_ENV}-postinstall as cleanup

# Cleanup
RUN \
    rm -rf requirements.txt docker-entrypoint.sh
RUN apt-get autoremove -y gcc

# Dev pre final stage
FROM base as dev-prefinal

# Prod pre final stage
FROM base as prod-prefinal

COPY --from=cleanup /app/ /app/

# Final stage
FROM ${APP_ENV}-prefinal as final

# Install Dockerize
# https://github.com/jwilder/dockerize
ENV DOCKERIZE_VERSION v0.6.1
RUN apt-get -y install wget
RUN wget "https://github.com/jwilder/dockerize/releases/download/${DOCKERIZE_VERSION}/dockerize-linux-amd64-${DOCKERIZE_VERSION}.tar.gz" \
    && tar -C /usr/local/bin -xzvf "dockerize-linux-amd64-${DOCKERIZE_VERSION}.tar.gz" \
    && rm "dockerize-linux-amd64-${DOCKERIZE_VERSION}.tar.gz" && dockerize --version
RUN apt-get autoremove -y wget

COPY --from=cleanup /opt/venv /opt/venv

# Prepare entrypoint
COPY docker-entrypoint.sh docker-entrypoint.sh
RUN chmod a+x docker-entrypoint.sh

# switch to non-root user
USER user

ENTRYPOINT ["./docker-entrypoint.sh"]
