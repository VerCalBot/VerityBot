import logging
import CLI
import Utils

from Verkada import VerkadaContext
from interfaces.Pipeline import Pipeline

def init():
    args = CLI.setup_cli()
    ds = Pipeline()
    verkada = VerkadaContext(ds, time_delta=1)

    logging.info(f"Initializing Verkada service")
    verkada.login(args.verkada_api_key)

    while verkada.next_page_available():
        current_page = verkada.get_next_page()
        if not verkada.EOR_page():
            ## pipe data to elasticsearch api, for now we're just printing
            verkada.pipe()
            Utils.pretty_print_json(current_page)
