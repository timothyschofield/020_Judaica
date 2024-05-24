"""
File : main_judaica.py

Author: Tim Schofield
Date: 23 May 2024


"""
import openai
from openai import OpenAI

from db import OPENAI_API_KEY
from judaica_urls_batch1 import URL_PATH_LIST
from helper_functions_judaica import encode_image, get_file_timestamp, is_json, create_and_save_dataframe
import base64
import requests
import os
from pathlib import Path 
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time
from datetime import datetime

try:
  my_api_key = OPENAI_API_KEY          
  client = OpenAI(api_key=my_api_key)
except Exception as ex:
    print("Exception:", ex)
    exit()

# MODEL = "gpt-4-vision-preview"    # max_tokens 4096
MODEL = "gpt-4o"                    # max_tokens 4096

prompt = (
        f"Please OCR this document and make an ALTO XML file from the text."
        f"Return only the XML, make no comments."
)

count = 0
project_name = "Judaica"

source_type = "url" # url or offline
if source_type == "url":
  image_path_list = URL_PATH_LIST[30:40]
else:
  image_folder = Path("input_gpt/")
  image_path_list = list(image_folder.glob("*.jpg"))

print(f"Number to process:{len(image_path_list)}")

print("####################################### START OUTPUT ######################################")
try:
  
  for image_path in image_path_list:
 
    print(f"\n### {image_path} ###\n")
    count+=1
    print(f"count: {count}")

    if source_type == "url":
      url_request = image_path
    else:
      base64_image = encode_image(image_path)
      url_request = f"data:image/jpeg;base64,{base64_image}"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {my_api_key}"
    }
    
    # payload is in JSON format
    payload = {
        "model": MODEL,
        "logprobs": False,

         
        "messages": [
          {
            "role": "user",
            "content": [
              {
                "type": "text",
                "temperature": 0.2,
                "stream": True,
                "text": prompt
              },
              {
                "type": "image_url",
                "image_url": {
                  "url": url_request
                }
              }
            ]
          }
        ],
        "max_tokens": 4096   # 4096 is the  max_tokens that can be returned in gpt-4o
    } 

    ocr_output = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    response_code = ocr_output.status_code
    print(f"ocr_output response_code:{response_code}")
    print(f"{str(ocr_output.json())}")


  #################################### eo for loop


except openai.APIError as e:
  #Handle API error here, e.g. retry or log
  print(f"OpenAI API returned an API Error: {e}")
  pass

except openai.APIConnectionError as e:
  #Handle connection error here
  print(f"Failed to connect to OpenAI API: {e}")
  pass

except openai.RateLimitError as e:
  #Handle rate limit error (we recommend using exponential backoff)
  print(f"OpenAI API request exceeded rate limit: {e}")
  pass

print("####################################### END OUTPUT ######################################")











