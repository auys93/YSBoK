import os
import json
from collections import Counter
import pycountry

# Folder containing log files (replace with your folder path)
log_folder = "/workspaces/YSBoK/Logs"

# Standard HTTP request methods
standard_methods = {"GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS", "PATCH"}

def process_log_entry(log_entry, unique_ips, country_counts):
    try:
        log_data = json.loads(log_entry)
        client_ip = log_data.get("ClientIP")
        country_code = log_data.get("ClientCountry", "").upper()
        request_bytes = log_data.get("ClientRequestBytes", 0)
        request_method = log_data.get("ClientRequestMethod", "").upper()

        if client_ip and request_bytes != 0 and request_method in standard_methods:
            unique_ips.add(client_ip)
        if country_code:
            try:
                country_name = pycountry.countries.get(alpha_2=country_code).name
                country_counts[country_name] += 1
            except AttributeError:
                print(f"Unknown country code: {country_code}")
        
    except json.JSONDecodeError:
        print("Error: Invalid log entry format")
        print(f"Raw Log Entry: {log_entry}")

def process_log_files(folder_path):
    total_entries = 0
    unique_ips = set()
    country_counts = Counter()

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            with open(file_path, "r") as log_file:
                log_entries = [line.strip() for line in log_file.readlines() if line.strip() and not line.strip().startswith("#")]
                for entry in log_entries:
                    process_log_entry(entry, unique_ips, country_counts)
                    total_entries += 1

    print("----Log Analyst Report----")
    print(f"\nTotal log entries: {total_entries}")
    print(f"\nTotal unique client IP addresses making requests: {len(unique_ips)}")
    print("\nUnique IP addresses:")
    for ip in unique_ips:
        print(ip)

    print("\nMost common country names:")
    for name, count in country_counts.most_common():
        print(f"{name}: {count}")

if __name__ == "__main__":
    process_log_files(log_folder)
