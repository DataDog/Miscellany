#!opt/datadog-agent/embedded/bin/python3
import json
import sys
import requests

secret_id = "<YOUR_SECRET_ID_HERE>"
role_id = "<YOUR_ROLE_ID_HERE>"
VAULT_ADDR= "https://<YOUR_VAULT_ADDRESS_HERE"
VAULT_NAMESPACE = "admin"

def fetch_secrets_from_vault():

    try:
        # Authenticate and get the client token
        response = requests.post(
            url=f"{VAULT_ADDR}/v1/auth/approle/login",
            headers={
                "X-Vault-Namespace": VAULT_NAMESPACE
            },
            json={
                "role_id": role_id,
                "secret_id": secret_id
            }
        )
        response.raise_for_status()
        vault_token = response.json()["auth"]["client_token"]
        
        # Fetch the secret from Vault
        response = requests.get(
            url=f"{VAULT_ADDR}/v1/secret/data/sample-secret",
            headers={
                "X-Vault-Token": vault_token,
                "X-Vault-Namespace": VAULT_NAMESPACE
            }
        )
        response.raise_for_status()
        secret_data = response.json()["data"]["data"]
        return secret_data
    
    except Exception as e:
        print(f"An error occurred while fetching secrets from Vault: {e}")

def retrieve_secrets():

    try:

      secret_request = json.load(sys.stdin)
      secrets = fetch_secrets_from_vault()
  
      secret_response = {}
  
      for secret in secret_request["secrets"]:
          if secret in secrets.keys():
              
              secret_response[secret] = {
                  "value": str(secrets[secret]),
                  "error": None
              }
          else:
              secret_response[secret] = {
                  "value": None,
                  "error": "Unable to retrieve secret."
              }
    except Exception as e:
        print("There was an error retrieving secrets", e)

    sys.stdin.close()
    return secret_response

if __name__ == "__main__" :

    secrets = retrieve_secrets()
    print(json.dumps(secrets))
