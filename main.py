import dialogue_generator
import text_to_speech
import image_creator
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
    print("Generated Dialogue:")
    print(dialogue)

    # Step 2: Synthesize voices (Optional for now)
    output_path = "output_dialogue.mp3"
    audio_files = text_to_speech.synthesize_voices(dialogue,output_path)
    print("Audio files generated:", audio_files)

    # Step 3: Create image with dialogue
    # image_path = image_creator.create_image(dialogue, person1, person2)
    # print("Image created at:", image_path)

    # Step 4: Post to Instagram
    # instagram_poster.post_to_instagram(image_path, topic)
    # print("Post uploaded to Instagram!")


if __name__ == "__main__":
    # Example inputs
    topic = "Blockchain"
    person1 = "Donald Trump"
    person2 = "Justin Bieber"
    main(topic, person1, person2)