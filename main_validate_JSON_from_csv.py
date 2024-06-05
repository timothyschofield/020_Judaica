"""
File : main_validate_JSON_from_csv.py

Author: Tim Schofield
Date: 04 June 2024

This starts with asking ChatGPT to generate ALTO JSON from OCR - NOT ALTO XML 

Takes the csv JSON output of the main_judaica_batch and seperates it into three folders
in seperate JSON files

It then takes the valid ALTO JSON turns it into ALTO XML and save them as seperate XML fiels

Folders
all_json
valid_json
invalid_json

valid_xml
"""
from pathlib import Path 
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import xml.etree.ElementTree as ET
from helper_functions_judaica import validate_xml, get_file_timestamp, is_json

FILE_NAME = "Judaica_ALTO_JSON_2024-06-05T08-51-58_ALTO_JSON_50.csv"

input_folder = Path("validate_JSON_input_csv")
output_folder = Path(f"validate_JSON_output")

df = pd.read_csv(input_folder / FILE_NAME)
# print(df)

time_stamp = get_file_timestamp()
valid_json = []
invalid_json = []
valid_count = 0
invalid_count = 0
count = 0

for index, row in df.iterrows():

    json_returned = row["ocr content"]


   

    # 1) Turn to raw with "r" to avoid the escaping quotes problem
    json_returned = fr'{json_returned}'
    # print(f"content****{json_returned}****")
    
    # 2) Sometimes null still gets returned, even though I asked it not to
    if "null" in json_returned: 
        json_returned = json_returned.replace("null", "'none'")
    
    # 3) Occasionaly the whole of the otherwise valid JSON is returned with surrounding square brackets like '[{"text":"tim"}]'
    # or other odd things like markup '''json and ''' etc.
    # This removes everything prior to the opening "{" and after the closeing "}"
    
    open_brace_index = json_returned.find("{")
    json_returned = json_returned[open_brace_index:]
    close_brace_index = json_returned.rfind("}")
    json_returned = json_returned[:close_brace_index+1]
    
    row["ocr content"] = json_returned

    if is_json(json_returned):
        valid_json.append(row)
        valid_count = valid_count + 1
    else:
        invalid_json.append(row)
        invalid_count = invalid_count + 1

print(f"{valid_count=} {invalid_count=}")

valid_json_df = pd.DataFrame(valid_json)
invalid_json_df = pd.DataFrame(invalid_json)

valid_json_path = Path(f"{output_folder}/valid_JSON_{time_stamp}.csv")
invalid_json_path = Path(f"{output_folder}/invalid_JSON_{time_stamp}.csv")

with open(valid_json_path, "w") as f:
    valid_json_df.to_csv(f, index=False)

with open(invalid_json_path, "w") as f:
    invalid_json_df.to_csv(f, index=False)




















