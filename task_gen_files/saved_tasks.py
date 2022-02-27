import json
data = {"1": []}
with open("saved_tasks.json", "w+") as f:
    json.dump(data, f)