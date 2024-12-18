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
parser.add_argument("--person_1", type=str, required=True)
parser.add_argument("--person_2", type=str, required=True)
parser.add_argument("--n_lines", type=int, default=10)
args = parser.parse_args()

# Load environment variables
load_dotenv()

import os
eleven_labs_api_key = os.getenv("ELEVENLABS_KEY")

client = OpenAI()

messages = [{
  "role": "system",
  "content": f"You are a conversation generator on a philosophy podcast."\
              f"The conversation is between {args.person_1} and {args.person_2}."\
              f"Format the conversation as follows: '{args.person_1}: <message>' '{args.person_2}: <message>' ..."\
              "You don't have to be agreeable, the two people should have opposing views."\
              f"{args.person_1} supports the idea, {args.person_2} opposes it."\
              "Please make the coversation generated adhere to the personalities of the people."\
              "Please only generate the script and no additional output."
  },
  {
    "role": "user",
    "content": f"The topic is {args.topic}. Please generate the first sentence of {args.person_1}."
  },
]
response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=messages
)

names = [args.person_1, args.person_2]

full_text = ""

for i in range(args.n_lines):
  messages.append({
    "role": "user",
    "content": f"Please generate the response of {names[1-i%2]}."
  })
  response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=messages
  )
  response_text = response.choices[0].message.content
  messages.append({
    "role": "assistant",
    "content": response_text
  })
  full_text += response_text + "\n"
  print(response_text)

# Output the generated text to a file
# make directory
os.makedirs(f"generated_text/{args.name}", exist_ok=True)
with open(f"generated_text/{args.name}/conversation.txt", "w") as f:
  f.write(full_text)

