import requests
import pandas as pd
import os
import json
from datetime import datetime


# Set the Vault TOKEN
vault_token = os.getenv('VAULT_TOKEN')
if not vault_token:
    raise ValueError("VAULT_TOKEN environment variable is not set.")

    # Set the Vault address
vault_addr = os.getenv('VAULT_ADDR')
if not vault_addr:
    raise ValueError("VAULT_ADDR environment variable is not set.")

vault_namespace = os.getenv('VAULT_NAMESPACE')
print(vault_namespace)
# Define the API URL with the required parameters
start_time = "2022-12-31T00:00:00Z"
end_time = "2024-04-30T23:59:59Z"

# Set the headers including the Vault token
headers = {
    "X-Vault-Token": vault_token
}
# change header if using a namespace (needed for HCP Vault)

# Function to convert timestamp to human-readable format
def convert_timestamp(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
# Define the function to fetch data from the API and load it into a pandas DataFrame
def fetch_activities_from_vault():
    api_url = f"{vault_addr}/v1/sys/internal/counters/activity/export?start_time={start_time}&end_time={end_time}"
    # Make the GET request to the API
    response = requests.get(api_url, headers=headers)
    # Check if the request was successful
    if response.status_code == 200:
        # Load the JSON response into a pandas DataFrame
        data = json.loads(f" [ {response.text.replace("\n", ",").rstrip(',')} ]")
        for activity in data:
            activity['client_id'] = entity_alias_from_list(activity['client_id'],activity['mount_accessor'])
            #activity['client_id'] = entity_alias_from_list("505f84c9-02dc-391b-3794-b4baf0a9b688","auth_oidc_363d78c8")
            activity['timestamp'] = convert_timestamp(activity['timestamp'])
        return data
    else:
        # Print the error message if the request failed
        raise Exception(f"Failed to fetch Activities: {response.status_code} - {response.text}")
def fetch_all_entities_from_vault():
    api_url = f"{vault_addr}/v1/identity/entity/id"
    # Make the GET request to the API
    response = requests.request('LIST',api_url, headers=headers)
    # Check if the request was successful
    if response.status_code == 200:
        # Load the JSON response into a pandas DataFrame
        data = response.json()['data']['key_info']
        return data
    else:
        # Print the error message if the request failed
        raise Exception(f"Failed to fetch All Entities: {response.status_code} - {response.text}")

def entity_alias_from_list(client_id,mount_accessor):
    if not (entities.get(client_id) is None):
     data = entities.get(client_id) ['aliases']
     name = client_id
     #find the alias for the correct mount path
     for item in data:
        if item['mount_accessor'] == mount_accessor:
            name = item['name']
     return name
    else:
        return client_id


entities = fetch_all_entities_from_vault()
df = pd.DataFrame(fetch_activities_from_vault())
# Display the first few rows of the DataFrame
print(df.head())
df.to_excel("vault_consumption.xlsx",sheet_name='Vault Consumption') 