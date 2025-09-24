import json

def parse_config():
    with open('config.json', 'r') as f:
        return_value = json.loads(f.read())
    f.close()
    return return_value