import os
import requests
from dotenv import load_dotenv
from pydub import AudioSegment
import math

# Problems 
# - how to get specific voice id for a speaker from eleven labs api ? 
# -> Uploading a sample audio needs verification so I created voices from desciption
# - how to combine multiple audio files into one audio file ? -> Done

def synthesize_voices(topic, dialogue, output_path):
    """
    Convert a dialogue into speech using Eleven Labs API, alternating between speakers.

    Parameters:
    dialogue (str): The dialogue in the format "speaker - line".
    output_path (str): Path to save the final stitched audio file.

    Returns:
    str: Path to the saved audio file.
    """
    load_dotenv()
    api_key = os.getenv("ELEVENLABS_API_KEY")
    base_url = "https://api.elevenlabs.io/v1/text-to-speech"

    if not api_key:
        raise ValueError("Missing Eleven Labs API key in environment variables.")

    lines = [line for line in dialogue.strip().split("\n") if line.strip()]
    file_names = []
    voice_cache = {"Donald Trump": "g3U3eVk0Yt5sfeJlxM0P", 
                   "Justin Bieber": "HLdlhjpJxmtzdJlOEsKv",
                   "Andrew Tate":"6PgIfRMmk2rtjgBBmsHM",
                   "Lionel Messi":"Dzc1MThPTaWVYCF2dwcL",
                   "Gandalf":"2pUh3WvmJfKcmUzjaqrA",
                   "Celine Dion":"0pDL6hElaKtwz4gU3Oez",
                   "Dakota Johnson":"W8b7yotTTKO1HaSI5xSh",
                   "Taylor Swift":"is13V6bEhe2BdMasbKuN",
                   "Nicole Kidman":"A6tzLAZnfblVILfkLgbB",
                   "Helena Bonham Carter":"vPJVoXdSXn5usCAi1Zxw"}

    i = 0
    for line in lines:
        try:
            speaker, text = line.split(": ", 1)
            voice_id = voice_cache[speaker]

            headers = {
                "Accept": "application/json",
                "xi-api-key": api_key,
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

            response = requests.post(
                f"{base_url}/{voice_id}/stream",
                headers=headers,
                json=data,
                stream=True
            )
            response.raise_for_status()

            # audio_data = response.content
            speaker_name = speaker.split(" ")[0].lower()
            file_name = f"dialogues/{topic}_{speaker_name}_{math.floor(i/2)}.mp3"
            file_names.append(file_name)
            with open(file_name, "wb") as f:
                f.write(response.content)
        except Exception as e:
            print(f"Error processing line '{line}': {e}")
        i += 1

    """combined_audio = AudioSegment.from_mp3(file_names[0])
    for file_name in file_names[1:]:
        audio = AudioSegment.from_mp3(file_name)
        combined_audio = combined_audio + audio

    combined_audio.export(output_path, format="mp3")"""
    return output_path