import logging
import CLI
import ElasticSearch
import Utils

from dotenv import load_dotenv
from Verkada import VerkadaContext

def init():
    load_dotenv()
    args = CLI.setup_cli()
    verkada = VerkadaContext(time_delta=1)

    logging.info(f"Initializing Verkada service")
    verkada.login(args.verkada_api_key)

    if ElasticSearch.wait_for_elasticsearch():
        while verkada.next_page_available():
            verkada.get_next_page()
            if not verkada.is_eor_page():
                ElasticSearch.send_bulk_ndjson(verkada.current_page_ndjson_bulk(), password=args.elastic_password)
    else:
        logging.error("ElasticSearch connection timed out")

    # while verkada.next_page_available():
    #         current_page = verkada.get_next_page()
    #         if not verkada.is_eor_page():
    #             # ElasticSearch.send_bulk_ndjson(verkada.current_page_ndjson_bulk(), password=args.elastic_password)
    #             Utils.pretty_print_json(current_page['events'])
    #             break
