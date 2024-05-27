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
import json

try:
  my_api_key = OPENAI_API_KEY          
  client = OpenAI(api_key=my_api_key)
except Exception as ex:
    print("Exception:", ex)
    exit()

# MODEL = "gpt-4-vision-preview"    # max_tokens 4096
MODEL = "gpt-4o"                    # max_tokens 4096

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
        f"The script is in Hebrew"
)
#### OLD

count = 0
project_name = "Judaica"

source_type = "local" # url or local
if source_type == "url":
  image_path_list = URL_PATH_LIST[32:33]
else:
  image_folder = Path("input_gpt/")
  image_path_list = list(image_folder.glob("*.jpg"))


print(f"Number to process:{len(image_path_list)}")


""""
image_path = "https://lrfhec.maxcommunications.co.uk/LRF/JUDAICA/IMAGES/uni-ucl-heb-0015052/uni-ucl-heb-0015052-001/uni-ucl-heb-0015052-001-0033L.jpg"
image_path = "https://d2seqvvyy3b8p2.cloudfront.net/2ca62a26221a397d6942874b6ee7a225.jpg"
# Half page old german
image_path = "https://lrfhec.maxcommunications.co.uk/LRF/JUDAICA/IMAGES/uni-ucl-heb-0015052/uni-ucl-heb-0015052-001/uni-ucl-heb-0015052-001-0011L.jpg"
image_path = "input_gpt/uni-ucl-heb-0015052-001-0011L.jpg"
image_path = "input_gpt/Lot of Hebrew uni-ucl-heb-0015091-001-0019L.jpg"
image_path = "input_gpt/genesis-930x520.jpg"
"""

output_list = []
print("####################################### START OUTPUT ######################################")
try:
  
  for image_path in image_path_list:
  # for i in range(3):
 
    print(f"\n### {image_path} ###\n")
    count+=1
    print(f"count: {count}")

    # "url" or "local"
    if source_type == "url":
      url_request = image_path
    else:
      base64_image = encode_image(image_path)
      url_request = f"data:image/jpeg;base64,{base64_image}"

    messages=[
        {
            "role": "user",
            "logprobs": False,
            "content": [
                {
                    "type": "text",
                    "temperature": 0.2,
                    "text": prompt
                },
                {
                    "type": "image_url",
                    "image_url":  {"url": url_request}
                }
            ]
        }  
    ]

    ocr_output = client.chat.completions.create(model=MODEL, messages=messages, max_tokens=4096)
    
    print("====================================================")
    print(ocr_output)
    ocr_json = ocr_output.model_dump_json()             # a string in json format
    print("========================")
    ocr_json = ocr_json.replace("null", '"none"')       # a string in json format with no nulls
    ocr_dict = json.loads(ocr_json)                     # convert from a string in json format to a Python dict
    print(ocr_dict)
    print("====================================================")
    finish_reason = ocr_dict["choices"][0]["finish_reason"]
    usage = ocr_dict["usage"]
    print(f"{finish_reason=} {usage=}")
    print("====================================================")
    
    dict_returned = dict()
    dict_returned["source"] = str(image_path)
    dict_returned["ocr content"] = f'==== START ================ uni-ucl-heb-0015052-001-0011L ===============================\n{ocr_dict["choices"][0]["message"]["content"]}'
    dict_returned["finish_reason"] = finish_reason
    dict_returned["usage"] = usage
    
    output_list.append(dict_returned)
    
    # How to handle
    #response_code = ocr_output.status_code
    #print(f"ocr_output response_code:{response_code}")

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












