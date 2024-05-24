"""
test_contination.py

Tim Schofield
23 May 2024
    
"""
import os
import time
from openai import OpenAI
from db import OPENAI_API_KEY
import json

MODEL = "gpt-4o"

my_api_key = OPENAI_API_KEY
client = OpenAI(api_key=my_api_key)   # openai version 1.2.3

try:

    prompt = "Please read this text and return everything you can. Just retun what you see, do not make comments"
    
    url = "https://d2seqvvyy3b8p2.cloudfront.net/2ca62a26221a397d6942874b6ee7a225.jpg"

    print("========================== START OUTPUT =============================")

    model = MODEL
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": prompt
                },
                {
                    "type": "image_url",
                    "image_url":  {"url": url}
                }
            ]
        }  
    ]

    ocr_output1 = client.chat.completions.create(model=model, messages=messages, max_tokens=10) # max_tokens is too large: 6000.
    #print(ocr_output1)
    print("====================================================")
    ocr_json = ocr_output1.model_dump_json()            # a string in json format
    print(ocr_json)
    print("====================================================")
    ocr_json = ocr_json.replace("null", '"none"')   # a string in json format with no nulls
    print(ocr_json)
    print("====================================================")
    ocr_dict = eval(ocr_json)                        # convert from a string in json format to a Python dict
    print(ocr_dict)
    print("====================================================")
    print(ocr_dict["id"])
    
    
    
    
    
    
    
    
    
 
    print("========================== STOP OUTPUT =============================")   

except Exception as ex:
    print("Exception:", ex)