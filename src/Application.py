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


    # I propose this is how we iterate through request pages
    while verkada.next_page_available():
        current_page = verkada.get_next_page()
        # check for the end-of-request page
        if not verkada.EOR_page():
            # pipe data to some kind of filtering pipeline,
            # for now we're just doing nothing, then printing
            verkada.pipe()
            Utils.pretty_print_json(current_page['events'][0])
