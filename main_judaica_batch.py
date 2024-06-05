"""
File : main_judaica_batch.py

Author: Tim Schofield
Date: 23 May 2024

"""
import openai
from openai import OpenAI
from db import OPENAI_API_KEY

# from urls_generates_invalid_xml import URL_PATH_LIST
from urls_judaica_batch1 import URL_PATH_LIST

from helper_functions_judaica import encode_image, get_file_timestamp, is_json, create_and_save_dataframe, make_payload
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
  



# MODEL = "gpt-4-vision-preview" # 4096 - I've tested it
MODEL = "gpt-4o"   # max_tokens 4096


prompt = (
        f"Please OCR this document and extract the text"
        f"Please return only the text, no not make comments"
        f"Do not wrap the returned text with backticks."  
)

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
        f"Do not wrap the returned text with backticks."   
)

prompt = (
        f"OCR this document and extract the text and make into ALTO XML"
        f"The text is in a mixture of Gothic German, Latin and Hebrew"
        f"For String tags only include the CONTENT attribute"     
        f"A CONTENT attribute must only contain one word"                   # dumping word and Hebrew
        f"If you can find no text return '<alto> <!-- No text --> </alto>'"
        f"Return only the text do not make comments"
        f"Do not wrap the returned text with backticks"   
)

prompt = (
        f"OCR this document and extract the text and make into ALTO XML"
        f"The text is in a mixture of Gothic German, Latin and Hebrew"
        f"For String tags only include the CONTENT attribute"  
        f"Words in a line should be contained within a TextLine tag"
        f"Each word in a TextLine should be contained within a seperate String tag"
        f"If you can find no text return '<alto> <!-- No text --> </alto>'"
        f"Return only the text do not make comments"
        f"Do not wrap the returned text with backticks"
)

################################# XML
prompt = (
        f"OCR this document and extract the text and make into ALTO XML"
        f"The text is in a mixture of Gothic German, Latin and Hebrew"
        f"For String tags only include the CONTENT attribute"  
        f"Words in a line should be contained within a TextLine tag"
        f"Each word in a TextLine should be contained within a seperate String tag"
        
        f"Ensure all XML elements are properly closed and nested"
        f"Ampersand ('&') must be replaced with &amp;"
        f"String tags must be terminated by '/>'"
        f"String CONTENT must be surrounded by matching quotes"
        
        f"If you can find no text return '<alto> <!-- No text --> </alto>'"
        f"Return only the text do not make comments"
        f"Do not wrap the returned text with backticks"
)


############################### JSON
prompt = (
          f"OCR this document and extract the text and make into ALTO JSON"
          f"The text is in a mixture of Gothic German, Latin and Hebrew"
          f"Do not return OCRProcessing infomation"
          f"Do not return HPOS VPOS WIDTH or HEIGHT information"
          f"One word per Content attribute"
          f"If you can find no text return {{'alto' :'No text'}}"
          f"Return only the text do not make comments"
)

prompt = (
          f'OCR this document and extract the text and make into ALTO JSON'
          f'The text is in a mixture of Gothic German, Latin and Hebrew'

          f'Generate a valid ALTO JSON object with the following structure: {{ "Page": {{ "Page": {{ "ID": "1", "Width": 2000, "Height": 3000, "PrintSpace": {{ "Height": 2800, "Width": 1800, "TopMargin": 100, "LeftMargin": 100 }}, "TextBlock": [{{ "ID": "TB1", "HPOS": 100, "VPOS": 100, "WIDTH": 1800, "HEIGHT": 400, "TextLine": [{{ "ID": "TL1", "Text": "Sample text line 1", "HPOS": 100, "VPOS": 100, "WIDTH": 1800, "HEIGHT": 50 }}, {{ "ID": "TL2", "Text": "Sample text line 2", "HPOS": 100, "VPOS": 150, "WIDTH": 1800, "HEIGHT": 50 }}] }}] }} }}'

          f'If you can find no text return {{"alto" :"No text"}}'
          f'Return only the text do not make comments'
)




 
judaica_input_folder = "judaica_input"
judaica_output_folder = "judaica_output"
project_name = "Judaica_ALTO_JSON"

source_type = "url" # url or local
count = 0

batch_size = 20 # saves every batch_size
time_stamp = get_file_timestamp()
experiment = "ALTO_JSON"

if source_type == "url":
  image_path_list = URL_PATH_LIST
else:
  image_folder = Path(f"{judaica_input_folder}/")
  image_path_list = list(image_folder.glob("*.jpg"))

output_list = []

headers = {
  "Content-Type": "application/json",
  "Authorization": f"Bearer {my_api_key}"
}


print("####################################### START OUTPUT ######################################")
try:
  
  for image_path in image_path_list[:50]:

    error_message = "OK"

    print(f"\n### {image_path} ###")
    count+=1
    print(f"count: {count}")

    # "url" or "local"
    if source_type == "url":
      url_request = image_path
    else:
      base64_image = encode_image(image_path)
      url_request = f"data:image/jpeg;base64,{base64_image}"
      
    payload = make_payload(MODEL, prompt, url_request, 4096)
    
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
      # ERROR 200 not returned
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
      # OK 200 returned

      print(f"{response_code=}")
      print(ocr_dict)
      finish_reason = ocr_dict["choices"][0]["finish_reason"]
      usage = ocr_dict["usage"]
      print(f"{finish_reason=} {usage=}")
      print("=====================================================")
      
      # Check the last characters are "</alto>"
      
      dict_returned = dict()
      dict_returned["source"] = str(image_path)
      dict_returned["error"] = error_message
      
      
      xml_string = f'{ocr_dict["choices"][0]["message"]["content"]}'
      
      
      
      
      
      dict_returned["ocr content"] = xml_string
      
      dict_returned["finish_reason"] = finish_reason
      dict_returned["usage"] = usage
    
    output_list.append(dict_returned)
    
    if count % batch_size == 0:
      print(f"WRITING BATCH:{count}")  
      output_path_name = f"{judaica_output_folder}/{project_name}_{time_stamp}_{experiment}_{count}.csv"
      create_and_save_dataframe(output_list=output_list, key_list_with_logging=[], output_path_name=output_path_name)
    
  #################################### eo for loop

  print(f"WRITING BATCH:{count}")  
  output_path_name = f"{judaica_output_folder}/{project_name}_{time_stamp}_{experiment}_{count}.csv"
  create_and_save_dataframe(output_list=output_list, key_list_with_logging=[], output_path_name=output_path_name)
 

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











