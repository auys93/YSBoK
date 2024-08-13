import json
import re

# Read the log file
with open('/workspaces/YSBoK/Output/normalized_logs', 'r') as f:
    log_lines = [line.strip() for line in f.readlines()]

# Parse the log lines into a list of dictionaries
log_data = []
for line in log_lines:
    log_dict = {}
    # Use regex to parse the key and values
    pairs = re.findall(r'(\w+)=(?:"([^"]*)"|(\S+))', line)
    for key, value1, value2 in pairs:
        log_dict[key] = value1 or value2
    log_data.append(log_dict)

# Write the log data to a JSON file
with open('/workspaces/YSBoK/Output/output.json', 'w') as f:
    json.dump(log_data, f, indent=4)