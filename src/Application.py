import logging
import CLI
import Utils
import requests

from Verkada import VerkadaContext
from Pipeline import Pipeline

def init() -> str:
    args = CLI.setup_cli()
    ds = Pipeline()
    verkada = VerkadaContext(ds, time_delta=1)

    logging.info(f"Initializing Verkada service")
    verkada.login(args.verkada_api_key)


    while verkada.next_page_available():
        current_page = verkada.get_next_page()
        if not verkada.EOR_page():
            # right now, verkada's current pipeline is doing nothing
            verkada.pipe()
            return (verkada.current_page_ndjson_bulk())
            # To format in regular JSON instead of NDJSON, uncomment the line below and comment out the print statement above
            #Utils.pretty_print_json(verkada.current_page()['events'][0])

def send_bulk_ndjson(bulk_ndjson : str,ca_path: str = "/certs/ca.crt", user_name: str = "elastic", password : str = None):

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
