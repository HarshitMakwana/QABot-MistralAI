import json

with open('configs/config.json', 'r') as f:
    config_param = json.load(f)

with open('data/data.json', 'r') as f:
    data = json.load(f)

new_dict = dict()
for each in data:
    new_dict[each.get('index')] = [each.get('short_list'),each.get('content')]
    
model = config_param.get("model")
api_key = config_param.get("api_key")