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
                if re.match(r'\w{3} \w{3} \d{2} \d{2}:\d{2}:\d{2} \w{3} \d{4}', line):
                    # If we're not at the start of the file, write the previous log entry
                    if current_log_entry:
                        output_file.write(current_log_entry)
                    # Start a new log entry
                    current_log_entry = line + '\n'
                else:
                    # If the line does not start with a timestamp, append it to the current log entry
                    current_log_entry += ' ' + line
            # Write the last log entry to the output file
            if current_log_entry:
                output_file.write(current_log_entry)