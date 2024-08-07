import os
import json
from collections import Counter

# Folder containing log files (replace with your folder path)
log_folder = "/workspaces/YSBoK/Logs"

# Standard HTTP request methods
standard_methods = {"GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS", "PATCH"}

# def process_log_entry(log_entry):
#     try:
#         log_data = json.loads(log_entry)
#         client_ip = log_data.get("ClientIP", "N/A")
#         response_status = log_data.get("EdgeResponseStatus", 0)
#         origin_response_time = log_data.get("OriginResponseTime", 0)
#         # Add more analysis as needed
#         print(f"Client IP: {client_ip}")
#         print(f"Response Status: {response_status}")
#         print(f"Origin Response Time (ms): {origin_response_time}")
#     except json.JSONDecodeError:
#         print("Error: Invalid log entry format")

#function to perform all analysis
def process_log_entry(log_entry, unique_ips, country_counts):
    try:
        log_data = json.loads(log_entry)
        # print(json.dumps(log_data, indent=4))
        # with open("/workspaces/YSBoK/Output/output.txt", "a") as f:
        #     f.write(json.dumps(log_data, indent=4) + "\n")
        #Code line to get all Client IPs to and to get the unique ones making the requests
        client_ip = log_data.get("ClientIP")
        country_code = log_data.get("ClientCountry", "")
        request_bytes = log_data.get("ClientRequestBytes", 0)
        request_method = log_data.get("ClientRequestMethod", "").upper()

        if client_ip and request_bytes != 0 and request_method in standard_methods:
            unique_ips.add(client_ip)
        if country_code:
                country_counts[country_code] += 1
        
    except json.JSONDecodeError:
        print("Error: Invalid log entry format")
        print(f"Raw Log Entry: {log_entry}")

# def process_log_files(folder_path):
#     for filename in os.listdir(folder_path):
#         file_path = os.path.join(folder_path, filename)
#         if os.path.isfile(file_path):
#             with open(file_path, "r") as log_file:
#                 log_entries = log_file.read().splitlines()
#                 for entry in log_entries:
#                     process_log_entry(entry)
#                     print("-" * 40)

def process_log_files(folder_path):
    total_entries = 0 #intialize count
    unique_ips = set()  # Initialize a set for unique IPs
    country_counts = Counter()

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            with open(file_path, "r") as log_file:
                log_entries = [line.strip() for line in log_file.readlines() if line.strip() and not line.strip().startswith("#")]
                for entry in log_entries:
                    process_log_entry(entry, unique_ips, country_counts)
                    total_entries += 1  # Increment the count
                    #print("-" * 40)
    print("----Log Analyst Report----")
    print(f"Total log entries: {total_entries}")
    print(f"Total unique client IP addresses making requests: {len(unique_ips)}")
    print("Unique IP addresses:")
    for ip in unique_ips:
        print(ip)
    # Print the most common country codes and their counts
    print("\nMost common country codes:")
    for code, count in country_counts.most_common():
        print(f"{code}: {count}")

if __name__ == "__main__":
    process_log_files(log_folder)
