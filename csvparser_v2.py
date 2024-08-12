import re
import os

# Specify the folder path that contains the log files
log_folder = '/workspaces/YSBoK/CSVLogs'

# Initialize an empty list to store the normalized log entries
normalized_log = []

# Iterate over the files in the log folder
for filename in os.listdir(log_folder):
    # Check if the file is a log file (e.g. has a .log extension)
    if filename.endswith('.log'):
        # Open the log file and read its contents
        with open(os.path.join(log_folder, filename), 'r') as file:
            # Split the log into lines
            lines = file.readlines()

            # Initialize an empty string to store the current log entry
            current_entry = ''

            # Iterate over the lines
            for line in lines:
                # Check if the line starts with a timestamp
                if re.match(r'timestamp=', line):
                    # If the current entry is not empty, add it to the normalized log
                    if current_entry:
                        normalized_log.append(current_entry.strip())
                    # Reset the current entry with the new timestamp line
                    current_entry = line
                else:
                    # If the line does not start with a timestamp, append it to the current entry
                    current_entry += ' ' + line

            # Add the last entry to the normalized log
            if current_entry:
                normalized_log.append(current_entry.strip())

# Print the normalized log
for entry in normalized_log:
    print(entry)