import json
import pandas as pd

# Load data from months2.json
with open('months.json', 'r') as file:
    data = json.load(file)

# Process the JSON data with each mount_path having its own row and correct client counts
def process_data_with_correct_counts(data):
    result = []
    for entry in data:
        timestamp = entry["timestamp"]
        for namespace in entry["namespaces"]:
            namespace_id = namespace["namespace_id"]
            namespace_path = namespace["namespace_path"]
            for mount in namespace["mounts"]:
                mount_path = mount["mount_path"]
                clients = mount["counts"]["clients"]
                new_clients = 0
                if entry["new_clients"] and entry["new_clients"]["namespaces"]:
                    for new_namespace in entry["new_clients"]["namespaces"]:
                        if new_namespace["namespace_id"] == namespace_id:
                            for new_mount in new_namespace["mounts"]:
                                if new_mount["mount_path"] == mount_path:
                                    new_clients = new_mount["counts"]["clients"]
                result.append({
                    "timestamp": timestamp,
                    "namespace_id": namespace_id,
                    "namespace_path": namespace_path,
                    "clients": clients,
                    "new_clients": new_clients,
                    "mount_path": mount_path
                })
    return result

# Get the breakdown of namespaces, their clients, new clients, and individual mount_paths with correct counts
breakdown_with_correct_counts = process_data_with_correct_counts(data)

# Convert to DataFrame
breakdown_with_correct_counts_df = pd.DataFrame(breakdown_with_correct_counts)

# Print the DataFrame (optional)
print(breakdown_with_correct_counts_df)
breakdown_with_correct_counts_df.to_excel("output.xlsx",sheet_name='Sheet_name_1') 