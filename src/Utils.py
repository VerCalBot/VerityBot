import json
from pathlib import Path

# Source - https://stackoverflow.com/a/53465812
# Posted by RikH, modified by community. See post 'Timeline' for change history
# Retrieved 2026-03-18, License - CC BY-SA 4.0
def get_project_root() -> Path:
    return Path(__file__).parent.parent

def pretty_print_json(data):
    pretty_json_string = json.dumps(data, indent=4, sort_keys=True)
    print(pretty_json_string)
