#!/usr/bin/env bash
# Run this from the root of the repo

# terminate the script immediately if error occurs
set -e

echo "Checking dependencies..."
sudo apt update

# Checks if unzip is installed
if ! command -v unzip &> /dev/null; then
    echo "Installing unzip..."
    sudo apt install -y unzip
fi

# Checks if nginx is installed
if ! command -v nginx &> /dev/null; then
    echo "Installing nginx..."
    sudo apt install -y nginx
fi

# Checks if nginx is installed
if ! command -v openssl &> /dev/null; then
    echo "Installing openssl..."
    sudo apt install -y openssl
fi

echo "Dependencies check complete"