
import openai
from openai import OpenAI
from db import OPENAI_API_KEY

try:
  my_api_key = OPENAI_API_KEY          
  client = OpenAI(api_key=my_api_key)
except Exception as ex:
    print("Exception:", ex)
    exit()


messages = [{'role': 'user', 'content': "What's 1+1? Answer in one word."}]
model = "gpt-4o" 

response = client.chat.completions.create(model=model, messages=messages, stream=True)

print(response)

print("=====================================")


for chunk in response:
    print(chunk)
    print(chunk.choices[0].delta.content)
    print("****************")