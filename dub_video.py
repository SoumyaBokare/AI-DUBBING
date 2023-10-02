import io
import os
from google.cloud import speech_v1p1beta1 as speech
from google.cloud import texttospeech_v1 as tts
from google.cloud import translate_v2 as translate
import subprocess

# Define input file path
input_file = os.path.join("videos", "input", "input.mp4")

# Extract audio from input video
ffmpeg_path = r"C:\PATH_programs\ffmpeg\bin\ffmpeg.exe"
subprocess.run([ffmpeg_path, "-y", "-i", input_file, "-vn", "-acodec", "copy", "audio.aac"])

# Set up Google Cloud API credentials
credentials_file = r"C:\Users\soumy\Downloads\dubbing-ai-400711-5211ed5388a5.json"
input_file = r"C:\Users\soumy\OneDrive\Desktop\dub_python\videos\input\input.mp4"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_file

# Extract audio from input video
ffmpeg_path = r"C:\PATH_programs\ffmpeg.exe"
os.system(f"{ffmpeg_path} -i {input_file} -vn -acodec copy audio.aac")

# Set up speech-to-text client
speech_client = speech.SpeechClient()

# Set up translation client
translate_client = translate.Client()

# Set up text-to-speech client
tts_client = tts.TextToSpeechClient()

# Set up input and output file paths
output_file = r"C:\Users\soumy\OneDrive\Desktop\dub_python\videos\output\output.mp4"

# Extract audio from input video
os.system(f"{ffmpeg_path} -y -i {input_file} -vn -acodec copy audio.aac")

# Transcribe audio from input video
with io.open('audio.aac', 'rb') as audio_file:
    content = audio_file.read()
audio = speech.RecognitionAudio(content=content)
config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
    language_code='en-US',
    audio_channel_count=2,
)
response = speech_client.recognize(config=config, audio=audio)
transcription = response.results[0].alternatives[0].transcript

# Translate transcription to Hindi
translation = translate_client.translate(transcription, target_language='hi')['translatedText']

# Generate Hindi audio from translated text
synthesis_input = tts.SynthesisInput(text=translation)
voice = tts.VoiceSelectionParams(
    language_code='hi-IN',
    name='hi-IN-Wavenet-A',
    ssml_gender=tts.SsmlVoiceGender.FEMALE
)
audio_config = tts.AudioConfig(
    audio_encoding=tts.AudioEncoding.MP3
)
response = tts_client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
with open('audio.mp3', 'wb') as out:
    out.write(response.audio_content)