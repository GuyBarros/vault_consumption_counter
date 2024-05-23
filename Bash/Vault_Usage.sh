export VAULT_ADDR=http://localhost:8200
export VAULT_TOKEN=root
export START_TIME="2022-12-31T00:00:00Z"
export END_TIME="2024-04-30T23:59:59Z"
export TEMP_ACTIVITIES_FILE="activities.txt"
export ACTIVITIES_FILE="activities.json"
export ENTITIES_FILE="entities.json"
export OUTPUT_JSON_FILE="vault_usage.json"
export OUTPUT_CSV_FILE="vault_usage.csv"

# --header "X-Vault-Namespace: ${VAULT_NAMESPACE}"
curl -o ${ENTITIES_FILE} --header "X-Vault-Token: ${VAULT_TOKEN}"  --request LIST   "${VAULT_ADDR}/v1/identity/entity/id"
# NOTE: activity/export isnt yet available on HCP Vault
curl -o ${TEMP_ACTIVITIES_FILE} --header "X-Vault-Token: ${VAULT_TOKEN}"  --request GET     "${VAULT_ADDR}/v1/sys/internal/counters/activity/export?start_time=${START_TIME}&end_time=${END_TIME}"



jq -s '.' "$TEMP_ACTIVITIES_FILE" > "$ENTITIES_FILE"

# Extract relevant data from entities file and create a temporary JSON mapping file
jq -r '
  .data.key_info | 
  to_entries | 
  map(
    .key as $client_id | 
    .value.aliases[] | 
    select(.mount_accessor != null) | 
    {
      mount_accessor: .mount_accessor, 
      client_id: $client_id, 
      alias_name: .name
    }
  ) | 
  map({ (.mount_accessor + ":" + .client_id): .alias_name }) | 
  add
' "$ENTITIES_FILE" > temp_mapping.json

# Read activities file, replace client_id with alias name, and convert timestamp to human-readable format
jq --argjson mapping "$(cat temp_mapping.json)" '
  map(
    .client_id as $cid |
    .mount_accessor as $ma |
    .client_id = ($mapping[$ma + ":" + $cid] // $cid) |
    .timestamp = (.timestamp | todate)
  )
' "$ACTIVITIES_FILE" > "$OUTPUT_JSON_FILE"

# Convert the final JSON output to CSV format
jq -r '
  (.[0] | keys_unsorted) as $keys |
  $keys,
  map([.[ $keys[] ]])[] |
  @csv
' "$OUTPUT_JSON_FILE" > "$OUTPUT_CSV_FILE"

# Clean up temporary files
rm temp_mapping.json

echo "Vault Usage JSON file has been generated at $OUTPUT_JSON_FILE"
echo "Vault Usage CSV file has been generated at $OUTPUT_CSV_FILE"


