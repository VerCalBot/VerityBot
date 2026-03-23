#!/usr/bin/env bash
# Run this from the root of the repo

# terminate the script immediately if error occurs
set -e

# Move into repo root
cd "$(dirname "$0")/.."

INITIAL_COMPOSE="compose.initial.yaml"
ES_CONTAINER="elasticsearch"
ES_URL="http://localhost:9200"

# Will print the first argument given after using the function fail.  Ex: ERROR: This will be a string appearing after fail.
fail() {
    echo
    echo "ERROR: $1"
    exit 1
}

echo "Checking dependencies..."

# Checks if unzip is installed
if ! command -v unzip &> /dev/null; then
    echo "Error: unzip is required but not installed."
    echo "Please install unzip and rerun this script."
    exit 1
fi

echo "Make sure your .env file already contains the kibana_system password before continuing."
echo "Starting initial stack..."
# -f allows for user to use a specific compose file such as compose.initial instead of the default compose.yaml
docker compose -f "${INITIAL_COMPOSE}" up -d

echo
echo "Waiting for Elasticsearch to start..."

# Iterate i through range of 1 to 60
for i in {1..60}; do
    # if container reponse succeeds then container is ready
    if docker exec "${ES_CONTAINER}" curl -s "${ES_URL}" >/dev/null; then
        echo "Elasticsearch is ready."
        break
    fi

    echo "Still waiting... (${i}/60)"
    sleep 5

    # if i equals 60 then fail
    if [ "$i" -eq 60 ]; then
        fail "Elasticsearch did not start in time.
Check logs with: docker compose -f ${INITIAL_COMPOSE} logs elasticsearch"
    fi
done

echo
echo "Resetting kibana_system password..."
echo "When prompted, enter the password you already placed in your .env file."

# -it ensures user can enter password into terminal
docker exec -it "${ES_CONTAINER}" \
    bin/elasticsearch-reset-password \
    -u kibana_system \
    -i \
    --url "${ES_URL}"

echo
echo "Stopping initial stack..."
docker compose -f "${INITIAL_COMPOSE}" down

echo
echo "Running certificate creation script..."
./scripts/cert_creation.sh

echo
echo "Starting normal secure stack..."
docker compose up -d

echo
echo "Setup complete."