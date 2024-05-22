curl -o activities.txt --header "X-Vault-Token: $(cat ~/.vault-token)"  --request GET     "${VAULT_ADDR}/v1/sys/internal/counters/activity/export?start_time=${START_TIME}&end_time=${END_TIME}"

input_file="activities.txt"
output_file="activities.json"

jq -s '.' "$input_file" > "$output_file"

echo "[" >> client_ids.json
jq -r '.[].client_id' "$output_file" | while read client_id; do
    
    # Make the API call (assuming a GET request, you can modify if needed)
    response=$(curl -s -X GET --header "X-Vault-Token: $(cat ~/.vault-token)"  --request GET     "${VAULT_ADDR}/v1/identity/entity/id/$client_id")

    # Print the response (or handle it as needed)
    echo "$response,"   >> client_ids.json
done
echo "]" >> client_ids.json
