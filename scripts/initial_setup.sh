#!/usr/bin/env bash
# Run this from the root of the repo

# Exit on errors, prevent undefined variables, and fail if any command in a pipeline fails
set -euo pipefail

# Move into repo root
cd "$(dirname "$0")/.."

if crontab -l >/dev/null 2>&1; then
  echo "Cron jobs exist"
  echo "Deleting Cron jobs"
  crontab -i -r
else
  echo "No cron jobs"
fi

echo
echo "Running dependencies check..."
sudo apt update
sudo apt install -y unzip openssl
sudo apt install python3-venv
sudo apt install python3-tk
echo "Dependencies check complete..."

echo 
echo "Setting up Python virtual environment and installing dependencies..."
python3 -m venv .venv
source .venv/bin/activate
pip install python-dotenv

echo
echo "Getting Windows IP"
./scripts/get_ip.sh
echo "Windows IP added to .env"

echo
echo "Ensuring config.ini exists..."
cp -n config.ini.example config.ini

echo
echo "Ensuring .env exists..."
cp -n .env.example .env

echo
echo "Launching setup dialogue box..."
python3 ./src/dialogueBox.py
echo "Setup dialogue box entry complete..."

echo
echo "building images from compose.yaml..."
docker compose build --no-cache

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
echo "running cron_creation.sh..."
./scripts/cron_creation.sh

echo
echo "Setup complete."
