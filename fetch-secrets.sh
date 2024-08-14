#!/bin/sh

# Set the Vault address and token
export VAULT_ADDR='http://192.168.3.59:8200'
export VAULT_TOKEN='test'

# Retrieve the secrets from Vault
email=$(vault kv get -field=email secret/myapp)
password=$(vault kv get -field=password secret/myapp)

# Export the secrets as environment variables
export SECRET_EMAIL="$email"
export SECRET_PASSWORD="$password"

# Debugging: Print the retrieved secrets
echo "Email: $SECRET_EMAIL"
echo "Password: $SECRET_PASSWORD"
