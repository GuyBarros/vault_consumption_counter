export VAULT_ADDR="https://localhost:8200"
export VAULT_NAMESPACE="admin"
export VAULT_TOKEN=root

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
