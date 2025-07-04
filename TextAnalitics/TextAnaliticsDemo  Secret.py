import os
from azure.keyvault.secrets import SecretClient
from azure.ai.textanalytics import TextAnalyticsClient, SentimentConfidenceScores
from azure.core.credentials import AzureKeyCredential
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv
import json


load_dotenv()
key_vault_endpoint = os.environ['KEY_VAULT_URL']
cognitive_service_endpoint = os.environ['COGNITIVE_SERVICE_ENDPOINT']

def authenticate_client():
    credential = DefaultAzureCredential() # This will use the default credentials available in the environment
    secret_client = SecretClient(vault_url=key_vault_endpoint, credential=credential)   # Create a SecretClient instance
    cognitive_service_key = secret_client.get_secret("SecretForTextAnalystDemo").value  # Retrieve the secret value from Key Vault
    token= AzureKeyCredential(cognitive_service_key)  # Create an AzureKeyCredential using the retrieved key
    client = TextAnalyticsClient(endpoint=cognitive_service_endpoint, credential=token)   # Create a TextAnalyticsClient instance using the retrieved key
    return client

def analyze_sentiment(client, document):
    return client.analyze_sentiment(documents=document)

def convert_to_dict(obj):
    if isinstance(obj, SentimentConfidenceScores):
        return {
            'positive': obj.positive,
            'neutral': obj.neutral,
            'negative': obj.negative
        }
    elif hasattr(obj, '__dict__'):
        return {key: convert_to_dict(value) for key, value in obj.__dict__.items()}
    elif isinstance(obj, list):
        return [convert_to_dict(item) for item in obj]
    else:
        return obj

def print_json_response(json_response):
    
    data = [convert_to_dict(doc) for doc in json_response]
    json_data = json.dumps(data, indent=4)
    print(json_data)


def main():
    documents = ["I had the best day of my life. I wish you were there with me."]
    client = authenticate_client()
    response = analyze_sentiment(client, documents)
    print_json_response(response)


# Entry point
if __name__ == "__main__":
    main()