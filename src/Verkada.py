import json
import requests
import logging
import datetime
import Utils
import time 

# Fields to exclude from events
EXCLUDED_FIELDS: set = {
    'organization_id',
    'device_type',
    'end_timestamp',
    'entityType',
    'floorId',
    'floors',
    'inputValue',
    'rawCard',
    'scenarioInfo',
    'direction',
    'lockdownInfo',
    'auxInputId',
    'auxInputName',
}

class VerkadaContext:
    def __init__(self, time_delta: int, start_timestamp: datetime.datetime = None):
        self._current_page: dict = {}
        self._session = requests.Session()
        self._time_delta: int = time_delta
        self._next_page_token: int = -1
        self._verkada_api_key = None
        self._start_timestamp = start_timestamp
        self._access_users = None
        self._user_employment_title_dict = None

    ## Verkada API-Specific Logic
    def current_page(self) -> dict:
        return self._current_page

    def next_page_token(self) -> int:
        return self._next_page_token

    def login(self, verkada_api_key: str):
        logging.info("Logging in to Verkada")
        self._verkada_api_key = verkada_api_key
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
        logging.info(f"GET Verkada API endpoint: {endpoint}")

        max_attempts = 3

        for attempt in range(1, max_attempts + 1):

            response = self._session.get(f"https://api.verkada.com/{endpoint}")
            st = response.status_code

            # Success
            if st >= 200 and st < 300:
                return response
            
            # Session expired, Retry logic
            if st == 401 or st == 403:
                logging.warning(f"Attempt {attempt}/{max_attempts}: Session expired, renewing session")

                if self._verkada_api_key is None:
                    logging.error("No Verkada API Key found. Failed to renew session.")
                    exit(1)

                self.login(self._verkada_api_key)
                continue

            # Internal Server Error
            if st >= 500:
                logging.warning(f"Attempt {attempt}/{max_attempts} failed with {st}")
                logging.warning(response.text)
                time.sleep(1)
                continue

            # any other errors will break the loop
            break

        # All attemps failed
        logging.error(f"Failed after {max_attempts} attempts")
        logging.error("Verkada API error")
        logging.error(f"Endpoint: {endpoint}")
        logging.error(f"Status code: {st}") 
        logging.error(response.text)
        logging.error("Cannot continue")
        exit(1)

    def _get_unix_timestamp(self) -> int:

        if self._start_timestamp:
            return int(self._start_timestamp.timestamp())

        days_back = datetime.date.today() - datetime.timedelta(self._time_delta)
        days_back_dt = datetime.datetime.combine(days_back, datetime.time.min, tzinfo=datetime.timezone.utc)
        unix_time = int(days_back_dt.timestamp())
        return unix_time

    def get_next_page(self) -> dict:
        endpoint = ""
        start_time = self._get_unix_timestamp()

        if self._current_page == {}:
            endpoint += f"events/v1/access?start_time={start_time}&page_size=200"
        else:
            endpoint += f"events/v1/access?start_time={start_time}&page_token={self._next_page_token}&page_size=200"

        self._current_page = self._get(endpoint).json()
        self._next_page_token = self._current_page['next_page_token']

        return self._current_page

    # Gets all access users and stores it as an object in VerkadaContext
    def get_access_users(self) -> list[dict]:
        users = []
        next_page_token = None

        while True:
            # We can add vistors - access_users?include_visitors=false' 
            endpoint = "access/v1/access_users"
            if next_page_token:
                endpoint += f"?page_token={next_page_token}"

            response = self._get(endpoint)
            data = response.json()

            users.extend(data.get("access_members", []))

            next_page_token = data.get("next_page_token")
            if not next_page_token:
                break

        self._access_users = users
        return users

    # builds a dictionary with the key being the userId and the value being the employee title. This is stored as an object in VerkadaContext
    def build_user_employment_title_dict(self) -> dict:

        if self._user_employment_title_dict is not None:
            return self._user_employment_title_dict

        if self._access_users is None:
            self.get_access_users()

        title_dict = {}

        for user in self._access_users:
            userId = user.get("user_id")
            if userId:
                title_dict[userId] = user.get("department")

        self._user_employment_title_dict = title_dict
        return self._user_employment_title_dict

    def current_page_ndjson(self) -> str:
        return "\n".join(
            json.dumps(self._filter_event(e)) for e in self._current_page.get("events", []) if e.get('event_info', {}).get('userName')
        )

    def _filter_event(self, event: dict) -> dict:
        filtered = {}
        for k, v in event.items():
            if k not in EXCLUDED_FIELDS:
                if isinstance(v, dict):
                    filtered[k] = self._filter_event(v)
                else:
                    filtered[k] = v
        return filtered

    # Creates Bulk ndjson using event ID as "key" so all index events will be unique, and prevents duplication allowing for replacement in ElasticSearch
    # Adds employee_title to events so that we can track type of users within verkada events
    def current_page_ndjson_bulk(self) -> str:
        events = [e for e in self._current_page.get("events", []) if e.get('event_info', {}).get('userName')]
        lines = []

        if self._user_employment_title_dict is None:
            self.build_user_employment_title_dict()


        for e in events:
            userId = e.get("event_info", {}).get("userId")
            title = self._user_employment_title_dict.get(userId)
            if title:
                e["event_info"]["userInfo"]["department"] = title
            action = {
                "index":{
                    "_index":"verkada_events",
                    "_id" : e["event_id"]
                }
            }
            lines.append(json.dumps(action))
            lines.append(json.dumps(self._filter_event(e)))

        return "\n".join(lines)+ "\n"

    def print_events(self):
        while self.next_page_available():
            self.get_next_page()
            if not self.is_eor_page():
                Utils.pretty_print_json(self._current_page['events'])

    # checks if we've reached the end-of-request page
    def is_eor_page(self) -> bool:
        return self._current_page.get('next_page_token', None) == None

    def next_page_available(self) -> bool:
        return self._next_page_token != None
