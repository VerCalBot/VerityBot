import requests
import time
import logging

def send_bulk_ndjson(bulk_ndjson: str,ca_path: str = "/certs/ca.crt", user_name: str = "elastic", password: str = None, attempts: int = 5, sleep_sec: int = 5):

    if not bulk_ndjson.strip():
        logging.info("Bulk ndjson was empty, no data sent to ES")
        return

    for attempt in range(1, attempts + 1):
        try:
            # Sends data to Bulk endpoint _bulk and content type is specified to ndjson
            response = requests.post(
                url="https://elasticsearch:9200/_bulk",
                headers={"Content-Type": "application/x-ndjson"},
                verify=ca_path,
                auth=(user_name, password),
                data=bulk_ndjson,
                timeout=30)

            # Indicates what Status code is returned
            logging.info(f"Attempt {attempt}, HTTP: {response.status_code}")

            # Raises HTTP errors
            response.raise_for_status()

            # format reponse data into Json format
            result = response.json()

            # indicates if errors occured during indexing of bulk ndjson
            if result.get("errors"):
                logging.error("Bulk indexing finished with errors")
            else:
                logging.info("Bulk indexing succeeded without errors")

            return

        except requests.RequestException as error:
            logging.error(f"Attempt {attempt} : ElasticSearch failed to receive Bulk NDJSON {error}")

            if attempt < attempts :
                time.sleep(sleep_sec)

    raise RuntimeError("ElasticSearch failed to receive Bulk NDJSON after all attempts")

# Waits for ElasticSearch to repond. Note assumes CA is mounted at /certs/ca.crt and that DNS name is elasticsearch
def wait_for_elasticsearch(url : str = "https://elasticsearch:9200", ca_path: str = "/certs/ca.crt", user_name: str = "elastic", password: str = None, attempts: int = 30, sleep_sec: int = 5) -> bool:

    for attempt in range(1, attempts + 1):
        try:
            response = requests.get(
                    url,
                    verify= ca_path,
                    auth=(user_name, password),
                    timeout=5
                )

            logging.info(f"Attempt {attempt}, HTTP: {response.status_code}")

            # Checks to see if request is successful with authentification
            if response.status_code == 200:
                logging.info("ElasticSearch is ready")
                return True

        except requests.RequestException as error:
            logging.info(f"Attempt {attempt} : ElasticSearch is not ready yet {error}")

        if attempt < attempts :
            time.sleep(sleep_sec)

    raise RuntimeError("ElasticSearch did not become ready")

# Sends request to return latest timestamp from index
def get_latest_timestamp(ca_path: str = "/certs/ca.crt", user_name: str = "elastic", password: str = None, attempts: int = 30, sleep_sec: int = 5) -> str | None:

    # retries if errors occur such as status code 503
    for attempt in range(1, attempts + 1):
        try:
            # Sends request to receive latest timestamp from verkada events
            response = requests.get(
                url="https://elasticsearch:9200/verkada_events/_search",
                verify=ca_path,
                auth=(user_name, password),
                json={
                    "sort" : [
                        {"timestamp" : {"order" : "desc"}}
                    ],
                "size" : 1
                },
                timeout=30)
            
            logging.info(f"Attempt {attempt}, HTTP: {response.status_code}")

            # Checks to see if request is successful
            if response.status_code == 200:
                 # format reponse data into Json format
                result = response.json()

                # if json contains no documents return None, else return timestamp
                hits = result.get("hits", {}).get("hits", [])
                if hits:
                    logging.info("TimeStamp received")
                    return hits[0]["_source"]["timestamp"]
                else:
                    logging.info("Empty Index, No Timestamp received")
                    return None
            
            elif response.status_code == 404:
                return None

        except requests.RequestException as error:
                logging.error(f"ElasticSearch failed timestamp request {error}")

        if attempt < attempts :
            time.sleep(sleep_sec)

    raise RuntimeError("ElasticsSearch failed to get timestamp after all attempts.")