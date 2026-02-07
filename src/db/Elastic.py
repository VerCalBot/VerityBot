from elasticsearch import Elasticsearch, AuthenticationException, ConnectionError
from Pipeline import Pipeline
import logging

class Elastic(Pipeline):
    def __init__(self, mappings: dict={}):
        self._mappings = mappings if mappings else None
        self._current_index = ""


    def connect(self, elastic_host: str, elastic_api_key: str):
        self._client = Elasticsearch(
            hosts=elastic_host,
            api_key=elastic_api_key
        )

        try:
            self._client.info()

        except AuthenticationException:
            logging.error("Elastic Cloud authentication error")
            logging.error("Cannot continue")
            exit(1)

        except ConnectionError:
            logging.error("Elastic Cloud connnection error")
            logging.error("Cannot continue")
            exit(1)

        except Exception as e:
            logging.error(f"Unexpected error while connecting to Elastic Cloud: {e}")
            exit(1)

    def add_index(self, new_index: str, update_index: bool=False):
        if not self._client.indices.exists(index=new_index):
            self._client.indices.create(index=new_index, mappings=self._mappings)

        if update_index:
            self._current_index = new_index

    def update_index(self, index_name: str):
        self.add_index(index_name, update_index=True)

    def pipe_data(self, data: dict):
        # This is where we would populate the remote database in Elasticsearch
        # for now, we'll just call the interface method
        return super().pipe_data(data)
