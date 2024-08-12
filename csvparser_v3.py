import os
import re
import csv

# Set the folder path and the output file path
folder_path = '/workspaces/YSBoK/CSVLogs'
output_file_path = '/workspaces/YSBoK/Output/normalized_logs.csv'

# Open the output file in write mode
with open(output_file_path, 'w', newline='') as output_file:
    writer = csv.writer(output_file)
    writer.writerow(['ID', 'Timestamp (YYYY-MM-DD)', 'Message', 'Field_1', 'Field_2', 'Field_3', 'Field_4', 'Field_5', 'Field_6', 'Field_9'])

    log_entries = []
    # Iterate over all files in the folder
    for filename in os.listdir(folder_path):
        # Open the file in read mode
        with open(os.path.join(folder_path, filename), 'r') as file:
            # Initialize an empty string to build the current log entry
            current_log_entry = ''
            # Iterate over all lines in the file
            for line in file:
                # Strip the line of leading and trailing whitespace
                line = line.strip()
                # If the line starts with a timestamp, it's a new log entry
                if re.match(r'timestamp="[^"]+"', line):
                    # If we're not at the start of the file, write the previous log entry
                    if current_log_entry:
                        fields = current_log_entry.split()
                        timestamp = fields[0].replace('timestamp="', '').replace('"', '').split()[0]
                        message = fields[1].replace('message="', '').replace('"', '')
                        id = fields[2].replace('id=', '')
                        fields_dict = {}
                        for field in fields[3:]:
                            key, value = field.replace('"', '').split('=')
                            fields_dict[key] = value
                        log_entries.append([id, timestamp, message, fields_dict.get('field_1', ''), fields_dict.get('field_2', ''), fields_dict.get('field_3', ''), fields_dict.get('field_4', ''), fields_dict.get('field_5', ''), fields_dict.get('field_6', ''), fields_dict.get('field_9', '')])
                    # Start a new log entry
                    current_log_entry = line
                else:
                    # If the line does not start with a timestamp, append it to the current log entry
                    current_log_entry += ' ' + line
            # Write the last log entry to the output file
            if current_log_entry:
                fields = current_log_entry.split()
                timestamp = fields[0].replace('timestamp="', '').replace('"', '').split()[0]
                message = fields[1].replace('message="', '').replace('"', '')
                id = fields[2].replace('id=', '')
                fields_dict = {}
                for field in fields[3:]:
                    key, value = field.replace('"', '').split('=')
                    fields_dict[key] = value
                log_entries.append([id, timestamp, message, fields_dict.get('field_1', ''), fields_dict.get('field_2', ''), fields_dict.get('field_3', ''), fields_dict.get('field_4', ''), fields_dict.get('field_5', ''), fields_dict.get('field_6', ''), fields_dict.get('field_9', '')])

    # Write the log entries to the CSV file
    log_entries.sort(key=lambda x: int(x[0]))
    writer.writerows(log_entries)