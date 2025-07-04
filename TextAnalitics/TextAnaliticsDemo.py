import os
from dotenv import load_dotenv
from azure.ai.textanalytics import TextAnalyticsClient, SentimentConfidenceScores
from azure.core.credentials import AzureKeyCredential
import json

load_dotenv()
key = os.environ['COGNITIVE_SERVICE_KEY']
endpoint = os.environ['COGNITIVE_SERVICE_ENDPOINT']

def authenticate_client():
    credential = AzureKeyCredential(key) # Create an AzureKeyCredential using the Cognitive Service key
    client = TextAnalyticsClient(endpoint=endpoint, credential=credential) # Create a TextAnalyticsClient instance using the key and endpoint
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