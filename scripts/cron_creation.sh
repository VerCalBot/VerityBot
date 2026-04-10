#!/usr/bin/env bash
# Run this from the root of the repo

# Exit on errors, prevent undefined variables, and fail if any command in a pipeline fails
set -euo pipefail

# Move into repo root
cd "$(dirname "$0")/.."

# install dependencies
echo "Installing dependencies..."
# pip install python-dotenv
# pip install python-crontab

# for reading time fields
declare update_interval
declare cron_command
declare cron_expression

extract_email_time_field()
{
  echo "$(grep )"
  #local time="$(grep -e $1 config.ini | grep -oE '[0-9]+|:' | tr -d '\n')"
  #IFS=':' read -r hours mins <<< "$time"
}

extract_etl_time_field()
{
  update_interval="$(grep $1 config.ini | cut -d '=' -f2)"
}

write_cron_job()
{
  cat <(fgrep -i -v "$cron_command" <(crontab -l)) <(echo "$cron_expression") | crontab -
}

fail() {
    echo
    echo "ERROR: $1"
    exit 1
}

echo "Creating cron job for ETL..."
extract_etl_time_field "ELASTIC_UPDATE_INTERVAL"

DOCKER_PATH="$(which "docker")"
COMPOSE_PATH="$(realpath "compose.yaml")"

cron_command="${DOCKER_PATH} compose -f ${COMPOSE_PATH} up -d"

case $update_interval in
  *m)
    minutes=${update_interval%m}
    cron_expression="*/$minutes * * * * $cron_command"
    ;;
  *h)
    hours=${update_interval%h}
    cron_expression="0 */$hours * * * $cron_command"
    ;;
  *d)
    days=${update_interval%d}
    cron_expression="0 0 */$days * * $cron_command"
    ;;
  *)
    fail "Invalid ELASTIC_UPDATE_INTERVAL"
    ;;
esac

write_cron_job
echo "ETL cron job created!"

echo "Creating cron job for email sender..."
