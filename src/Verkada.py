import json
import requests
import logging
import datetime

def login(args) -> requests.Session:
    logging.info("Logging in to Verkada")
    session = requests.Session()
    session.headers.update({
        "accept": "application/json",
        "x-api-key": args.verkada_api_key,
    })
    response = session.post("https://api.verkada.com/token")
    st = response.status_code
    if st >= 200 and st < 300:
        all_data = json.loads(response.text)
        session.headers.update({
            "x-verkada-auth": all_data['token'],
        })
        return session

    logging.error("Verkada authentication error")
    logging.error(response.text)
    logging.error("Cannot continue")
    exit(1)

# Generic helper for Verakada API endpoints
def _get(session: requests.Session, endpoint: str) -> requests.Response:
    logging.debug(f"GET Verkada API endpoint: {endpoint}")
    response = session.get(f"https://api.verkada.com/{endpoint}")

    st = response.status_code
    if st >= 200 and st < 300:
        return response

    logging.error("Verkada API error")
    logging.error(response.text)
    logging.error("Cannot continue")
    exit(1)

def _get_unix_timestamp(time_delta: int=1) -> str:
  yesterday = datetime.date.today() - datetime.timedelta(time_delta)
  yesterday_dt = datetime.datetime.combine(yesterday, datetime.time.min, tzinfo=datetime.timezone.utc)
  unix_time = int(yesterday_dt.timestamp())
  return unix_time


def get_access_events(session: requests.Session):
    logging.info("Downloading a list of access events")

    start_time = _get_unix_timestamp()
    endpoint = f"events/v1/access?start_time={start_time}&page_size=100"
    response = _get(session, endpoint)
    all_data = json.loads(response.text)
    return all_data
