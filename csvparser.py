import csv
import re

# Define the log file path and the output CSV file path
log_file_path = '/workspaces/YSBoK/CSVLogs/Security Response_ SecurityEngineering- Raw Data'
output_csv_path = '/workspaces/YSBoK/Logs/csvfile.csv'

# Define the regular expression pattern to extract log data
pattern = r'timestamp="([^"]+)"\s*message="([^"]+)"\s*id=(\d+)\s*(.*)'

# Open the log file and the output CSV file
with open(log_file_path, 'r') as log_file, open(output_csv_path, 'w', newline='') as csv_file:
    # Create a CSV writer
    csv_writer = csv.writer(csv_file)

    # Write the header row
    csv_writer.writerow(['Timestamp', 'Message', 'ID', 'Field_1', 'Field_6'])

    # Initialize an empty dictionary to store the log data
    log_data = {}

    # Iterate over each line in the log file
    for line in log_file:
        # Strip whitespace and remove trailing newline characters
        line = line.strip()

        # Check if the line contains a key-value pair
        if '=' in line:
            # Extract the key and value
            key, value = line.split('=', 1)
            key = key.strip()
            value = value.strip().strip('"')

            # Add the key-value pair to the log data dictionary
            log_data[key] = value
        else:
            # If the line doesn't contain a key-value pair, it's a new log entry
            if log_data:
                # Extract the log data from the dictionary
                timestamp = log_data.get('timestamp')
                message = log_data.get('message')
                id = log_data.get('id')
                field_1 = log_data.get('field_1')
                field_6 = log_data.get('field_6')

                # Write the log data to the CSV file
                csv_writer.writerow([timestamp, message, id, field_1, field_6])

                # Reset the log data dictionary
                log_data = {}

    # Write any remaining log data to the CSV file
    if log_data:
        timestamp = log_data.get('timestamp')
        message = log_data.get('message')
        id = log_data.get('id')
        field_1 = log_data.get('field_1')
        field_6 = log_data.get('field_6')
        csv_writer.writerow([timestamp, message, id, field_1, field_6])