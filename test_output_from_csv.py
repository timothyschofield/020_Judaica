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
from urllib.parse import urlparse

"""
Required file hierachy

uni-ucl-heb-0015052                             <<<<< call this the section level
    uni-ucl-heb-0015052-001                     <<<<< this is the item level
        uni-ucl-heb-0015052-001-0001L.xml
        uni-ucl-heb-0015052-001-0001R.xml   
        ...    
"""

FILE_NAME = "TIM METADATA - Proquest UCL - Judaica Batch 1 (C260_0003) - BENCHMARK.csv"
csv_folder = Path("input_gpt")

dest_folder = Path("output_xml_folders")

df = pd.read_csv(csv_folder / FILE_NAME)
# print(df) 


for index, row in df.iterrows():
    
    # https://lrfhec.maxcommunications.co.uk/LRF/JUDAICA/IMAGES/uni-ucl-heb-0015052/uni-ucl-heb-0015052-001/uni-ucl-heb-0015052-001-0001L.jpg
    url = row["Image url link"]
   
    if url == "none": 
        continue

    print(f"{url}")
    
    url_list = url.split("/")
    
    # print(f"{url_list}")
    
    filename = url_list[-1]
    item_name = url_list[-2]
    section_name =  url_list[-3]
    
    print(f"{section_name=}\n{item_name=}\n{filename=}\n")

    
    
    exit()

























