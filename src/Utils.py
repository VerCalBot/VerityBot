import json
import time
import requests

def pretty_print_json(data):
    pretty_json_string = json.dumps(data, indent=4, sort_keys=True)
    print(pretty_json_string)

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