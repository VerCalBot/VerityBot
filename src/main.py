from dotenv import load_dotenv
from db.Elastic import Elastic
import Application
import Verkada
import Utils
import argparse
import os
import logging

ELASTIC_API_KEY="V1g1aUxwd0JHVWJ6dTlfU044Sm46dnJZRHlVbDhfc0p4VFZ0bVkxR2RKZw=="
ELASTIC_HOST="https://my-elasticsearch-project-ce839c.es.us-central1.gcp.elastic.cloud:443"

def main():
    load_dotenv()
    Application.init()


if __name__ == '__main__':
    main()
    # instance = Elastic()
    # instance.connect(elastic_host=ELASTIC_HOST, elastic_api_key=ELASTIC_API_KEY)
