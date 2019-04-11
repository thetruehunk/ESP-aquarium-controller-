

import json
filename = 'config.json'
with open(filename, 'r') as f:
    data = json.load(f)

print(data["light_relay_start"][1])
# int(start_time[0]), int(stop_time[1])