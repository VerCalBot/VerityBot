import Application
import Utils
import os

ELASTIC_PASSWORD = os.environ.get("ELASTIC_PASSWORD")
if not ELASTIC_PASSWORD:
    raise RuntimeError("Missing ELASTIC_PASSWORD")

def main():

    # Ensures that ElasticSearch is running before anything else is performed
    if Utils.wait_for_elasticsearch():

        # Stores the bulk ndjson data
        verkada_bulk_ndjson = Application.init()

        # This will send the bulk ndjson data to ElasticSearch
        Application.send_bulk_ndjson(bulk_ndjson=verkada_bulk_ndjson, password=ELASTIC_PASSWORD)

    else:
        print("Wait for elasticSearch failed.")
        
if __name__ == '__main__':
    main()
