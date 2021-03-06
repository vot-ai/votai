#!/bin/sh

# Check that mongo is up and running on port `27017`:
dockerize -wait 'tcp://mongo:27017' -timeout 30s -wait-retry-interval 3s

echo "Building locally"
yarn build
echo "Done! Executing command"
exec "$@"
