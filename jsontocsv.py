import json
import csv
from dateutil import parser
import pytz

# Load the JSON log file
with open('/workspaces/YSBoK/Output/output.json') as f:
    log_data = json.load(f)

# Get the unique keys from the log data
keys = set()
for entry in log_data:
    keys.update(entry.keys())

# Create a CSV writer
with open('/workspaces/YSBoK/Output/output.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)

    # Write the header row
    header = ['ID', 'Timestamp (YYYY-MM-DD)', 'Timezone', 'Message']
    for key in sorted(list(keys - {'id', 'timestamp', 'message'})):
        header.append(key.replace('field_', 'Field_').title())
    writer.writerow(header)

    #Create a timezone mapping to align timezones
    timezone_map = {
        'PDT': pytz.timezone('US/Pacific'),
        'EST': pytz.timezone('US/Eastern'),
    }

    # Write the data rows
    for entry in sorted(log_data, key=lambda x: int(x['id'])):
        timestamp_original = entry['timestamp']
        parts = timestamp_original.split()
        # Select the Timezone abbreviation from the original timestamp after splitting
        timezone_abbreviation = parts[-2]
        timezone = timezone_map.get(timezone_abbreviation)
        if timezone:
            dt = parser.parse(timestamp_original, tzinfos={timezone_abbreviation: timezone})
        else:
            dt = parser.parse(timestamp_original, fuzzy=True)
        # process rimezone in YYY-MM-DD format
        timestamp_formatted = dt.strftime('%Y-%m-%d')
        row = [entry['id'], timestamp_formatted, timezone_abbreviation, entry['message']]
        for key in sorted(list(keys - {'id', 'timestamp', 'message'})):
            row.append(entry.get(key, ''))
        writer.writerow(row)