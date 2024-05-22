#!/bin/bash

# Function to recursively iterate over Vault namespaces and execute a command
iterate_vault_namespaces() {
    local parent_namespace="$1"

    # Get list of Vault namespaces
    local namespaces
    if [ -z "$parent_namespace" ]; then
        namespaces=$(vault namespace list -format=json | jq -r '.namespaces[].id')
    else
        namespaces=$(vault namespace list -format=json -namespace="$parent_namespace" | jq -r '.namespaces[].id')
    fi

    # Check if namespaces list is empty
    if [ -z "$namespaces" ]; then
        echo "No namespaces found."
        return
    fi

    # Iterate over each namespace
    for namespace in $namespaces; do
        local full_namespace="$parent_namespace$namespace"
        echo "Processing namespace: $full_namespace"

        # Execute command for each namespace
        vault list -format=json -detailed -namespace="$full_namespace" identity/entity-alias/id | jq -r '.data.key_info[].canonical_id'

        # Recursively call function for child namespaces
        iterate_vault_namespaces "$full_namespace/"
    done
}

# Check if vault command is available
if ! command -v vault &> /dev/null; then
    echo "HashiCorp Vault CLI (vault) is not installed or not in PATH."
    exit 1
fi

# Authenticate with Vault if needed
# Replace this section with your authentication method if required

# Call the function to recursively iterate over Vault namespaces
iterate_vault_namespaces "admin"
