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
RUN chown -R user:user /app && chmod -R 755 /app

# Create venv
RUN pip install -U setuptools pip
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Preinstall commands
FROM base as preinstall

# Install build deps
# RUN apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev linux-headers libffi-dev openssl-dev python3-dev make libc-dev

# Running global install
FROM preinstall as install

# copy app and install python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# Prod postinstall
FROM install as prod-postinstall

COPY ./ /app/

RUN python manage.py collectstatic --noinput

# Dev Postinstall
FROM install as dev-postinstall

# Cleanup stage
FROM ${APP_ENV}-postinstall as cleanup

# Cleanup
RUN \
    # apk --purge del .build-deps && \
    rm -rf requirements.txt docker-entrypoint.sh
RUN apt-get autoremove -y gcc

# Dev pre final stage
FROM base as dev-prefinal

# Prod pre final stage
FROM base as prod-prefinal

COPY --from=cleanup /app/ /app/

# Final stage
FROM ${APP_ENV}-prefinal as final

COPY --from=cleanup /opt/venv /opt/venv

# Prepare entrypoint
COPY docker-entrypoint.sh docker-entrypoint.sh
RUN chmod a+x docker-entrypoint.sh

## switch to non-root user
USER user

ENTRYPOINT ["./docker-entrypoint.sh"]
