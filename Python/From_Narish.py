import argparse
import os
import csv
import requests
import json
from datetime import datetime, timedelta

# Global variables
activity_json_filename = 'activity-{}.json'.format(datetime.now().strftime("%Y%m%d"))
activity_namespaces_filename = 'activity-namespaces-{}.csv'.format(datetime.now().strftime("%Y%m%d"))
activity_mounts_filename = 'activity-mounts-{}.csv'.format(datetime.now().strftime("%Y%m%d"))
billing_start_date = "2023-06-01"
vault_addr = os.environ.get('VAULT_ADDR')
vault_token = os.environ.get('VAULT_TOKEN')


def _get_first_day_of_month(month):
    """
    This function takes a datetime object as input and returns a new datetime object representing the first day of the given month.
    The time part of the returned datetime object is set to 00:00:00.

    Args:
        month (datetime): A datetime object representing any day of the month.

    Returns:
        datetime: A datetime object representing the first day of the input month.
    """
    return month.replace(day=1)


def _get_last_day_of_month(month):
    """
    This function takes a datetime object as input and returns a new datetime object representing the last day of the given month.
    The time part of the returned datetime object is set to 00:00:00.

    Args:
        month (datetime): A datetime object representing any day of the month.

    Returns:
        datetime: A datetime object representing the last day of the input month.
    """
    next_month = month.replace(day=28) + timedelta(days=4)
    return next_month - timedelta(days=next_month.day)


def _get_last_month():
    """
    This function returns a datetime object representing the last day of the previous month from today's date.
    The time part of the returned datetime object is set to 00:00:00.

    Returns:
        datetime: A datetime object representing the last day of the previous month.
    """
    return (datetime.today().replace(day=1) - timedelta(days=1))  #.strftime('%Y-%m')


# Create activity report
import requests


def create_activity_report(start_date=None, end_date=None, json_file_name=None):
    """
    This function creates an activity report based on the provided start and end dates, or from a provided JSON file.
    The report includes information about namespaces and mounts, such as their IDs, paths, and client counts.

    Args:
        start_date (str, optional): The start date for the activity report in the format 'YYYY-MM-DD'. Defaults to None.
        end_date (str, optional): The end date for the activity report in the format 'YYYY-MM-DD'. Defaults to None.
        json_file_name (str, optional): The name of a JSON file to use for creating the activity report. Defaults to None.
    """

    namespaces = [['namespace_id', 'namespace_path', 'mounts', 'clients', 'entity_clients', 'non_entity_clients']]
    mounts = [['namespace_id', 'namespace_path', 'mount_path', 'clients', 'entity_clients', 'non_entity_clients']]

    # start_date = _get_first_day_of_month(datetime.strptime(month, '%Y-%m')).strftime("%Y-%m-%d")
    # end_date = _get_last_day_of_month(datetime.strptime(month, '%Y-%m')).strftime("%Y-%m-%d")

    data = None
    if json_file_name:
        print(f"Fetching activity report from {json_file_name}")
        with open(json_file_name, "r") as json_file:
            data = json.load(json_file)["data"]
    else:
        url = f"{vault_addr}/v1/sys/internal/counters/activity?end_time={end_date}T00%3A00%3A00Z&start_time={start_date}T00%3A00%3A00Z"
        print(f"Fetching activity report data for {start_date} to {end_date}\n{url}")

        headers = {'X-Vault-Token': vault_token}
        response = requests.get(url, headers=headers, timeout=300)
        if response.status_code == 200:
            data = response.json()["data"]

            print(f"Summary - Start datetime: {data['start_time']}, clients:{data['total']['clients']}, entity_clients:{data['total']['entity_clients']}, "
                  f"non_entity_clients:{data['total']['non_entity_clients']}\n")

            with open(activity_json_filename, 'w') as jsonfile:
                json.dump(data, jsonfile)
        else:
            raise Exception(f"Error creating activity report {response.status_code} - {response.text}")

    if data:
        for namespace in data["by_namespace"]:
            namespaces.append([namespace["namespace_id"],
                               namespace["namespace_path"],
                               len(namespace["mounts"]),
                               namespace["counts"]["clients"],
                               namespace["counts"]["entity_clients"],
                               namespace["counts"]["non_entity_clients"]])

            for mount in namespace["mounts"]:
                mounts.append([namespace["namespace_id"],
                               namespace["namespace_path"],
                               mount["mount_path"],
                               mount["counts"]["clients"],
                               mount["counts"]["entity_clients"],
                               mount["counts"]["non_entity_clients"]])


    with open(activity_mounts_filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(iter(mounts))

    with open(activity_namespaces_filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(iter(namespaces))


# Read activity report
def read_activity_report():
    """
    This function reads the activity report from two CSV files: 'activity-namespaces-{}.csv' and 'activity-mounts-{}.csv'.
    It prints the contents of these files to the console. The first file contains information about namespaces and the second one about mounts.

    Prints:
        Namespace client counts: Prints the contents of the 'activity-namespaces-{}.csv' file.
        Mount path client counts: Prints the contents of the 'activity-mounts-{}.csv' file.
    """
    print("Namespace client counts")
    with open(activity_namespaces_filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            print(row)

    print("\nMount path client counts")
    with open(activity_mounts_filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            print(row)


def main():
    parser = argparse.ArgumentParser(description='Create vault client activity report.')
    parser.add_argument('-s', '--start_date', type=str, help='Start date (YYYY-MM-DD) for the activity report')
    parser.add_argument('-e', '--end_date', type=str, help='End date (YYYY-MM-DD) for the activity report')
    parser.add_argument('-f', '--filename', type=str, help='JSON file name for the activity report')
    parser.add_argument('-p', '--print', default=False, action=argparse.BooleanOptionalAction,
                        help='Print the activity report')

    args = parser.parse_args()
    json_file_name = None
    if args.start_date:
        start_date = args.start_date
    else:
        start_date = billing_start_date

    if args.end_date:
        end_date = args.end_date
    else:
        end_date = _get_last_month().strftime("%Y-%m-%d")

    if args.filename:
        json_file_name = args.filename

    if json_file_name:
        create_activity_report(json_file_name=json_file_name)
    else:
        # Confirm if VAULT_ADDR and VAULT_TOKEN environment variables are set
        if not vault_token:
            raise Exception("VAULT_TOKEN environment variable not set")
        if not vault_addr:
            raise Exception("VAULT_ADDR environment variable not set")

        create_activity_report(start_date=start_date, end_date=end_date)

    if args.print:
        read_activity_report()


if __name__ == "__main__":
    main()