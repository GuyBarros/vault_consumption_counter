#!/bin/bash
export VAULT_ADDR=https://localhost:8200
export VAULT_CONSUMPTION_TOKEN=$(vault token create -policy=vault_consumption -ttl=8h -field=token)
export KMIP_PATH=kmip

# List all KMIP Scopes for the 
KMIP_SCOPES=$(curl -s -H "X-Vault-Token: ${VAULT_TOKEN}" -H "X-Vault-Request: true" -H "X-Vault-Namespace: ${VAULT_NAMESPACE}" "${VAULT_ADDR}/v1/${KMIP_PATH}/scope?list=true" | jq -r '.data.keys[]' )

# echo "Scopes: $KMIP_SCOPES"

# Iterate over the Scopes to get the Roles
for KMIP_SCOPE in $KMIP_SCOPES; do 

    KMIP_ROLES=$(curl -s -H "X-Vault-Token: ${VAULT_TOKEN}" -H "X-Vault-Request: true" -H "X-Vault-Namespace: ${VAULT_NAMESPACE}" "${VAULT_ADDR}/v1/${KMIP_PATH}/scope/$KMIP_SCOPE/role?list=true" | jq -r '.data.keys[]')

    # echo "Roles: $KMIP_ROLES"

    # Interate over roles to get all Certificates
    for KMIP_ROLE in $KMIP_ROLES; do

        while IFS= read -r cert; do
            KMIP_CERTIFICATES+=("$cert")
        done < <(curl -s -H "X-Vault-Request: true" -H "X-Vault-Token: ${VAULT_TOKEN}" -H "X-Vault-Namespace: ${VAULT_NAMESPACE}" "${VAULT_ADDR}/v1/${KMIP_PATH}/scope/$KMIP_SCOPE/role/$KMIP_ROLE/credential?list=true" | jq -r '.data.keys[]')
       
    done
done

# printf '%s\n' "${KMIP_CERTIFICATES[@]}"

IFS=' ' read -ra certificates_array <<< "$KMIP_CERTIFICATES"

certificate_count=${#KMIP_CERTIFICATES[@]}
echo "Number of KMIP certificates: $certificate_count"