import os
import requests
from dotenv import load_dotenv
from moviepy import VideoFileClip, concatenate_videoclips
import subprocess
import json

load_dotenv()

BYTESCALE_API_KEY = os.getenv("BYTESCALE_API_KEY")
BYTESCALE_ACCOUNT_ID = os.getenv("BYTESCALE_ACCOUNT_ID")
BYTESCALE_UPLOAD_URL = f"https://api.bytescale.com/v2/accounts/{BYTESCALE_ACCOUNT_ID}/uploads/binary"

GOOEY_API_KEY = os.getenv("GOOEY_API_KEY")
GOOEY_API_ENDPOINT = "https://api.gooey.ai/v2/Lipsync"

class ByteToScale:
    def __init__(self, first_person, second_person, topic):
        self.first_person = first_person
        self.second_person = second_person
        self.topic = topic

    def upload_to_bytescale(self, file_path):
        """
        Upload a file to Bytescale using the curl command and return its URL.
        """
        url = f"https://api.bytescale.com/v2/accounts/{BYTESCALE_ACCOUNT_ID}/uploads/binary"
        
        content_type = "image/png" if file_path.endswith(".png") else "audio/mpeg"

        result = subprocess.run([
            "curl",
            url,
            "-H",
            f"Authorization: Bearer {BYTESCALE_API_KEY}",
            "-H",
            f"Content-Type: {content_type}",
            "--data-binary",
            f"@{file_path}",
        ], capture_output=True, text=True)

        if result.returncode == 0:
            try:
                uploaded_url = json.loads(result.stdout).get("fileUrl")
                if uploaded_url:
                    print(f"Uploaded: {file_path} -> {uploaded_url}")
                    return uploaded_url
                else:
                    print(f"Error: No file URL returned for {file_path}")
                    return None
            except json.JSONDecodeError:
                print(f"Error decoding response for {file_path}: {result.stdout}")
                return None
        else:
            print(f"Error uploading {file_path}: {result.stderr}")
            return None

    def run(self):
        image_path = "images/"
        speech_path = "dialogues/"
        first_person_name = self.first_person.split(" ")[0].lower()
        second_person_name = self.second_person.split(" ")[0].lower()

        image_urls = {
            self.first_person: self.upload_to_bytescale(f"{image_path}{first_person_name}.png"),
            self.second_person: self.upload_to_bytescale(f"{image_path}{second_person_name}.png")
        }

        audio_files = [
            f"{speech_path}{self.topic}_{first_person_name}_0.mp3",
            f"{speech_path}{self.topic}_{second_person_name}_0.mp3",
            f"{speech_path}{self.topic}_{first_person_name}_1.mp3",
            f"{speech_path}{self.topic}_{second_person_name}_1.mp3",
            f"{speech_path}{self.topic}_{first_person_name}_2.mp3",
            f"{speech_path}{self.topic}_{second_person_name}_2.mp3",
        ]

        audio_urls = [self.upload_to_bytescale(audio) for audio in audio_files]

        return image_urls, audio_urls


class LipSyncVideo:
    def __init__(self, first_person, second_person, image_urls, audio_urls):
        self.first_person = first_person
        self.second_person = second_person
        self.image_urls = image_urls
        self.audio_urls = audio_urls

    def create_lip_sync_video(self, image_url, audio_url):
        """
        Use Gooey AI to create a lip-synced video for the given image and audio.
        """
        payload = {
            "input_face": image_url,
            "input_audio": audio_url,
            "face_padding_top": 0,
            "face_padding_bottom": 0,
            "face_padding_left": 0,
            "face_padding_right": 0,
            "sadtalker_settings": None,
            "selected_model": "Wav2Lip",
            "functions": None,
            "variables": None,
        }


        headers = {
            "Authorization": f"Bearer {GOOEY_API_KEY}",
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(GOOEY_API_ENDPOINT, json=payload, headers=headers)
            
            if response.status_code == 200:
                response_data = response.json()
                output_video = response_data.get("output", {}).get("output_video")
                if output_video:
                    print(f"Lip-sync video created: {output_video}")
                    return output_video
                else:
                    print("Output video URL not found in response.")
                    return None
            else:
                print(f"Error creating lip-sync video: {response.status_code}, {response.text}")
                return None

        except requests.exceptions.RequestException as e:
            print(f"API request failed: {e}")
            return None

    def run(self):
        video_urls = []
        for i, audio_url in enumerate(self.audio_urls):
            speaker = self.first_person if i%2 == 0 else self.second_person
            # print(i, speaker, audio_url, self.image_urls[speaker]), 
            video_url = self.create_lip_sync_video(self.image_urls[speaker], audio_url)
            video_urls.append(video_url)
        
        return video_urls

class VideoCreator:
    def __init__(self, video_urls, first_person, second_person, topic):
        self.video_urls = video_urls
        self.save_videos_path = "videos/"
        self.first_person = first_person
        self.second_person = second_person
        self.topic = topic
        self.save_final_video_path = f"final_video/final_video_{first_person}_{second_person}_{topic}.mp4"

    def download_video(self, video_url, file_name):
        """
        Download the video from the provided URL.
        """
        if not video_url:
            print(f"Skipping download, invalid URL: {video_url}")
            return None

        file_path = os.path.join(self.save_videos_path, file_name)
        try:
            response = requests.get(video_url, stream=True)
            if response.status_code == 200:
                with open(file_path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                print(f"Downloaded video: {file_path}")
                return file_path
            else:
                print(f"Failed to download video from {video_url}, Status Code: {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error downloading video {video_url}: {e}")
            return None
    

    def convert_video(self, input_file, output_file):
        """
        Convert video to a standard format (MP4, 1920x1080 resolution, 30fps).
        """
        try:
            command = [
                "ffmpeg",
                "-i", input_file,
                "-vf", "scale=480:480",
                "-r", "30",
                "-c:v", "libx264",
                "-preset", "slow",
                "-crf", "23",
                "-c:a", "aac",
                "-b:a", "128k",
                output_file
            ]
            subprocess.run(command, check=True)
            print(f"Converted {input_file} to {output_file}")
            return output_file
        except subprocess.CalledProcessError as e:
            print(f"Error converting video {input_file}: {e}")
            return None


    def combine_videos(self):
        """
        Combine multiple video clips into one.
        """
        downloaded_videos = []
        temp_video_files = []

        for idx, url in enumerate(self.video_urls):
            file_name = f"temp_video_{self.first_person}_{self.second_person}_{self.topic}_{idx}.mp4"
            downloaded_file = self.download_video(url, file_name)
            if downloaded_file:
                converted_file = self.convert_video(downloaded_file, f"{self.save_videos_path}converted_{file_name}")
                downloaded_videos.append(VideoFileClip(converted_file))
                temp_video_files.append(downloaded_file)

        final_video = concatenate_videoclips(downloaded_videos, method="compose")
        final_video.write_videofile(self.save_final_video_path, codec="libx264", fps=30, audio_codec="aac")

        print(f"Final combined video saved as {self.save_final_video_path}")

        self.cleanup_temp_files()

    def cleanup_temp_files(self):
        """
        Delete all temporary video files starting with 'temp_'.
        """
        for file in os.listdir(self.save_videos_path):
            if file.startswith("temp_"):
                file_path = os.path.join(self.save_videos_path, file)
                try:
                    os.remove(file_path)
                    print(f"Deleted temporary file: {file_path}")
                except OSError as e:
                    print(f"Error deleting file {file_path}: {e}")

    def run(self):
        self.combine_videos()
