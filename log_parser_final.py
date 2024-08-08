import os
import json
from collections import Counter
import pycountry
import pandas as pd
from datetime import datetime, timedelta

# Folder containing log files (replace with your folder path)
log_folder = "/workspaces/YSBoK/Logs"
output_file = "/workspaces/YSBoK/Output/AnalystReport"

# Standard HTTP request methods
standard_methods = {"GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS", "PATCH"}

def process_log_entry(log_entry, counters):
    try:
        log_data = json.loads(log_entry)
        client_ip = log_data.get("ClientIP")
        country_code = log_data.get("ClientCountry", "")
        request_bytes = log_data.get("ClientRequestBytes", 0)
        request_method = log_data.get("ClientRequestMethod", "").upper()
        user_agent = log_data.get("ClientRequestUserAgent", "")
        http_response_code = log_data.get("ClientRequestMethod", "")
        edge_response_status = log_data.get("EdgeResponseStatus", "")
        security_level = log_data.get("SecurityLevel", "")
        
        # Store data for anomaly analysis
        counters['log_entries'].append({
            'timestamp': log_data.get("EdgeStartTimestamp", ""),
            'country': log_data.get("ClientCountry", ""),
            'client_ip': log_data.get("ClientIP", ""),
            'client_request_uri': log_data.get("ClientRequestURI", ""),
            'user-agent': log_data.get("ClientRequestUserAgent", ""),
        })

        if client_ip and request_bytes != 0 and request_method in standard_methods:
            counters['unique_ips'][client_ip] += 1

        if country_code:
            try:
                country_name = pycountry.countries.get(alpha_2=country_code).name
                counters['country_counts'][country_name] += 1
            except AttributeError:
                print(f"Unknown country code: {country_code}")

        if user_agent:
            counters['unique_user_agents'].add(user_agent)
            counters['user_agent_counts'][user_agent] += 1
        else:
            counters['unique_user_agents'].add("EMPTY_USER_AGENT")
            counters['user_agent_counts']["EMPTY_USER_AGENT"] += 1

        # Count HTTP response codes
        if http_response_code:
            counters['http_response_counts'][http_response_code] += 1
        else:
            counters['http_response_counts']["EMPTY_RESPONSE_CODE"] += 1

        # Count EdgeResponseStatus codes
        if edge_response_status:
            counters['edge_response_counts'][edge_response_status] += 1
        else:
            counters['edge_response_counts']["EMPTY_RESPONSE"] += 1

        if security_level:
            counters['security_level_counts'][security_level] += 1
        else:
            counters['security_level_counts']["EMPTY_SECURITY_LEVEL"] += 1

    except json.JSONDecodeError:
        print("Error: Invalid log entry format")
        print(f"Raw Log Entry: {log_entry}")

def process_log_files(folder_path, output_file):
    counters = {
        'log_entries': [],
        'unique_ips': Counter(),
        'country_counts': Counter(),
        'unique_user_agents': set(),
        'user_agent_counts': Counter(),
        'http_response_counts': Counter(),
        'edge_response_counts': Counter(),
        'security_level_counts': Counter()
    }

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            with open(file_path, "r") as log_file:
                log_entries = [line.strip() for line in log_file.readlines() if line.strip() and line.strip().startswith("{")]
                for entry in log_entries:
                    process_log_entry(entry, counters)

    generate_report(counters, output_file)

def generate_report(counters, output_file):
    with open(output_file, "w") as report_file:
        report_file.write("----Log Analyst Report----\n")
        report_file.write(f"\nTotal log entries: {len(counters['log_entries'])}\n")
        report_file.write(f"\nTotal unique client IP addresses making requests: {len(counters['unique_ips'])}\n")
        report_file.write("\nUnique IP addresses:\n")
        for ip, count in counters['unique_ips'].items():
            report_file.write(f"{ip}: {count}\n")

        report_file.write("\nMost common country names:\n")
        for name, count in counters['country_counts'].most_common():
            report_file.write(f"{name}: {count}\n")

        report_file.write(f"\nTotal unique user agents: {len(counters['unique_user_agents'])}\n")
        report_file.write("\nTop User Agents:\n")
        for ua, count in counters['user_agent_counts'].most_common():
            report_file.write(f"{ua}: {count}\n")

        report_file.write("\nHTTP Response Code Counts:\n")
        for code, count in counters['http_response_counts'].items():
            report_file.write(f"{code}: {count}\n")

        report_file.write("\nEdgeResponseStatus Code Counts:\n")
        for response, count in counters['edge_response_counts'].items():
            report_file.write(f"{response}: {count}\n")
        report_file.write(f"Total number of unique response codes: {len(counters['edge_response_counts'])}\n")

        report_file.write("\nSecurity Level Counts:\n")
        for seclvl, count in counters['security_level_counts'].items():
            report_file.write(f"{seclvl}: {count}\n")
        report_file.write(f"Total number of unique security level values: {len(counters['security_level_counts'])}\n")

        log_df = pd.DataFrame(counters['log_entries'])
        anomalies = identify_anomalies(log_df)
        report_file.write('\nAnomalies detected:\n')
        for anomaly in anomalies:
            for key, value in anomaly.items():
                report_file.write(f"{key}: {value}\n")
            report_file.write("\n")  # Adds a newline after each dictionary

    print(f"Report generated and saved to {output_file}")

