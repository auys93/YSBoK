import pandas as pd
import json

# Load JSON data
with open('find_martin_events.json') as jsonlog:
    logger = json.load(jsonlog)

# Extract Hits List
data = logger['data']

# Store data
expanded_data = []

# Iterate over data
for logvalues in data:
    # Extract initial values
    sort_value = logvalues['sort'][0]  # Get the first element of the sort array
    # _timestamp = pd.to_datetime(logvalues['_source']['@timestamp']).strftime('%d %b %Y %H:%M:%S.%f')
    _timestamp = logvalues['_source']['@timestamp']
    _index = logvalues['_index']
    _id = logvalues['_id']
    
    expanded_source = {}

    # Flatten the JSON structure from _source
    _source = logvalues['_source']
    for jsonKey, jsonValue in _source.items():
        if isinstance(jsonValue, dict):
            for nestKey, nestValue in jsonValue.items():
                if isinstance(nestValue, dict):
                    for nestKeyL2, nestValueL2 in nestValue.items():
                        expanded_source[f"{jsonKey}.{nestKey}.{nestKeyL2}"] = nestValueL2
                else:
                    expanded_source[f"{jsonKey}.{nestKey}"] = nestValue
        else:
            expanded_source[jsonKey] = jsonValue
            
    # Create a dictionary for the CSV row with initial values first
    csvRow = {
        'timestamp (UTC)': _timestamp,
        'sort': sort_value,
        '_index': _index,
        '_id': _id
    }
    
    # Update with expanded source fields
    csvRow.update(expanded_source)
    
    # Append the row to the list
    expanded_data.append(csvRow)

# Create a DataFrame from the list of dictionaries
df = pd.DataFrame(expanded_data)

# Define the order of columns to ensure initial values come first
columns_order = ['timestamp (UTC)', 'sort', '_index', '_id'] + [col for col in df.columns if col not in ['timestamp (UTC)', 'sort', '_index', '_id']]
df = df[columns_order]

# Save DataFrame to CSV file without index
df.to_csv('logAnalysis.csv', index=False)