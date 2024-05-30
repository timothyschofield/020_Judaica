"""
File : test_read_xml_and_fix.py

Author: Tim Schofield
Date: 30 May 2024

from openai import OpenAI 
client = OpenAI() 
file = client.files.create( file=open("file.pdf", "rb"), purpose="fine-tune" ) 
client = OpenAI() completion = client.chat.completions.create( model="gpt-4-1106",
        messages=[ {"role": "system", "content": "You are a helpful assistant that can read PDFs."}, 
                   {"role": "user", "content": f"Extract the text from the 3rd page from {file.id}"} ] ) 
print(completion.choices[0].message) 

"""
import openai
from openai import OpenAI
from db import OPENAI_API_KEY

from pathlib import Path 
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import xml.etree.ElementTree as ET
from helper_functions_judaica import validate_xml, get_file_timestamp

try:
  my_api_key = OPENAI_API_KEY          
  client = OpenAI(api_key=my_api_key)
except Exception as ex:
    print("Exception:", ex)
    exit()

MODEL = "gpt-4o"   # max_tokens 4096

xml_source_folder = Path(f"output_xml_folders/judaica_xml_test_source/invalid_xml")

xml_source_list = list(xml_source_folder.glob("*/*/*.xml"))
# print(xml_source_list)
print(f"num of invalid files = {len(xml_source_list)}")


for xml_file in xml_source_list:
    
    with open(xml_file, 'r') as file_handle:
        xml_text = file_handle.read()

        # print(xml_text)
        
        # Doesn't work
        messages = [ 
                {
                    "role": "user", 
                    "content": f"Extract the first <TextLine> from {file_handle}"
                }    
            ]
        
        output = client.chat.completions.create(model=MODEL, messages=messages, max_tokens=4096) # max_tokens is too large: 6000.
        print(output)
        
        
        
        
        
        exit()




























