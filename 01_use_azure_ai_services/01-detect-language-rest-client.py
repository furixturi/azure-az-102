from dotenv import load_dotenv
import os, http.client, json


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
                get_language(user_text)
    except Exception as ex:
        print(ex)


def get_language(text):
    try:
        # construct JSON request body, which is a collection of documents, each with an ID and text
        json_body = {"documents": [{"id": "1", "text": text}]}

        print(json.dumps(json_body, indent=4))

        # construct REST http request
        uri = ai_endpoint.rstrip("/").replace("https://", "")
        conn = http.client.HTTPSConnection(uri)

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


if __name__ == "__main__":
    main()
