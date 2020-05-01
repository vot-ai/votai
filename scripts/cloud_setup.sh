#! /usr/bin/env bash

# Exit in case of error
set -e

source 'prod.env'

if [ ! -x "$(command -v docker)" ]; then
    echo " Installing Docker..."
    # Install docker
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
    apt-get update
    apt-cache policy docker-ce
    apt-get install -y docker-ce
    apt install -y apache2-utils
    echo " Done!"
fi

if [ ! -x "$(command -v docker-compose)" ]; then
    echo " Installing Docker Compose..."
    # Install compose
    curl -L "https://github.com/docker/compose/releases/download/1.25.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
    docker-compose --version
    echo " Done!"
fi

# Get env vars
echo "What is the Traefik password (for the user 'admin')?"
read TRAEFIK_PASS
htpasswd -nb admin "$TRAEFIK_PASS" > traefik_users

echo "What is the Grafana password (for the user 'admin')?"
read GRAFANA_PASS
echo "$GRAFANA_PASS" > grafana_password

echo "What is the Prometheus password (for the user 'admin')?"
read PROMETHEUS_PASS
htpasswd -nb admin "$PROMETHEUS_PASS" > prometheus_users

echo " Generating stack files..."
# Generate the stack file
./scripts/generate-stack.sh

echo " Setting up Docker Swarm..."
# Get IP
IP=$(curl http://checkip.amazonaws.com)
# Initialize swarm
docker swarm init --advertise-addr $IP || true
# Create the proxy network
docker network create -d overlay proxy || true

echo " Creating acme.json..."
# Create acme file
touch acme.json
chmod 600 acme.json
touch .htpasswd
chmod 600 .htpasswd

echo " Building local deps"
./scripts/build.sh

echo " Deploying stack"
./scripts/deploy.sh
