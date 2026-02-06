from dotenv import load_dotenv
import Verkada
import Utils
import argparse
import os
import logging

def setup_logging(args: argparse.Namespace):
    level = logging.WARNING
    if args.verbose:
        level = logging.INFO
    if args.debug:
        level = logging.DEBUG

    logging.basicConfig(level=level)

def setup_cli() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    default_val = os.environ.get("VERKADA_API_KEY", None)
    required_val = False if default_val else True

    parser.add_argument('--verbose', action=argparse.BooleanOptionalAction)
    parser.add_argument('--debug', action=argparse.BooleanOptionalAction)
    parser.add_argument('--verkada-api-key',
                        required=required_val,
                        default=default_val,
                        help='Verkada API key (defaults to VERKADA_API_KEY env var, if set)')

    args = parser.parse_args()

    setup_logging(args)

    return args

def main():

    # Load environment variables from the .env file (if present)
    # Docker already load environment variables with the etl container, override specifies if env variables are already loaded then dont run.
    load_dotenv(override=False)

    args = setup_cli()
    logging.info(f"Initializing Verkada service")

    verkada_service = Verkada.login(args)
    verkada_events = Verkada.get_access_events(verkada_service)

    # print the first entry in our response
    # keeping this in for now as a sanity check
    Utils.pretty_print_json(verkada_events['events'][0])

if __name__ == '__main__':
    main()