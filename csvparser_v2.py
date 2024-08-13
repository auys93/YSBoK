import os
import re

# Set the folder path and the output file path
folder_path = '/workspaces/YSBoK/CSVLogs'
output_file_path = '/workspaces/YSBoK/Output/normalized_logs'

# Open the output file in write mode
with open(output_file_path, 'w') as output_file:
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
                        output_file.write(current_log_entry + '\n')
                    # Start a new log entry
                    current_log_entry = line
                else:
                    # If the line does not start with a timestamp, append it to the current log entry
                    current_log_entry += ' ' + line
            # Write the last log entry to the output file
            if current_log_entry:
                output_file.write(current_log_entry + '\n')

# Normalize the log entries
with open(output_file_path, 'r') as file:
    log_entries = file.read().split('\n')

normalized_log_entries = []
for log_entry in log_entries:
    if log_entry:
        fields = log_entry.split()
        timestamp = fields[0].replace('timestamp="', '').replace('"', '')
        message = fields[1].replace('message="', '').replace('"', '')
        id = fields[2].replace('id=', '')
        fields_dict = {}
        for field in fields[3:]:
            key, value = field.replace('"', '').split('=')
            fields_dict[key] = value
        normalized_log_entry = f'{timestamp} {message} id={id} {", ".join(f"{k}={v}" for k, v in fields_dict.items())}\n'
        normalized_log_entries.append(normalized_log_entry)

# Write the normalized log entries to the output file
with open(output_file_path, 'w') as file:
    file.write(''.join(normalized_log_entries))
