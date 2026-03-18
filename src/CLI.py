import argparse
import os
import logging

def _setup_logging(args: argparse.Namespace):
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
    _setup_logging(args)

    return args
