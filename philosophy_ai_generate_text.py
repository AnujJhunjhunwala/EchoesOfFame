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
import re
import os
eleven_labs_api_key = os.getenv("ELEVENLABS_KEY")

client = OpenAI()


def format_text(t, person1, person2):
  text_splited = t.split()
  for i in range(len(text_splited)):
    text_splited[i] = re.sub(r'\s*\n\s*', '', text_splited[i])
  speaking_person = text_splited[0]
  if speaking_person == person1 + ":":
    listening_person = person2 + ":"
  else:
    listening_person = person1 + ":"
  line = ""
  formated_text = ""
  for i in range(1, len(text_splited)):
    if text_splited[i] == listening_person:
      formated_text += (speaking_person + line + "\n")
      listening_person = speaking_person
      speaking_person = text_splited[i]
      line = ""
    elif text_splited[i] == speaking_person:
      pass
    else:
      line += " " + text_splited[i]
  return formated_text



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
full_text = format_text(full_text, args.person_1, args.person_2)
os.makedirs(f"generated_text/{args.name}", exist_ok=True)
with open(f"generated_text/{args.name}/conversation.txt", "w") as f:
  f.write(full_text)

