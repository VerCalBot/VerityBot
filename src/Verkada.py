import json
import requests
import logging
import datetime

class VerkadaContext:
    def __init__(self, time_delta: int=7):
        self._current_page: dict = {}
        self._session = requests.Session()
        self._time_delta: int = time_delta
        self._next_page_token: int = -1

    ## Verkada API-Specific Logic
    def current_page(self) -> dict:
        return self._current_page

    def next_page_token(self) -> int:
        return self._next_page_token

    def login(self, verkada_api_key: str):
        logging.info("Logging in to Verkada")
        self._session.headers.update({
            "accept": "application/json",
            "x-api-key": verkada_api_key,
        })

        response = self._session.post("https://api.verkada.com/token")
        st = response.status_code

        if st >= 200 and st < 300:
            all_data = json.loads(response.text)
            self._session.headers.update({
                "x-verkada-auth": all_data['token'],
            })
        else:
            logging.error("Verkada authentication error")
            logging.error(response.text)
            logging.error("Cannot continue")
            exit(1)

    ### Generic helper for Verakada API endpoints
    def _get(self, endpoint: str) -> requests.Response:
        logging.debug(f"GET Verkada API endpoint: {endpoint}")
        response = self._session.get(f"https://api.verkada.com/{endpoint}")

        st = response.status_code
        if st >= 200 and st < 300:
            return response
        else:
            logging.error("Verkada API error")
            logging.error(response.text)
            logging.error("Cannot continue")
            exit(1)

    def _get_unix_timestamp(self) -> int:
        yesterday = datetime.date.today() - datetime.timedelta(self._time_delta)
        yesterday_dt = datetime.datetime.combine(yesterday, datetime.time.min, tzinfo=datetime.timezone.utc)
        unix_time = int(yesterday_dt.timestamp())
        return unix_time

    def get_next_page(self) -> dict:
        endpoint = ""
        start_time = self._get_unix_timestamp()

        if self._current_page == {}:
            endpoint += f"events/v1/access?start_time={start_time}&page_size=100"
        else:
            endpoint += f"events/v1/access?start_time={start_time}&page_token={self._next_page_token}&page_size=100"

        self._current_page = self._get(endpoint).json()
        self._next_page_token = self._current_page['next_page_token']

        return self._current_page

    def next_page_available(self) -> bool:
        return self._next_page_token != None
