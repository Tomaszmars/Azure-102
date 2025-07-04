from dotenv import load_dotenv
import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import json


def main():
    global ai_endpoint
    global ai_key

    try:
        # Get Configuration Settings
        load_dotenv()
        ai_endpoint = os.getenv('AI_SERVICE_ENDPOINT')
        key_vault_endpoint = os.environ['KEY_VAULT_URL']    
        
        credentials = DefaultAzureCredential()  # This will use the default credentials available in the environment
        secret_client = SecretClient(vault_url=key_vault_endpoint, credential=credentials)   # Create a SecretClient instance
        cognitive_service_key = secret_client.get_secret("SecretForAzureAiServices").value  # Retrieve the secret value from Key Vault
        ai_key = cognitive_service_key  # Use the retrieved key for authentication
        # Get user input (until they enter "quit")
        userText =''
        while userText.lower() != 'quit':
            userText = input('\nEnter some text ("quit" to stop)\n')
            if userText.lower() != 'quit':
                language = GetLanguage(userText)
                print('Language:', language)
                

    except Exception as ex:
        print(ex)

def GetLanguage(text):

    # Create client using endpoint and key
    credential = AzureKeyCredential(ai_key)
    client = TextAnalyticsClient(endpoint=ai_endpoint, credential=credential)

    # Call the service to get the detected language
    detectedLanguage = client.detect_language(documents = [text])[0]
    return detectedLanguage.primary_language.name


if __name__ == "__main__":
    main()