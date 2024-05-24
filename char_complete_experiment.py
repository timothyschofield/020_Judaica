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

# MODEL = "gpt-4-vision-preview"
MODEL = "gpt-4o" 

my_api_key = OPENAI_API_KEY
client = OpenAI(api_key=my_api_key)   # openai version 1.2.3

try:

    prompt = "Please read this text and return everything you can."
    
    url = "https://d2seqvvyy3b8p2.cloudfront.net/2ca62a26221a397d6942874b6ee7a225.jpg"

    print("========================== START OUTPUT =============================")


    ocr_output = client.chat.completions.create(
                                            model=MODEL,
                                            max_tokens=500,
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
                                        )
    
    # Works
    # json_input = ocr_output.choices[0].message.content
    # json_input = ocr_output.choices[0]
    json_input = ocr_output.json()
    print(json_input)
    
    print("========================== STOP OUTPUT =============================")   

except Exception as ex:
    print("Exception:", ex)






























