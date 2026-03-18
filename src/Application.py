import logging
import CLI
import ElasticSearch
import Utils

from dotenv import load_dotenv
from Verkada import VerkadaContext
from ConfigReader import config

def init():
    load_dotenv()
    args = CLI.setup_cli()
    time_delta = int(config['Verkada']['TIME_DELTA_RECURRING'])
    verkada = VerkadaContext(time_delta=time_delta)

    logging.info(f"Initializing Verkada service")
    verkada.login(args.verkada_api_key)

    if ElasticSearch.wait_for_elasticsearch():
        while verkada.next_page_available():
            verkada.get_next_page()
            if not verkada.is_eor_page():
                ElasticSearch.send_bulk_ndjson(verkada.current_page_ndjson_bulk(), password=args.elastic_password)
    else:
        logging.error("ElasticSearch connection timed out")
