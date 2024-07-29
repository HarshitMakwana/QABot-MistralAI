import json

with open('configs/config.json', 'r') as f:
    config_param = json.load(f)

with open('data/data.json', 'r') as f:
    data = json.load(f)

model = config_param.get("model")
api_key = config_param.get("api_key")