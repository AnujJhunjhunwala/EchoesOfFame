from dotenv import load_dotenv
from openai import OpenAI
from PIL import Image
import requests
from io import BytesIO
import matplotlib.pyplot as plt
from argparse import ArgumentParser
from dotenv import load_dotenv
from openai import OpenAI
from PIL import Image
import requests
from io import BytesIO
import matplotlib.pyplot as plt
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("--topic", type=str, required=True)
parser.add_argument("--name", type=str, required=True)
args = parser.parse_args()


import os
load_dotenv()
for key, value in os.environ.items():
    print(key, "=", value)
eleven_labs_api_key = os.getenv("ELEVENLABS_KEY")
client = OpenAI()



with open('generated_text/conv1/conversation.txt', 'r', encoding='utf-8') as plik:
    text = plik.read()
# Split the text into lines
lines = text.split("\n")

# get rid of the "name: " part
lines = ["".join(line.split(": ")[1:]) for line in lines]

person1_lines = [line for i, line in enumerate(lines) if i % 2 == 0]
person2_lines = [line for i, line in enumerate(lines) if i % 2 == 1]

tristan_voice_id = "9BWtsMINqrJLrRacOk9x"
andrew_voice_id = "CwhRBWXzGAHq8TQ4Fs17"

CHUNK_SIZE = 1024


def get_voice(text, voice_id, output_path):
    tts_url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream"
    headers = {
        "Accept": "application/json",
        "xi-api-key": eleven_labs_api_key,
    }
    data = {
        "text": text,
        "model_id": "eleven_turbo_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.8,
            "style": 0.0,
            "use_speaker_boost": True
        }
    }
    response = requests.post(tts_url, headers=headers, json=data, stream=True)

    if response.ok:
        # Open the output file in write-binary mode
        with open(output_path, "wb") as f:
            # Read the response in chunks and write to the file
            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                f.write(chunk)
        # Inform the user of success
        print("Audio stream saved successfully.")
    else:
        # Print the error message if the request was not successful
        print(response.text)


os.makedirs(args.name, exist_ok=True)

for i, andrew_line in enumerate(person2_lines):
    get_voice(andrew_line, andrew_voice_id, f"{args.name}/andrew_{i}.mp3")

for i, tristan_line in enumerate(person1_lines):
    get_voice(tristan_line, tristan_voice_id, f"{args.name}/tristan_{i}.mp3")

# now stitch the audio files together
from pydub import AudioSegment

combined_audio = None
for i in range(len(person1_lines)):
    try:
        andrew_audio = AudioSegment.from_file(f"{args.name}/andrew_{i}.mp3")
    except:
        break
    try:
        tristan_audio = AudioSegment.from_file(f"{args.name}/tristan_{i}.mp3")
    except:
        combined_audio = combined_audio + andrew_audio
        break
    if combined_audio is None:
        combined_audio = andrew_audio + tristan_audio
    else:
        combined_audio += andrew_audio + tristan_audio

combined_audio.export(f"{args.name}/combined.mp3", format="mp3")
