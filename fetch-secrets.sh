#!/bin/sh

# Set the Vault address and token (you may need to adjust these)
export VAULT_ADDR='http://192.168.3.59:8200'
export VAULT_TOKEN='test'

# Retrieve the secrets from Vault
export SECRET_USERNAME=$(vault kv get -field=email secret/myapp)
export SECRET_PASSWORD=$(vault kv get -field=password secret/myapp)

# Echo the retrieved secrets to the console (optional, for debugging)
echo "Email: $SECRET_USERNAME"
echo "Password: $SECRET_PASSWORD"
