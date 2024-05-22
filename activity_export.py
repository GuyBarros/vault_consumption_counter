import requests
import pandas as pd
import os
import json

# Define the function to fetch data from the API and load it into a pandas DataFrame
def fetch_data_from_api():
    # Get the Vault token from the specified file
    with open(os.path.expanduser("~/.vault-token"), 'r') as file:
        vault_token = file.read().strip()

    # Set the Vault address
    vault_addr = os.getenv('VAULT_ADDR')
    if not vault_addr:
        raise ValueError("VAULT_ADDR environment variable is not set.")

    # Define the API URL with the required parameters
    start_time = "2022-12-31T00:00:00Z"
    end_time = "2024-04-30T23:59:59Z"
    # api_url = f"{vault_addr}/v1/sys/internal/counters/activity/export?start_time={start_time}&end_time={end_time}"
    api_url = f"{vault_addr}/v1/sys/internal/counters/activity/export"
    # Set the headers including the Vault token
    headers = {
        "X-Vault-Token": vault_token
    }

    # Make the GET request to the API
    response = requests.get(api_url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Load the JSON response into a pandas DataFrame
        # data = response.text
        # data2 = f" [ {data.replace("\n", ",").rstrip(',')} ]"
        # data3 = json.loads(data2)
        data3 = json.loads(f" [ {response.text.replace("\n", ",").rstrip(',')} ]")
        #data = response.json()
        # print(data3)
        df = pd.DataFrame(data3)
        return df
    else:
        # Print the error message if the request failed
        raise Exception(f"Failed to fetch data: {response.status_code} - {response.text}")
    
df = fetch_data_from_api()

# Display the first few rows of the DataFrame
print(df.head())