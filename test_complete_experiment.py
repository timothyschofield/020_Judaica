"""
char_complete_experiment.py

Tim Schofield
08 November 2023
    
OpenAI API Experiments

Given an image URL it OCRs it

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

    # messages=[{"role": "user", "content": "Say this is a test"}]

    ocr_output = client.chat.completions.create(model=model, messages=messages, stream=True, max_tokens=500)
    
    output_list = []
    for chunk in ocr_output:
        # print(chunk)
        this_chunk = chunk.choices[0].delta.content
        # print(this_chunk)
        
        output_list.append(str(this_chunk))
        # print("****************")
   
    print("==============================================")
    print("num chunks:", len(output_list))
    print("".join(output_list))

    print("========================== STOP OUTPUT =============================")   

except Exception as ex:
    print("Exception:", ex)






























