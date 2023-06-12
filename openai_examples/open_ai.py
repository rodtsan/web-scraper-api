import os
import openai
# import wandb
from decouple import config

openai.organization = config("OPENAI_API_ORG")
openai.api_key = config("OPENAI_API_KEY")

list = openai.Model.list()
print(list)

# run = wandb.init("project='GPT-4 in Python'")
# prediction_table = wandb.Table(columns=["prompt", "prompt tokens", "completion", "completion tokens", "model", "total tokens"])

# gpt_prompt = input ("What prompt do you want to use?") 
# print(gpt_prompt)
# message=[{"role": "user", "content": gpt_prompt}]
# response = openai.ChatCompletion.create(
#     model="gpt-4",
#     messages = message,
#     temperature=0.2,
#     max_tokens=1000,
#     frequency_penalty=0.0
# )
# print(response)

# file_path = f"{os.getcwd()}/temp/harvard.wav"
# audio_file = open(file_path, "rb")
# transcript = openai.Audio.transcribe("whisper-1", audio_file)

# print(transcript)

