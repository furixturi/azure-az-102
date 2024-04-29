from dotenv import load_dotenv
import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient


def main():
    try:
        # Load configuration from .env file
        load_dotenv()
        ai_endpoint = os.getenv("AI_ENDPOINT")
        ai_key = os.getenv("AI_KEY")

        # Create a Text Analytics client with the endpoint and key
        credential = AzureKeyCredential(ai_key)
        ai_client = TextAnalyticsClient(endpoint=ai_endpoint, credential=credential)

        # Analyze each text file in the reviews folder
        reviews_folder = "reviews"
        for file_name in os.listdir(reviews_folder):
            # Read the file content
            print("\n--------\n" + file_name)
            text = open(os.path.join(reviews_folder, file_name), encoding="utf8").read()
            print(f"\n{text}\n")
            print("Analysis:")

            # Get language
            lang = ai_client.detect_language(documents=[text])[0]
            print(f"- Language: {lang.primary_language.name}")

            # Get sentiment
            sentiment = ai_client.analyze_sentiment(documents=[text])[0]
            print(f"- Sentiment: {sentiment.sentiment}")

            # Get key phrases
            key_phrases = ai_client.extract_key_phrases(documents=[text])[0].key_phrases
            if len(key_phrases) > 0:
                print("- Key Phrases:")
                for phrase in key_phrases:
                    print(f"  - {phrase}")

            # Get entities
            entities = ai_client.recognize_entities(documents=[text])[0].entities
            if len(entities) > 0:
                print("- Entities:")
                for entity in entities:
                    print(f"  - {entity.text} ({entity.category})")

            # Get linked entities
            linked_entities = ai_client.recognize_linked_entities(documents=[text])[
                0
            ].entities
            if len(linked_entities) > 0:
                print("- Linked Entities:")
                for entity in linked_entities:
                    print(f"  - {entity.name} ({entity.data_source})")
                    print(f"    - URL: {entity.url}")
                    print(
                        f"    - Data Source Entity ID: {entity.data_source_entity_id}"
                    )

    except Exception as e:
        print(f"Error: {e}")
        return


if __name__ == "__main__":
    main()
