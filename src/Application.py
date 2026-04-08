import logging
import CLI
import ElasticSearch
import os

from Verkada import VerkadaContext
from ConfigReader import config
from datetime import datetime, date, timedelta

ELASTIC_PASSWORD = os.environ.get("ELASTIC_PASSWORD")
if not ELASTIC_PASSWORD:
    print("ERROR: ELASTIC_PASSWORD has not been set, exiting...")
    exit(1)

def init():
    args = CLI.setup_cli()

    days_back = int(config['Verkada']['TIME_DELTA_INSTALLATION'])
    start_timestamp = None

    last_timestamp = ElasticSearch.get_latest_timestamp(password=str(ELASTIC_PASSWORD))

    # if no timestamp is found then time_delta remains installation default
    if last_timestamp:
        # Changes timestamp format to +00:00, then converts it to datetime, then drops time
        last_timestamp_dt = datetime.fromisoformat(last_timestamp.replace("Z", "+00:00"))
        # Calculates datetime since last event
        start_timestamp = last_timestamp_dt - timedelta(minutes=5)

    verkada = VerkadaContext(time_delta=days_back, start_timestamp=start_timestamp)

    logging.info("Initializing Verkada service")
    verkada.login(args.verkada_api_key)
    user_title_dict = verkada.build_user_employment_title_dict()

    # Waits to ensure ES is ready to receive data
    if ElasticSearch.wait_for_elasticsearch(password=str(ELASTIC_PASSWORD)):
        # will loop until there are no more pages available
        while verkada.next_page_available():
            verkada.get_next_page()

            # Only sends data if current pages is not empty ndjson
            ndjson = verkada.current_page_ndjson_bulk(user_title_dict)
            if ndjson.strip():
                ElasticSearch.send_bulk_ndjson(ndjson, password=str(ELASTIC_PASSWORD))

            # Logs when we reached last page
            if verkada.is_eor_page():
                logging.info("Finished all pages")

    else:
        logging.error("ElasticSearch connection timed out")
