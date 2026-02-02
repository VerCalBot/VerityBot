from Verkada import VerkadaContext
import Utils
import logging

def init(verkada_api_key: str):
    logging.info(f"Initializing Verkada service")
    current_page = {}

    instance = VerkadaContext(time_delta=1)
    instance.login(verkada_api_key)

    while instance.next_page_available():
        current_page = instance.get_next_page()
        if len(current_page['events']) > 0:
            ## pipe data to elasticsearch api, for now we're just printing
            Utils.pretty_print_json(current_page['events'][0])
