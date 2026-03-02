import logging
import CLI
import Utils

from Verkada import VerkadaContext
from Pipeline import Pipeline

def init():
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
            print(verkada.current_page_ndjson())

            # To format in regular JSON instead of NDJSON, uncomment the line below and comment out the print statement above
            #Utils.pretty_print_json(verkada.current_page()['events'][0])

