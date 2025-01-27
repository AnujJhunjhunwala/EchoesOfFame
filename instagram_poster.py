from instagrapi import Client
from dotenv import load_dotenv
import os

# # Load environment variables
load_dotenv()

def post_to_instagram(video_path, topic):
    """
    Post the image to Instagram with the given topic as the caption.
    
    Parameters:
    image_path (str): The path to the image file.
    topic (str): The topic of the debate.
    """
    print(f"Uploading post to Instagram with topic: {topic}")
    cl = Client()
    cl.login(os.getenv("INSTAGRAM_USERNAME"), os.getenv("INSTAGRAM_PASSWORD"))
    cl.clip_upload(video_path, caption=topic)
    cl.logout()