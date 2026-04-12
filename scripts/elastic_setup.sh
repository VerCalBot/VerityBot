#!/usr/bin/env bash
# Run this from the root of the repo

# Exit on errors, prevent undefined variables, and fail if any command in a pipeline fails
set -euo pipefail

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

    # if i is greater than or equal to 60 then fail
    if [ "$i" -ge 60 ]; then
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
