import logging
import CLI
import ElasticSearch
import os
import Utils

from dotenv import load_dotenv
from Verkada import VerkadaContext
from ConfigReader import config
from datetime import datetime, date

ELASTIC_PASSWORD = os.environ.get("ELASTIC_PASSWORD")
if not ELASTIC_PASSWORD:
    logging.error("ELASTIC_PASSWORD has not been set")
    exit(1)

def init():
    args = CLI.setup_cli()

    days_back = int(config['Verkada']['TIME_DELTA_INSTALLATION'])
    last_timestamp = ElasticSearch.get_latest_timestamp(password=str(ELASTIC_PASSWORD))
    # if no timestamp is found then time_delta remains installation default
    if last_timestamp:
        # Changes timestamp format to +00:00, then converts it to datetime, then drops time
        last_timestamp_date = datetime.fromisoformat(last_timestamp.replace("Z", "+00:00")).date()
        # Calculates number of days since last event
        days_back = max((date.today() - last_timestamp_date).days, 1)

    verkada = VerkadaContext(time_delta=days_back)

    logging.info(f"Initializing Verkada service")
    verkada.login(args.verkada_api_key)

    if ElasticSearch.wait_for_elasticsearch(password=str(ELASTIC_PASSWORD)):
        while verkada.next_page_available():
            verkada.get_next_page()
            if not verkada.is_eor_page():
                ElasticSearch.send_bulk_ndjson(verkada.current_page_ndjson_bulk(), password=str(ELASTIC_PASSWORD))
    else:
        logging.error("ElasticSearch connection timed out")
