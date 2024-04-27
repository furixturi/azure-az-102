from dotenv import load_dotenv
import ssl
import os, http.client, json
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient


def main():
    global ai_endpoint, ai_key

    try:
        # Get config
        load_dotenv()
        ai_endpoint = os.getenv("AI_SERVICE_ENDPOINT")
        ai_key = os.getenv("AI_SERVICE_KEY")

        # Get user input until they enter "quit"
        user_text = ""
        while user_text != "quit":
            user_text = input("Enter some text (or 'quit' to exit): \n")
            if user_text.lower() != "quit":
                # get_language_rest_client(user_text)
                get_language_sdk_client(user_text)
    except Exception as ex:
        print(ex)


def get_language_rest_client(text):
    try:
        # construct JSON request body, which is a collection of documents, each with an ID and text
        json_body = {"documents": [{"id": "1", "text": text}]}

        print(json.dumps(json_body, indent=4))

        # construct REST http request
        uri = ai_endpoint.rstrip("/").replace("https://", "")
        conn = http.client.HTTPSConnection(
            uri, context=ssl._create_unverified_context()
        )

        # add auth key to request header
        headers = {
            "Content-Type": "application/json",
            "Ocp-Apim-Subscription-Key": ai_key,
        }

        # construct request to Text Analytis language API
        conn.request(
            "POST",
            "/text/analytics/v3.0/languages",
            str(json_body).encode("utf-8"),
            headers,
        )

        # send request
        response = conn.getresponse()
        data = response.read().decode("utf-8")

        # parse the response data
        if response.status == 200:
            # log the full JSON response data
            results = json.loads(data)
            print(json.dumps(results, indent=4))
            # Extract the detected language name
            for document in results["documents"]:
                print(f"Detected language: {document['detectedLanguage']['name']}")
        else:
            # handle http error
            print(f"Error: {response.status}, {data}")

        # always cloase the connection
        conn.close()

    # handle other exceptions
    except Exception as ex:
        print(ex)


def get_language_sdk_client(text):
    # create client using endpoint and api key
    credential = AzureKeyCredential(ai_key)
    client = TextAnalyticsClient(endpoint=ai_endpoint, credential=credential)
    # call the service
    detected_language_response = client.detect_language(documents=[text])
    print(detected_language_response)
    print(f"Detected language: {detected_language_response[0].primary_language.name}")


if __name__ == "__main__":
    main()
