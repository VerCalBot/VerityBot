#!/usr/bin/env bash
# Run this from the root of the repo

# Exit on errors, prevent undefined variables, and fail if any command in a pipeline fails
set -euo pipefail

# Move into repo root
cd "$(dirname "$0")/.."

echo
echo "Running dependencies check..."
sudo apt update
sudo apt install -y unzip openssl
echo "Dependencies check complete..."

echo
echo "running elastic_setup.sh..."
./scripts/elastic_setup.sh

echo
echo "Running certificate creation script for ElasticSearch..."
./scripts/cert_creation.sh

echo
echo "Starting normal secure stack..."
docker compose up -d

echo
echo "Setup complete."