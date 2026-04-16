#!/usr/bin/env bash
# Run this from the root of the repo

set -euo pipefail

# Move into repo root
cd "$(dirname "$0")/.."

WINDOWS_IP=$(/mnt/c/Windows/System32/ipconfig.exe | sed -n '/Wireless LAN adapter.*:/,/IPv4 Address/s/.*IPv4 Address[^:]*: //p' | head -n 1 | tr -d '\r' | xargs)

if [ -z "$WINDOWS_IP" ]; then
    WINDOWS_IP=$(/mnt/c/Windows/System32/ipconfig.exe | sed -n '/Ethernet adapter.*:/,/IPv4 Address/s/.*IPv4 Address[^:]*: //p' | head -n 1 | tr -d '\r' | xargs)
fi

if [ -z "$WINDOWS_IP" ]; then
    echo "ERROR: Could not determine Windows IP"
    exit 1
fi

grep -q "^WINDOWS_IP=" .env && \
    sed -i "s|^WINDOWS_IP=.*|WINDOWS_IP=$WINDOWS_IP|" .env || \
    echo "WINDOWS_IP=$WINDOWS_IP" >> .env