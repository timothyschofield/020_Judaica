"""
File : main_judaica_batch.py

Author: Tim Schofield
Date: 23 May 2024

"""
import openai
from openai import OpenAI
from db import OPENAI_API_KEY
from peru_url_list import URL_PATH_LIST
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
import json

try:
  my_api_key = OPENAI_API_KEY          
  client = OpenAI(api_key=my_api_key)
except Exception as ex:
    print("Exception:", ex)
    exit()

MODEL = "gpt-4o"   # max_tokens 4096

prompt = (
        f"Please OCR this document and make an ALTO XML file from the text"
        f"Go through the XML and replace 'String CONTENT' with 'SC*"
        f"Return only the XML, make no comments"
)

prompt = (
        f"Please OCR this document and extract the text and make into ALTO XML"
        f"The text is in old German and Hebrew"
        f"String tags should always contain CONTENT, HEIGHT, WIDTH, HPOS and VPOS attributes"
        f"Please return only the text, no not make comments"
        f"Do not wrap the returned text with backticks."    # it does it anyway sometimes
)

prompt = (
        f"Please OCR this document and extract the text"
        f"Please return only the text, no not make comments"
        f"Do not wrap the returned text with backticks."  
)


count = 0
project_name = "Judaica"
source_type = "url" # url or local

if source_type == "url":
  image_path_list = URL_PATH_LIST[:3]
else:
  image_folder = Path("input_gpt/")
  image_path_list = list(image_folder.glob("*.jpg"))

output_list = []

headers = {
  "Content-Type": "application/json",
  "Authorization": f"Bearer {my_api_key}"
}

# image_path_list = ["https://d2seqvvyy3b8p2.cloudfront.net/2ca62a26221a397d6942874b6ee7a225.jpg"]
print("####################################### START OUTPUT ######################################")
try:
  
  for image_path in image_path_list:

    error_message = "OK"

    print(f"\n### {image_path} ###\n")
    count+=1
    print(f"count: {count}")

    # "url" or "local"
    if source_type == "url":
      url_request = image_path
    else:
      base64_image = encode_image(image_path)
      url_request = f"data:image/jpeg;base64,{base64_image}"
      
    payload = {
        "model": MODEL,
        "logprobs": False,
        "messages": [
          {
            "role": "user",
            "content": [
              {
                "type": "text",
                "temperature": "0.2",
                "text": prompt
              },
              {
                "type": "image_url",
                "image_url": {"url": url_request}
              }
            ]
          }
        ],
        "max_tokens": 4096
    } 
    
    num_tries = 3
    for i in range(num_tries):
      ocr_output = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
      
      response_code = ocr_output.status_code
      if response_code != 200:
        print(f"======= 200 not returned. Trying request again number {i} ===========================")
      else:
        break
    ###### eo try requests three times
    
    ocr_dict = ocr_output.json()  # Turns JSON string into Python dict
    
    # If it refused to return 200 num_tries tries then report the error and move on
    if response_code != 200:
      error_message = f"ERROR {response_code}"
      
      dict_returned = dict()
      dict_returned["source"] = str(image_path)
      dict_returned["error"] = error_message
      dict_returned["ocr content"] = str(ocr_dict)
      dict_returned["finish_reason"] = 'none'
      dict_returned["usage"] = 'none'
      print("=====================================================")
      print(f"{str(ocr_output.json())}")
      print(f"======= 200 not returned. MOVE ON ==================")
      print("=====================================================")
    else:
      print("=====================================================")
      print(f"{response_code=}")
      print(ocr_dict)
      print("=====================================================")
  
      finish_reason = ocr_dict["choices"][0]["finish_reason"]
      usage = ocr_dict["usage"]
      print(f"{finish_reason=} {usage=}")
      
      dict_returned = dict()
      dict_returned["source"] = str(image_path)
      dict_returned["error"] = error_message
      dict_returned["ocr content"] = f'{ocr_dict["choices"][0]["message"]["content"]}'
      dict_returned["finish_reason"] = finish_reason
      dict_returned["usage"] = usage
    
    output_list.append(dict_returned)
    
  #################################### eo for loop

  time_stamp = get_file_timestamp()
  output_path_name = f"output_gpt/{project_name}_{time_stamp}-{count}.csv"

  create_and_save_dataframe(output_list, key_list_with_logging=[], output_path_name=output_path_name)

  print("####################################### END OUTPUT ######################################")


except openai.APIError as e:
  #Handle API error here, e.g. retry or log
  print(f"TIM: OpenAI API returned an API Error: {e}")
  pass

except openai.APIConnectionError as e:
  #Handle connection error here
  print(f"TIM: Failed to connect to OpenAI API: {e}")
  pass

except openai.RateLimitError as e:
  #Handle rate limit error (we recommend using exponential backoff)
  print(f"TIM: OpenAI API request exceeded rate limit: {e}")
  pass
  
# openai.BadRequestError











