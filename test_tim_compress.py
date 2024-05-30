"""
test_contination.py

Tim Schofield
23 May 2024
    
    not sure if this works - dead end
    
"""
import os
import time
from openai import OpenAI
from db import OPENAI_API_KEY
import json



MODEL = "gpt-4-32k"
MODEL = "gpt-4-Turbo-Vision"
MODEL = "gpt-4o"

my_api_key = OPENAI_API_KEY
client = OpenAI(api_key=my_api_key)   # openai version 1.2.3

try:

    prompt = (
        f"OCR this document and make ALTO XML."
        f"Go through the XML and replace 'String CONTENT' with '<S', 'TextLine>' with 'T>', delete all '\n'"
        f"Return only the XML."
)
    
    # problems   f"Go through the XML and replace '\n' by ' '"
    # f"Search the XML and replace 'String CONTENT' with '<S'."
    prompt = (
        f"OCR this document and make ALTO XML."
        f"Return only XML"
) 
    
    url = "https://lrfhec.maxcommunications.co.uk/LRF/JUDAICA/IMAGES/uni-ucl-heb-0015052/uni-ucl-heb-0015052-001/uni-ucl-heb-0015052-001-0033BIG.jpg"
    
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

    for i in range(1):
    
        ocr_output = client.chat.completions.create(model=model, messages=messages, max_tokens=4096) # max_tokens is too large: 6000.
        print(f"****{ocr_output}****")
        #print("====================================================")
        ocr_json = ocr_output.model_dump_json()             # a string in json format
        print(f"{ocr_json=}")
        print("====================================================")
        ocr_json = ocr_json.replace("null", '"none"')       # a string in json format with no nulls
        print(f"{ocr_json=}")
        print("====================================================")
        ocr_dict = json.loads(ocr_json)                     # convert from a string in json format to a Python dict
        print(f"{ocr_dict=}")
        print("====================================================")
        finish_reason = ocr_dict["choices"][0]["finish_reason"]
        usage = ocr_dict["usage"]
        print(f"{finish_reason=} {usage=}")
    print("========================== STOP OUTPUT =============================")

except Exception as ex:
    print("Exception:", ex)