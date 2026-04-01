#!/usr/bin/env bash
# Run this from the root of the repo

# terminate the script immediately if error occurs
set -e

# Move into repo root
cd "$(dirname "$0")/.."


echo
echo "Running dependencies script..."
./scripts/install_dependencies.sh

echo
echo "running elastic_setup.sh..."
./scripts/elastic_setup.sh

echo
echo "Running certificate creation script for ElasticSearch..."
./scripts/cert_creation.sh

echo
echo "Running nginx setup..."
./scripts/nginx_setup.sh

echo
echo "Starting normal secure stack..."
docker compose up -d

echo
echo "Setup complete."