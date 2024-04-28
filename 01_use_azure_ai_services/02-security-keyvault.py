# After creating the key vault, importing the Azure AI Services resource's key, and creating the service principal, you can use the service principal identity in an application to access the secret key, then use that to access the corresponding Azure AI service resource. (Refer to the notes_w_secrets.md)
# After ceating the service principal, note down the following and put them in your env
## KEY_VAULT: the key vault name
## TENANT_ID: the service principal's tenant ID
## APP_ID: the service principal's app ID
## APP_PASSWORD: the service principal's password


# Dependencies that we'll use:
##  azure-identity==1.5.0
##  azure-keyvault-secrets==4.2.0

from dotenv import load_dotenv
import os
from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient


def main():
    global ai_endpoint
    global cog_key

    try:
        ai_endpoint, cog_key = get_configs()

        # Get user input until "quit" and identify language
        user_text = ""
        while user_text.lower() != "quit":
            user_text = input(
                "Enter a text to identify the language (or 'quit' to exit): "
            )
            if user_text.lower() != "quit":
                language = get_language(user_text)
                print(f"The language of the text is: {language}")

    except Exception as ex:
        print(f"Error: {ex}")


def get_configs():
    # Get config from envs
    load_dotenv()
    ai_endpoint = os.getenv("AI_SERVICE_ENDPOINT")
    key_vault = os.getenv("KEV_VAULT")
    secret_key = os.getenv("SECRET_KEY")
    app_tenant = os.getenv("TENANT_ID")
    app_id = os.getenv("APP_ID")
    app_password = os.getenv("APP_PASSWORD")

    # Get the secret from key vault
    key_vault_uri = f"https://{key_vault}.vault.azure.net"
    credential = ClientSecretCredential(app_tenant, app_id, app_password)
    keyvault_client = SecretClient(key_vault_uri, credential)
    secret = keyvault_client.get_secret(secret_key)
    cog_key = secret.value
    return ai_endpoint, cog_key


def get_language(text):
    # create client using endpoint and cog_key
    credential = AzureKeyCredential(cog_key)
    client = TextAnalyticsClient(endpoint=ai_endpoint, credential=credential)

    # use client to call the service to get detected language
    language = client.detect_language(documents=[text])[0]
    return language.primary_language.name


if __name__ == "__main__":
    main()
