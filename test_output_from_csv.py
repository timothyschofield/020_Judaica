"""
File : test_output_from_csv.py

Author: Tim Schofield
Date: 28 May 2024

print('scheme  :', url_parsed.scheme)
print('netloc  :', url_parsed.netloc)
print('path    :', url_parsed.path)
print('params  :', url_parsed.params)
print('query   :', url_parsed.query)
print('fragment:', url_parsed.fragment)
print('username:', url_parsed.username)
print('password:', url_parsed.password)
print('hostname:', url_parsed.hostname, '(netloc in lower case)')
print('port    :', url_parsed.port)


"""
from pathlib import Path 
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import xml.etree.ElementTree as ET
from helper_functions_judaica import validate_xml

"""
Required file hierachy

uni-ucl-heb-0015052                             <<<<< call this the section level
    uni-ucl-heb-0015052-001                     <<<<< this is the item level
        uni-ucl-heb-0015052-001-0001L.xml
        uni-ucl-heb-0015052-001-0001R.xml   
        ...    
"""

FILE_NAME = "Judaica_2024-05-27-No_Floats-return-ALTO-001-261.csv"
csv_folder = Path("input_gpt")

dest_folder = Path("output_xml_folders")

df = pd.read_csv(csv_folder / FILE_NAME)
# print(df) 


for index, row in df.iterrows():
    
    # https://lrfhec.maxcommunications.co.uk/LRF/JUDAICA/IMAGES/uni-ucl-heb-0015052/uni-ucl-heb-0015052-001/uni-ucl-heb-0015052-001-0001L.jpg
    url = row["source"]
    # print(f"{url}")
    
    if url == "none": 
        continue

    url_list = url.split("/")
    # print(f"{url_list}")
    
    filename = Path(url_list[-1]).stem  # Get rid of the extension
    item_name = url_list[-2]
    section_name =  url_list[-3]
    # print(f"{section_name=}\n{item_name=}\n{filename=}\n")
    
    
    all_xml_path = Path(f"{dest_folder}/all_xml/{section_name}/{item_name}")
    valid_xml_path = Path(f"{dest_folder}/valid_xml/{section_name}/{item_name}")
    invalid_xml_path = Path(f"{dest_folder}/invalid_xml/{section_name}/{item_name}")
    
    all_xml_path.mkdir(parents = True, exist_ok = True)
    valid_xml_path.mkdir(parents = True, exist_ok = True)
    invalid_xml_path.mkdir(parents = True, exist_ok = True)
    
    # write everything whether valid or not to all_xml
    file_path_all = Path(f"{all_xml_path}/{filename}.xml")
    file_path_valid = Path(f"{valid_xml_path}/{filename}.xml")
    file_path_invalid = Path(f"{invalid_xml_path}/{filename}.xml") 
    #print(f"{file_path_all}")
    
    ocr_output = row["ocr content"]
    
    with open(file_path_all, 'a') as the_file:
        the_file.write(ocr_output)
        
    is_valid, message = validate_xml(ocr_output)
    if is_valid:
        with open(file_path_valid, 'a') as the_file:
            the_file.write(ocr_output)
    else:
         with open(file_path_invalid, 'a') as the_file:
            the_file.write(ocr_output)       
    
    
    
        
























