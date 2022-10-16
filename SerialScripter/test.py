import json
with open("website/data/hosts.json", "r") as f:
        box_list = json.load(f)
print(str(box_list))