import os
import json
from collections import Counter
import pycountry
import pandas as pd

# Folder containing log files (replace with your folder path)
log_folder = "/workspaces/YSBoK/Logs"

# Standard HTTP request methods
standard_methods = {"GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS", "PATCH"}

def process_log_entry(log_entry, unique_ips, country_counts, unique_user_agents, user_agent_counts, http_response_counts, edge_response_counts, security_level_counts, log_entries_list):
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

        # Collect log data for anomaly detection
        log_entries_list.append(log_data)

        if client_ip and request_bytes != 0 and request_method in standard_methods:
            unique_ips[client_ip] += 1

        if country_code:
            try:
                country_name = pycountry.countries.get(alpha_2=country_code).name
                country_counts[country_name] += 1
            except AttributeError:
                print(f"Unknown country code: {country_code}")

        if user_agent:
            unique_user_agents.add(user_agent)
            user_agent_counts[user_agent] += 1
        else:
            # Add an empty user agent as a unique value
            unique_user_agents.add("EMPTY_USER_AGENT")
            # Count occurrences of empty user agents
            user_agent_counts["EMPTY_USER_AGENT"] += 1

        # Count HTTP response codes
        if http_response_code:
            http_response_counts[http_response_code] += 1
        else:
            http_response_counts["EMPTY_RESPONSE_CODE"] += 1

        # Count EdgeResponseStatus codes
        if edge_response_status:
            edge_response_counts[edge_response_status] += 1
        else:
            edge_response_counts["EMPTY_RESPONSE"] += 1

        if security_level:
            security_level_counts[security_level] += 1
        else:
            # Count occurrences of empty user agents
            security_level_counts["EMPTY_SECURITY_LEVEL"] += 1

    except json.JSONDecodeError:
        print("Error: Invalid log entry format")
        print(f"Raw Log Entry: {log_entry}")

def process_log_files(folder_path):
    total_entries = 0
    unique_ips = Counter()
    country_counts = Counter()
    unique_user_agents = set()
    user_agent_counts = Counter()
    # Initialize a dictionary to count HTTP response codes
    http_response_counts = Counter()
    edge_response_counts = Counter()
    security_level_counts = Counter()
    log_entries_list = []

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            with open(file_path, "r") as log_file:
                log_entries = [line.strip() for line in log_file.readlines() if line.strip() and line.strip().startswith("{")]
                for entry in log_entries:
                    process_log_entry(entry, unique_ips, country_counts, unique_user_agents, user_agent_counts, http_response_counts, edge_response_counts, security_level_counts, log_entries_list)
                    total_entries += 1

    print("----Log Analyst Report----")
    print(f"\nTotal log entries: {total_entries}")
    print(f"\nTotal unique client IP addresses making requests: {len(unique_ips)}")
    print("\nUnique IP addresses:")
    for ip, count in unique_ips.items():
        print(f"{ip}: {count}")

    print("\nMost common country names:")
    for name, count in country_counts.most_common():
        print(f"{name}: {count}")
    
    print(f"\nTotal unique user agents: {len(unique_user_agents)}")
    print("Top User Agents:")
    for ua, count in user_agent_counts.most_common():
        print(f"{ua}: {count}")

     # Print HTTP response code counts
    print("\nHTTP Response Code Counts:")
    for code, count in http_response_counts.items():
        print(f"{code}: {count}")

    # Print EdgeResponseStatus code counts
    print("\nEdgeResponseStatus Code Counts:")
    for response, count in edge_response_counts.items():
        print(f"{response}: {count}")
    print(f"Total number of unqiue response codes: {len(edge_response_counts)}")

    # Print Security Level counts
    print("\nSecurity Level Counts:")
    for seclvl, count in security_level_counts.items():
        print(f"{seclvl}: {count}")
    print(f"Total number of unqiue security level values: {len(security_level_counts)}")

    # Convert log entries list to DataFrame for anomaly detection
    log_df = pd.DataFrame(log_entries_list)
    anomalies = identify_anomalies(log_df)
    print('\nAnomalies detected:', anomalies)

def identify_anomalies(df):
    anomalies = []

    if df['CacheResponseStatus'].value_counts().idxmax() != 200:
        anomalies.append('Unexpected CacheResponseStatus')

    if df['ClientCountry'].nunique() > 10:
        anomalies.append('High number of unique ClientCountry')

    if df['EdgeResponseStatus'].value_counts().idxmax() != 200:
        anomalies.append('Unexpected EdgeResponseStatus')

    if df['OriginResponseTime'].mean() > 1000000:
        anomalies.append('High average OriginResponseTime')

    if df['ClientIP'].value_counts().max() > 1000:
        anomalies.append('High request rate from a single IP')

    if df['ClientRequestUserAgent'].str.contains('bot|crawler|spider', case=False).any():
        anomalies.append('Suspicious User-Agent detected')

    if df['ClientRequestMethod'].value_counts().idxmax() not in ['GET', 'POST']:
        anomalies.append('Unexpected HTTP method used')

    if df['EdgeResponseStatus'].isin([400, 404, 500, 503]).sum() > 100:
        anomalies.append('Frequent 4xx/5xx status codes')

    if df['ClientSSLProtocol'].isin(['SSLv3', 'TLSv1.0']).any():
        anomalies.append('Outdated SSL/TLS protocol used')

    if df['EdgeRateLimitAction'].notna().sum() > 50:
        anomalies.append('Frequent rate limiting actions')

    if df['FirewallMatchesActions'].apply(len).sum() > 50:
        anomalies.append('Frequent firewall matches')

    if df['ClientRequestBytes'].max() > 1000000 or df['EdgeResponseBytes'].max() > 1000000:
        anomalies.append('Unusually large request/response sizes')

    return anomalies

if __name__ == "__main__":
    process_log_files(log_folder)
