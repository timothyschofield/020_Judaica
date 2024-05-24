

import cv2
import base64
import time
import openai
from openai import OpenAI
import os
import requests
from db import OPENAI_API_KEY



try:
  my_api_key = OPENAI_API_KEY          
  client = OpenAI(api_key=my_api_key)
except Exception as ex:
    print("Exception:", ex)
    exit()


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

img = encode_image("image1.jpg")
    
PROMPT_MESSAGES = [
    {
        "role": "user",
        "content": [
            """These is a image of a page of a book. Get all the text from the image.""",
            *map(lambda x: {"image": x, "resize": 768}, [img]),
        ],
    },
]

params = {
    "model": "gpt-4-vision-preview",
    "messages": PROMPT_MESSAGES,
    "max_tokens": 500,
}

result = client.chat.completions.create(**params)
print(result.choices[0].message.content)















