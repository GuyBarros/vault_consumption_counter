import requests
import pandas as pd
import os
import json
import pygwalker as pyg

def fetch_data_from_api():
    # Set the Vault address
    vault_addr = os.getenv('VAULT_ADDR')
    if not vault_addr:
        raise ValueError("VAULT_ADDR environment variable is not set.")
    # Set the Vault Namespace
    vault_namespace = os.getenv('VAULT_NAMESPACE')
    if not vault_namespace:
        raise ValueError("VAULT_NAMESPACE environment variable is not set.")
    vault_token = os.getenv('VAULT_TOKEN')
    if not vault_token:
        raise ValueError("VAULT_TOKEN environment variable is not set.")
    # Define the API URL with the required parameters
    start_time = "2022-12-31T00:00:00Z"
    end_time = "2024-04-30T23:59:59Z"
    # api_url = f"{vault_addr}/v1/sys/internal/counters/activity/export?start_time={start_time}&end_time={end_time}"
    api_url = f"{vault_addr}/v1/sys/internal/counters/activity??start_time={start_time}&end_time={end_time}"
    # Set the headers including the Vault token
    headers = {
        "X-Vault-Token": vault_token,
        "X-Vault-Namespace": vault_namespace
    }

    # Make the GET request to the API
    response = requests.get(api_url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Load the JSON response into a pandas DataFrame
        data = response.json()['data']
        # data2 = f" [ {data.replace("\n", ",").rstrip(',')} ]"
        #data3 = json.loads(f" [ {response.text.replace("\n", ",").rstrip(',')} ]")
        #print(data2)
        months = data['months']
        # df = pd.read_json(months)
        df = pd.DataFrame(months)
        #df = pd.DataFrame(data2)

        return df
    else:
        # Print the error message if the request failed
        raise Exception(f"Failed to fetch data: {response.status_code} - {response.text}")

df = fetch_data_from_api()
print(df.head())
walker = pyg.walk(df)