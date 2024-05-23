export VAULT_ADDR=https://localhost:8200
export VAULT_TOKEN=root
export VAULT_SKIP_VERIFY=true

vault policy write vault_consumption - <<EOR
  path "sys/internal/counters/activity" {
    capabilities = ["list","read"]
  }
  path "sys/internal/counters/activity/*" {
    capabilities = ["list","read"]
  }
  path "identity/entity/id" {
    capabilities = ["list","read"]
  }
EOR

vault auth enable -path="consumption-test" userpass

vault write auth/consumption-test/users/bob password="training" policies="default"
vault write auth/consumption-test/users/burger password="training" policies="default"
vault write auth/consumption-test/users/guy password="training" policies="default"
vault write auth/consumption-test/users/test password="training" policies="default"

vault login -format=json -method=userpass -path=consumption-test  username=bob password=training
vault login -format=json -method=userpass -path=consumption-test  username=burger password=training
vault login -format=json -method=userpass -path=consumption-test  username=guy password=training
vault login -format=json -method=userpass -path=consumption-test  username=test password=training

export TEMP_ACTIVITIES_FILE="activities.txt"
export ACTIVITIES_FILE="activities.json"
export ENTITIES_FILE="entities.json"
export OUTPUT_JSON_FILE="vault_usage.json"
export OUTPUT_CSV_FILE="vault_usage.csv"
