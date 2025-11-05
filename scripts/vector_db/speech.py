#%% packages
import os
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
#%%
speech_config = speechsdk.SpeechConfig(subscription=os.getenv("AZURE_OPENAI_API_KEY"), endpoint=os.getenv("COGNITIVE_SERVICES_ENDPOINT"))
# %%
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

#%% listen for speech
result = speech_recognizer.recognize_once_async().get()
print(result.text)
# %% transcribe a wav file
audio_config = speechsdk.AudioConfig(filename="recording.wav")
speech_recognizer = speechsdk.SpeechRecognizer(
    speech_config=speech_config,
    audio_config=audio_config,
    language="de-DE"
)
result = speech_recognizer.recognize_once_async().get()
print(result.text)

# %%
