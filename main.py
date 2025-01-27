import dialogue_generator
import text_to_speech
from video_creator import ByteToScale, LipSyncVideo, VideoCreator
import argparse
import instagram_poster


def main(topic, person1, person2):
    """
    Main function to generate a debate post and upload it to Instagram.
    
    Parameters:
    topic (str): The topic of the debate.
    person1 (str): Name of the first famous person.
    person2 (str): Name of the second famous person.
    """
    # Step 1: Generate dialogue
    dialogue = dialogue_generator.generate_dialogue(topic, person1, person2)
    print("Dialogue generated!")
    print(dialogue)

    # Step 2: Synthesize voices (Optional for now)
    output_path = f"{topic}_{person1}_{person2}.mp3"
    audio_files = text_to_speech.synthesize_voices(topic, dialogue, output_path)
    print("Audio files generated:", audio_files)

    # Step 3: Create image with dialogue
    bytescale = ByteToScale(person1, person2, topic)
    image_urls, audio_urls = bytescale.run()

    # print(image_urls, audio_urls)

    # Generate lip-sync videos
    lipsync = LipSyncVideo(person1, person2, image_urls, audio_urls)
    video_urls = lipsync.run()

    # Combine videos
    video_creator = VideoCreator(video_urls, person1, person2, topic)
    video_creator.run()

    # Step 4: Post to Instagram - uncomment below lines to post to Instagram
    # video_path = f"final_video/final_video_{person1}_{person2}_{topic}.mp4"
    # instagram_poster.post_to_instagram(video_path, topic)
    # print("Post uploaded to Instagram!")


if __name__ == "__main__":
    '''
    Choose from the following famous people:
    - Lionel Messi
    - Justin Bieber
    - Andrew Tate
    - Donald Trump
    - Gandalf
    - Celine Dion
    - Dakota Johnson
    - Taylor Swift
    - Nicole Kidman
    - Helena Bonham Carter
    '''

    parser = argparse.ArgumentParser(description="Generate dialogues between two persons on a given topic.")
    parser.add_argument("--topic", required=True, type=str, help="Topic of the dialogue")
    parser.add_argument("--person1", required=True, type=str, help="Name of the first person")
    parser.add_argument("--person2", required=True, type=str, help="Name of the second person")

    args = parser.parse_args()

    main(args.topic, args.person1, args.person2)