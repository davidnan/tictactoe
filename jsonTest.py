import json

with open("serverInf.json") as f:
	data = json.load(f)

print(data['ip'])
