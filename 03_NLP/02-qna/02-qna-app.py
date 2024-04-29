from dotenv import load_dotenv
import os

from azure.core.credentials import AzureKeyCredential
from azure.ai.language.questionanswering import QuestionAnsweringClient


def main():
    try:
        # Load configuration from environment variables
        load_dotenv()
        ai_endpoint = os.getenv("AI_ENDPOINT_CUSTOM")
        ai_key = os.getenv("AI_KEY_CUSTOM")
        ai_project_name = os.getenv("QA_PROJECT_NAME")
        ai_deployment_name = os.getenv("QA_DEPLOYMENT_NAME")

        # Create client using endpoint and key
        credential = AzureKeyCredential(ai_key)
        ai_client = QuestionAnsweringClient(endpoint=ai_endpoint, credential=credential)

        # Submit a question and display the answer
        user_question = ""
        while user_question.lower() != "quit":
            user_question = input('\nSubmit a question, or type "quit" to quit.\n')
            if user_question.lower() != "quit":
                response = ai_client.get_answers(
                    question=user_question,
                    project_name=ai_project_name,
                    deployment_name=ai_deployment_name,
                )
                for candidate in response.answers:
                    print(candidate.answer)
                    print(f"Confidence: {candidate.confidence}")
                    print(f"Source: {candidate.source}")

    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()
