#!/bin/sh

# Set the Vault address and token (you may need to adjust these)
export VAULT_ADDR='http://192.168.3.59:8200'
export VAULT_TOKEN='test'

# Retrieve the secrets from Vault
username=$(vault kv get -field=username secret/mdop)
password=$(vault kv get -field=password secret/mdop)

# Echo the retrieved secrets to the console
echo "Username: $username"
echo "Password: $password"
