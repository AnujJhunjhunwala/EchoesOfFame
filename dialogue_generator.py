from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

client = OpenAI()

def generate_dialogue(topic, person1, person2, n_lines=6):
    """
    Generate a debate-style dialogue between two famous people on a given topic.

    Parameters:
    topic (str): The topic of the debate.
    person1 (str): Name of the first famous person.
    person2 (str): Name of the second famous person.
    n_lines (int): Number of lines (each person contributes half).

    Returns:
    str: Generated dialogue.
    """
    messages = [{
        "role": "system",
            "content": (
                f"You are a conversation generator simulating a debate between {person1} and {person2}. "
                f"The topic is '{topic}'. "
                f"Format the conversation as follows:\n"
                f"{person1}:<message>\n{person2}:<message>\n"
                "They should have opposing views. "
                f"{person1} supports the idea, while {person2} opposes it. "
                "Make sure the responses reflect their real-world speaking styles."
                "Ensure that each response is about 20 words"
            )
    }]
    
    full_text = ""
    speakers = [person1, person2]

    for i in range(n_lines):
        current_speaker = speakers[i % 2]
        messages.append({
            "role": "user", 
            "content": (
                f"Continue the dialogue with {current_speaker}'s response only."
                f"Make sure it is consistent with his previous responses."
            )
        })

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )
        response_text = response.choices[0].message.content.strip()

        # Extract the line starting with the speaker's name
        if response_text.startswith(f"{current_speaker}:"):
            line = response_text
        else:
            # If format is incorrect, prepend the speaker manually
            line = f"{current_speaker}: {response_text}"

        full_text += line + "\n\n"
        messages.append({"role": "assistant", "content": line})

    return full_text.strip()