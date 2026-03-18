#!/usr/bin/env bash
# Run this in the root dir of your repo

# terminate the script immediately if error occurs
set -e

# Move into repo root
cd "$(dirname "$0")/.."

# Working folder dir
CERT_DIR="./certs"

# Elastic Search (ES) image
ES_IMAGE="docker.elastic.co/elasticsearch/elasticsearch-wolfi:9.3.0"

# if dir CERT_DIR folder doesnt exist create in root
mkdir -p "${CERT_DIR}"

# If statement checking to see if CERT_DIR contains Certificate Authority (CA) already
if [ -f "${CERT_DIR}/ca/ca.crt" ]; then

    # echo just prints out string
    echo "Certs already exist. Terminating."

    # return no error
    exit 0
# closes if block
fi

echo "Generating CA"

# Run temp container using ES IMAGE, mount (-v) local certs folder inside container as /certs
# create CA using ES tool certutil and zip it into /certs
# MSYS_NO_PATHCONV=1 prevents Linux paths converting into Windows paths when using Git Bash
MSYS_NO_PATHCONV=1 docker run --rm \
    -v "$(pwd)/certs:/certs" \
    "${ES_IMAGE}" \
    bin/elasticsearch-certutil ca --silent --pem -out /certs/ca.zip

# unzip the ca.zip into certs
unzip -q certs/ca.zip -d certs

echo "Generating ES node certificate"

# Run temp container using ES IMAGE, mount local certs folder inside container as /certs
# create public cert and private key for elasticsearch using ES tool certutil and zip it into /certs/ca
MSYS_NO_PATHCONV=1 docker run --rm \
    -v "$(pwd)/certs:/certs" \
    "${ES_IMAGE}" \
    bin/elasticsearch-certutil cert --silent --pem \
    --ca-cert /certs/ca/ca.crt \
    --ca-key /certs/ca/ca.key \
    --name elasticsearch \
    --ip 127.0.0.1 \
    --dns elasticsearch,localhost \
    --out /certs/elasticsearch.zip

unzip -q certs/elasticsearch.zip -d certs

echo "Generating Kibana node certificate"

# Run temp container using ES IMAGE, mount local certs folder inside container as /certs
# create public cert and private key for elasticsearch using ES tool certutil and zip it into /certs/ca
MSYS_NO_PATHCONV=1 docker run --rm \
    -v "$(pwd)/certs:/certs" \
    "${ES_IMAGE}" \
    bin/elasticsearch-certutil cert --silent --pem \
    --ca-cert /certs/ca/ca.crt \
    --ca-key /certs/ca/ca.key \
    --name kibana \
    --dns kibana,localhost \
    --ip 127.0.0.1 \
    --out /certs/kibana.zip

unzip -q certs/kibana.zip -d certs

echo "Kibana Certificates created and stored in certs/kibana"

echo "Removing zip files"

# Remove temporary zip files
rm -f certs/ca.zip certs/elasticsearch.zip certs/kibana.zip

echo "Script executed successfully"