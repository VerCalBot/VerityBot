import requests
import time

def send_bulk_ndjson(bulk_ndjson: str,ca_path: str = "/certs/ca.crt", user_name: str = "elastic", password: str = None):

    # Sends data to Bulk endpoint _bulk and content type is specified to ndjson
    response = requests.post(
        url="https://elasticsearch:9200/_bulk",
        headers={"Content-Type": "application/x-ndjson"},
        verify=ca_path,
        auth=(user_name, password),
        data=bulk_ndjson,
        timeout=30)

    # Indicates what Status code is returned
    print("HTTP status:", response.status_code)

    # Raises HTTP errors
    response.raise_for_status()

    # format reponse data into Json format
    result = response.json()

    # indicates if errors occured during indexing of bulk ndjson
    if result.get("errors"):
        print("Bulk indexing finished with errors")
    else:
        print("Bulk indexing succeeded without errors")

# Waits for ElasticSearch to repond. Note assumes CA is mounted at /certs/ca.crt and that DNS name is elasticsearch
def wait_for_elasticsearch(url : str = "https://elasticsearch:9200", ca_path: str = "/certs/ca.crt", attempts: int = 30, sleep_sec: int = 5) -> bool:

    for attempt in range(1, attempts + 1):
        try:
            response = requests.get(
                    url,
                    verify= ca_path,
                    timeout=5
                )

            print(f"Attempt {attempt}, HTTP: {response.status_code}")

            # Checks to see if request is successful on transport layer
            if response.status_code in (200,401):
                print("ElasticSearch is ready")
                return True

        except requests.RequestException as error:
            print(f"Attempt {attempt} : ElasticSearch is not ready yet {error}")

        time.sleep(sleep_sec)

    raise RuntimeError("ElasticsSarch did not become ready")
