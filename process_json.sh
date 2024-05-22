#!/bin/bash

# Load JSON data from months2.json
JSON_FILE="months.json"
OUTPUT_FILE="namespace_breakdown.csv"

# Process the JSON data and handle null values
jq -r '
    .[] |
    .timestamp as $timestamp |
    .namespaces[] |
    .namespace_id as $namespace_id |
    .namespace_path as $namespace_path |
    .mounts[] |
    .mount_path as $mount_path |
    .counts.clients as $clients |
    [
        $timestamp,
        $namespace_id,
        $namespace_path,
        $mount_path,
        $clients,
        (
            .root // [] |
            .[] |
            select(.timestamp == $timestamp) |
            .new_clients.namespaces[]? 
            | select(.namespace_id == $namespace_id) |
            .mounts[]? |
            select(.mount_path == $mount_path) |
            .counts.clients
        )
    ] | @csv
' "$JSON_FILE" > "$OUTPUT_FILE"

# Add header to the output CSV file
echo "timestamp,namespace_id,namespace_path,mount_path,clients,new_clients" | cat - "$OUTPUT_FILE" > temp && mv temp "$OUTPUT_FILE"

# Print the output file
cat "$OUTPUT_FILE"
