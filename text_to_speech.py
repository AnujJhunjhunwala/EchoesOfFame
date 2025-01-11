import os
import requests
from dotenv import load_dotenv
from pydub import AudioSegment
import io

# Problems 
# - how to get specific voice id for a speaker from eleven labs api ?
# - how to combine multiple audio files into one audio file ?

# def fetch_voice_id(speaker_name):
#     """
#     Fetch or map the voice ID for a given speaker name using Eleven Labs API.

#     Parameters:
#     speaker_name (str): Name of the speaker.

#     Returns:
#     str: Voice ID corresponding to the speaker.
#     """
#     load_dotenv()
#     api_key = os.getenv("ELEVENLABS_API_KEY")
#     base_url = "https://api.elevenlabs.io/v1/voices"

#     if not api_key:
#         raise ValueError("Missing Eleven Labs API key in environment variables.")

#     headers = {
#         "Accept": "application/json",
#         "xi-api-key": api_key,
#     }
#     # response = requests.get(base_url, headers={"Authorization": f"Bearer {api_key}"})
#     response = requests.get(base_url, headers=headers)
#     response.raise_for_status()
#     voices = response.json().get("voices", [])

#     # Find a matching voice by name (this assumes a simple name match)
#     for voice in voices:
#         if speaker_name.lower() in voice.get("name", "").lower():
#             return voice.get("voice_id")

#     raise ValueError(f"No matching voice found for speaker '{speaker_name}'.")

def synthesize_voices(dialogue, output_path):
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
    audio_segments = []
    voice_cache = {"Donald Trump": "9BWtsMINqrJLrRacOk9x", "Justin Bieber": "CwhRBWXzGAHq8TQ4Fs17"}
    #combined_audio = AudioSegment.silent(duration=0)
    # print(lines)

    i = 0
    for line in lines:
        try:
            speaker, text = line.split(": ", 1)
            # if speaker not in voice_cache:
            #     voice_cache[speaker] = fetch_voice_id(speaker)
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
            with open(f"test_{i}.mp3", "wb") as f:
                f.write(response.content)
            try:
                audio_segments.append(AudioSegment.from_mp3(f"D:\\University\\AnujDevelops\\EchoesOfFame_Anuj\\test_{i}.mp3"))
            except Exception as e:
                print(f"Very bad")
        except Exception as e:
            print(f"Error processing line '{line}': {e}")
        i += 1

    combined_audio = sum(audio_segments)
    combined_audio.export("combined_audio.mp3", format="mp3")
    return output_path