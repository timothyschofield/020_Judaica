"""
test_contination.py

Tim Schofield
23 May 2024
    
Probably a bad idea
    
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

    prompt = "Please read this text and return everything you can. Just return what you see, do not make comments"
    
    url = "https://d2seqvvyy3b8p2.cloudfront.net/2ca62a26221a397d6942874b6ee7a225.jpg"
    url = "https://lrfhec.maxcommunications.co.uk/LRF/JUDAICA/IMAGES/uni-ucl-heb-0015052/uni-ucl-heb-0015052-001/uni-ucl-heb-0015052-001-0033L.jpg"
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

    page_length = 200
    overlap_size = 20
    
    ocr_output1 = client.chat.completions.create(model=model, messages=messages, max_tokens=page_length) # max_tokens is too large: 6000.
    #print(ocr_output1)
    #print("====================================================")
    ocr_json = ocr_output1.model_dump_json()            # a string in json format
    #print(ocr_json)
    #print("====================================================")
    ocr_json = ocr_json.replace("null", '"none"')       # a string in json format with no nulls
    #print(ocr_json)
    #print("====================================================")
    ocr_dict = eval(ocr_json)                           # convert from a string in json format to a Python dict
    #print(ocr_dict)
    print("====================================================")
    finish_reason = ocr_dict["choices"][0]["finish_reason"]

    if finish_reason == "length":
        content = ocr_dict["choices"][0]["message"]["content"]
        print(f"*first {page_length}\n****{content}****\n")
        list_content = content.split(" ")
        #print(list_content)
        
        overlap_in_list = list_content[-overlap_size:]
        #print(overlap_in_list)
    
        overlap_as_str = " ".join(overlap_in_list)
        #print(f"\n****{overlap_as_str}****\n")   
    
        prompt = f"Continue from '{overlap_as_str}'"
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
        
        print("====================================================")
        ocr_output2 = client.chat.completions.create(model=model, messages=messages, max_tokens=page_length)
        #print(ocr_output2)
        #print("====================================================")
        ocr_json = ocr_output2.model_dump_json()            # a string in json format
        #print(ocr_json)
        #print("====================================================")
        ocr_json = ocr_json.replace("null", '"none"')       # a string in json format with no nulls
        #print(ocr_json)
        #print("====================================================")
        ocr_dict = eval(ocr_json)                           # convert from a string in json format to a Python dict
        #print(ocr_dict)
        print("====================================================")
        content = ocr_dict["choices"][0]["message"]["content"]
        print(f"*second {page_length}\n****{content}****\n")
 
 
 
    print("========================== STOP OUTPUT =============================")   

except Exception as ex:
    print("Exception:", ex)