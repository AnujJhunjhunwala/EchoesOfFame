# Echoes of Fame

### Generate, Voice, and Share Celebrity Conversations!

**Echoes of Fame** is an innovative project that brings fictional yet intriguing conversations between celebrities to life. Using cutting-edge AI technologies, the project generates dialogues, synthesizes their voices, and posts them as Instagram reels to engage audiences. 

🌟 Check out the Instagram page: [@echoes.of.fame](https://www.instagram.com/echoes.of.fame/?igsh=MW1hdWZxZnk1em40ZA%3D%3D)

---

## Features
- **AI-Generated Dialogues**: Harness the power of OpenAI's GPT to create engaging and realistic conversations.
- **Voice Synthesis**: Eleven Labs API brings the celebrities' voices to life.
- **Seamless Media Handling**: Bytescale API ensures smooth handling of images and videos.
- **Interactive GUI**: Gooey provides a simple, user-friendly interface for lipsync.
- **Instagram Automation**: Automatically posts the reels to the Instagram page.

---

## Usage

### Prerequisites
1. Install Python 3.8+.
2. Clone the repository:
   ```bash
   git clone <repository_url>
   cd EchoesOfFame
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
4. Create a .env file in the root directory and add the following keys:
    ```bash
    OPENAI_API_KEY=XXXXXXXXXXXXXXXX
    ELEVENLABS_API_KEY=XXXXXXXXXXXXXXXX
    BYTESCALE_API_KEY=XXXXXXXXXXXXXXXX
    BYTESCALE_ACCOUNT_ID=XXXXXXXXXXXXXXXX
    GOOEY_API_KEY=XXXXXXXXXXXXXXXX
    INSTAGRAM_USERNAME=XXXXXXXXXXXXXXXX
    INSTAGRAM_PASSWORD=XXXXXXXXXXXXXXXX
### Running the Project
Use the following command to generate a conversation and post it to Instagram:

    python main.py --topic "TOPIC" --person1 "PERSON 1" --person2 "PERSON 2"
- **--topic**: The theme or subject of the conversation.
- **--person1** and **--person2**: The two celebrities featured in the conversation. (Choose from these celebs - Lionel Messi, Justin Bieber, Andrew Tate, Donald Trump, Gandalf, Celine Dion, Dakota Johnson, Taylor Swift, Nicole Kidman, Helena Bonham Carter)

## File and Folder Structure

1. **Images**:
- If you want to change the celebrity images, ensure the following:
    - The resolution should not exceed 1920x1080.
    - The file name should be the first name of the person (e.g., donald.png, nicole.png).

2. **Dialogues**:
- Each generated dialogue is saved as an audio file in the following format:
    ```bash
    dialogues/"topic_name"_"first_name"_"index".mp3
    
    For example: dialogues/messi_vs_ronaldo_donald_1.mp3
3. **Videos**:
- Combined videos are saved in the final_video folder.
- You can directly use the files from this folder for Instagram posting.

## Technologies and APIs Used
- **OpenAI API**: To generate realistic and engaging conversations.
- **Eleven Labs API**: For high-quality voice synthesis.
- **Gooey.AI API**: For lipsync.
- **Bytescale API**: Generate URLs for efficient image and video handling.
## Contributors
1. Anuj Jhunjhunwala
2. Emre Beray Boztepe
3. Łukasz Wasilewski
## Future Enhancements
- **Video-Based Reels**: Transition from static images to animated video reels for a more engaging experience.
- **Custom Celebrity Selection**: Allow users to select celebrities dynamically.
- **Multi-Language Support**: Generate and synthesize conversations in different languages.