# def generate_report(counters):
#     report = "----Log Analyst Report----\n"
#     report += f"\nTotal log entries: {len(counters['log_entries'])}"
#     report += f"\nTotal unique client IP addresses making requests: {len(counters['unique_ips'])}"
#     report += "\nUnique IP addresses:\n"
#     for ip, count in counters['unique_ips'].items():
#         report += f"{ip}: {count}\n"

#     report += "\nMost common country names:\n"
#     for name, count in counters['country_counts'].most_common():
#         report += f"{name}: {count}\n"

#     report += f"\nTotal unique user agents: {len(counters['unique_user_agents'])}"
#     report += "\nTop User Agents:\n"
#     for ua, count in counters['user_agent_counts'].most_common():
#         report += f"{ua}: {count}\n"

#     report += "\nHTTP Response Code Counts:\n"
#     for code, count in counters['http_response_counts'].items():
#         report += f"{code}: {count}\n"

#     report += "\nEdgeResponseStatus Code Counts:\n"
#     for response, count in counters['edge_response_counts'].items():
#         report += f"{response}: {count}\n"
#     report += f"Total number of unique response codes: {len(counters['edge_response_counts'])}\n"

#     report += "\nSecurity Level Counts:\n"
#     for seclvl, count in counters['security_level_counts'].items():
#         report += f"{seclvl}: {count}\n"
#     report += f"Total number of unique security level values: {len(counters['security_level_counts'])}\n"

#     log_df = pd.DataFrame(counters['log_entries'])
#     anomalies = identify_anomalies(log_df)
#     report += '\nAnomalies detected:\n'
#     for anomaly in anomalies:
#         for key, value in anomaly.items():
#             report += f"{key}: {value}\n"
#         report += "\n"  # Adds a newline after each dictionary

#     return report

def identify_anomalies(df):
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Sort by timestamp
    df = df.sort_values(by='timestamp')

    # Initialize variables to track anomalies
    anomalies = []
    country_ip_map = {}
    ip_uri_map = {}

    # Iterate over log entries
    for index, row in df.iterrows():
        country = row['country']
        client_ip = row['client_ip']
        timestamp = row['timestamp']

        # Check if client IP has made requests from multiple countries within a short timeframe
        if client_ip in country_ip_map:
            previous_country, previous_timestamp = country_ip_map[client_ip]
            if country != previous_country and timestamp - previous_timestamp < timedelta(minutes=15):
                anomalies.append({
                    'client_ip': client_ip,
                    'country': country,
                    'previous_country': previous_country,
                    'timestamp': timestamp,
                    'anomaly': 'Multiple countries within 15 minutes'
                })
        # Update country IP map
        country_ip_map[client_ip] = (country, timestamp)


    # Iterate over log entries
    for index, row in df.iterrows():
        client_ip = row['client_ip']
        timestamp = row['timestamp']
        client_request_uri = row['client_request_uri']

        # Check if IP has made a request with a different URI within a short timeframe (e.g., 30 seconds)
        if client_ip in ip_uri_map:
            previous_uri, previous_timestamp = ip_uri_map[client_ip]
            if client_request_uri != previous_uri and timestamp - previous_timestamp < timedelta(seconds=30):
                anomalies.append({
                    'client_ip': client_ip,
                    'timestamp': timestamp,
                    'client_request_uri': client_request_uri,
                    'anomaly': 'Change in URI within 30 seconds'
                })
        # Update IP URI map
        ip_uri_map[client_ip] = (client_request_uri, timestamp)

    return anomalies

if __name__ == "__main__":
    process_log_files(log_folder, output_file)