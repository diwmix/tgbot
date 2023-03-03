import json

with open('result.json', 'r', encoding='utf-8') as file:
  data = json.load(file)

data = [{'card_value': 'Ні', **entry} for entry in data]

with open('result_3.json', 'w', encoding='utf-8') as file:
  json.dump(data, file, indent=2, ensure_ascii=False)