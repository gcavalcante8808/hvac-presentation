path "database/creds/da-todas-as-permissoes-na-base-db" {
  capabilities = ["read"]
}

path "kv/metadata/mysql-apresentacao" {
  capabilities = ["read", "list"]
}

path "kv/data/mysql-apresentacao" {
  capabilities = ["read", "list"]
}

path "kv/mysql-apresentacao" {
  capabilities = ["read", "list"]
}
