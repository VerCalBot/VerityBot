#!/usr/bin/env bash
# Run this from the root of the repo

# Exit on errors, prevent undefined variables, and fail if any command in a pipeline fails
set -euo pipefail

# Move into repo root
cd "$(dirname "$0")/.."

# start venv and install dependencies
echo "Starting a python virtual environment..."
python3 -m venv .venv
echo "Installing dependencies for email_sender.py..."
pip install python-dotenv

# for reading time fields
declare update_interval
declare cron_command
declare cron_expression

extract_field()
{
  echo "$(grep $1 config.ini | cut -d '=' -f2)"
}

fail() {
    echo
    echo "ERROR: $1"
    exit 1
}

parse_email_time_field()
{
  local h_or_m=$(extract_field "EMAIL_SEND_TIME" | cut -d ':' -f$1)
  if [[ "$h_or_m" =~ ^[0-9]{2}$ ]]; then
    local stoi=10#$h_or_m

    # handle cases where hour > 23 and minute > 59 
    if (( ("$1" == "1" && $stoi > 23) || ("$1" == "2" && $stoi > 59) )); then
      echo "-1"

    elif [[ "$h_or_m" == "00" ]]; then
      echo "0"

    else
      echo $h_or_m | grep -oE '[1-9]+'
    fi

  else
    echo "-1"
  fi
}

write_cron_job()
{
  cat <(fgrep -i -v "$cron_command" <(crontab -l)) <(echo "$cron_expression") | crontab -
}

echo "Creating cron job for ETL..."

update_interval=$(extract_field "ELASTIC_UPDATE_INTERVAL")

CRON_EXEC="$(which "docker")"
CRON_TARGET="$(realpath "compose.yaml")"

cron_command="${CRON_EXEC} compose -f ${CRON_TARGET} up -d"

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

CRON_EXEC="$(which python3)"
CRON_TARGET=$(realpath "src/email_sender.py")

cron_command="${CRON_EXEC} ${CRON_TARGET}"
cron_expression="$(parse_email_time_field "2") $(parse_email_time_field "1") * * * ${cron_command}"

# check if cron_expression contains "-1", this means we reached an edge case
# so send time format is invalid
if [[ "$cron_expression" == *"-1"* ]]; then
  fail "Invalid EMAIL_SEND_TIME, must be in 24-hour format"
fi
write_cron_job
echo "Email cron job created!"

