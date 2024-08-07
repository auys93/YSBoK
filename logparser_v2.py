import os
import json
from collections import Counter
import pycountry

# Folder containing log files (replace with your folder path)
log_folder = "/workspaces/YSBoK/Logs"

# Standard HTTP request methods
standard_methods = {"GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS", "PATCH"}

def process_log_entry(log_entry, unique_ips, country_counts, unique_user_agents, user_agent_counts, http_response_counts, unique_edge_reponse,edge_response_counts):
    try:
        log_data = json.loads(log_entry)
        client_ip = log_data.get("ClientIP")
        country_code = log_data.get("ClientCountry", "").upper()
        request_bytes = log_data.get("ClientRequestBytes", 0)
        request_method = log_data.get("ClientRequestMethod", "").upper()
        user_agent = log_data.get("ClientRequestUserAgent", "")
        http_response_code = log_data.get("ClientRequestMethod", "")
        edge_response_status = log_data.get("EdgeResponseStatus", "")
        unique_edge_reponse = log_data.get("EdgeResponseStatus", "")

        if client_ip and request_bytes != 0 and request_method in standard_methods:
            unique_ips.add(client_ip)

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

        # # Count EdgeResponseStatus codes
        # if edge_response_status:
        #     unique_edge_reponse.add(edge_response_status)
        #     edge_response_counts[edge_response_status] += 1

        # Count EdgeResponseStatus codes (if it's an integer)
        if isinstance(edge_response_status, int):
            edge_response_counts[edge_response_status] += 1

    except json.JSONDecodeError:
        print("Error: Invalid log entry format")
        print(f"Raw Log Entry: {log_entry}")

def process_log_files(folder_path):
    total_entries = 0
    unique_ips = set()
    country_counts = Counter()
    unique_user_agents = set()
    user_agent_counts = Counter()
    # Initialize a dictionary to count HTTP response codes
    http_response_counts = Counter()
    unique_edge_reponse = set()
    edge_response_counts = Counter()


    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            with open(file_path, "r") as log_file:
                log_entries = [line.strip() for line in log_file.readlines() if line.strip() and not line.strip().startswith("#")]
                for entry in log_entries:
                    process_log_entry(entry, unique_ips, country_counts, unique_user_agents, user_agent_counts,http_response_counts, unique_edge_reponse, edge_response_counts)
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
    
    print(f"\nTotal unique user agents: {len(unique_user_agents)}")
    print("\nTop User Agents:")
    for ua, count in user_agent_counts.most_common():
        print(f"{ua}: {count}")

     # Print HTTP response code counts
    print("\nHTTP Response Code Counts:")
    for code, count in http_response_counts.items():
        print(f"{code}: {count}")

    # # Print EdgeResponseStatus code counts
    # print(f"\nTotal Response Cosdes: {len(unique_edge_reponse)}")
    # print("EdgeResponseStatus Code Counts:")
    # for response, count in edge_response_counts.items():
    #     print(f"{response}: {count}")
    print("\nEdgeResponseStatus Code Counts (Integers Only):")
    for code, count in edge_response_counts.items():
        print(f"{code}: {count}")

if __name__ == "__main__":
    process_log_files(log_folder)
