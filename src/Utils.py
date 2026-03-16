import json

def pretty_print_json(data):
    pretty_json_string = json.dumps(data, indent=4, sort_keys=True)
    print(pretty_json_string)
