from dotenv import load_dotenv
from datetime import datetime
import os
import azure.cognitiveservices.speech as speech_sdk


def main():
    try:
        global speech_config

        # load configuration from environment variables
        load_dotenv()
        ai_key = os.getenv("SPEECH_KEY")
        ai_region = os.getenv("SPEECH_REGION")

        # configure speech service
        speech_config = speech_sdk.SpeechConfig(ai_key, ai_region)
        print(f"Ready to use speech service in: {speech_config.region}")

        # get spoken input
        command = transcribe_command()
        if command.lower() == "what time is it?":
            tell_time()

    except Exception as ex:
        print(ex)


def transcribe_command():
    command = ""

    # configure speech recognition
    audio_config = speech_sdk.AudioConfig(use_default_microphone=True)
    speech_recognizer = speech_sdk.SpeechRecognizer(speech_config, audio_config)
    print("Speak now...")

    # process speech input
    speech = speech_recognizer.recognize_once_async().get()
    if speech.reason == speech_sdk.ResultReason.RecognizedSpeech:
        command = speech.text
        print(f"Recognized command: '{command}'")
    else:
        print(speech.reason)
        if speech.reason == speech_sdk.ResultReason.Canceled:
            cancellation = speech.cancellation_details
            print(f"Cancellation reason: {cancellation.reason}")
            print(f"Cancellation error details: {cancellation.error_details}")

    # return the command
    return command


def tell_time():
    now = datetime.now()
    response_text = f"The time is {now:%I:%M %p}"

    # configure speech synthesis
    # speech_config.speech_synthesis_voice_name = "en-GB-RyanNeural"
    speech_config.speech_synthesis_voice_name = "en-GB-LibbyNeural"
    speech_synthesizer = speech_sdk.SpeechSynthesizer(speech_config)

    # synthesize spoken response
    ## optional: use SSML to customize the response
    response_ssml = f" \
        <speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='en-GB'> \
            <voice name='en-GB-LibbyNeural'> \
                {response_text} \
                <break strength='weak'/> \
                Time to end this lab! \
            </voice> \
        </speak>"
    # speak = speech_synthesizer.speak_text_async(response_text).get()
    speak = speech_synthesizer.speak_ssml_async(response_ssml).get()
    if speak.reason != speech_sdk.ResultReason.SynthesizingAudioCompleted:
        print(f"Speech synthesis failed: {speak.reason}")


if __name__ == "__main__":
    main()
