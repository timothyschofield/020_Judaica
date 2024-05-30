"""
File : main_pmetadata.py

Author: Tim Schofield
Date: 30 May 2024

# I don't have authenication for an Max account
sheet_url = "https://docs.google.com/spreadsheets/d/1hmvDZgrYD2JA6NuI7lkSXwx7EzK_ENyDf5sDFmtNQlo/edit#gid=0"
csv_export_url = sheet_url.replace('/edit#gid=', '/export?format=csv&gid=')
pd.read_csv(csv_export_url)
print(pd)

Required file hierachy

uni-ucl-heb-0015052                             <<<<< this the book level
    
    uni-ucl-heb-0015052-000                     <<<<< this item folder contains the NISC xml
        uni-ucl-heb-0015052-000.xml             <<<<< the NISC xml
        
    uni-ucl-heb-0015052-001                     <<<<< this is the item level
        uni-ucl-heb-0015052-001.xml             <<<<< this is the metadata file for item 001
        *.jpg
        *.tiff
        ocr
            uni-ucl-heb-0015052-001-0001L.xml
            uni-ucl-heb-0015052-001-0001R.xml
            ...
    ...   
        
One xml metadata file per item
Each metadata file refers to each of the xml data files in that item AND the files in NISC
"""
from pathlib import Path 
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import io
import xml.etree.ElementTree as ET
from helper_functions_judaica import validate_xml, get_file_timestamp
import requests


"""
Image name
Image url link	
Image	
Page Type	
Colour	
Page number	
illustration_type_1	
instances_of_1	
illustration_type_2	
instances_of_2	
illustration_type_3	
instances_of_3	
illustration_type_4	
instances_of_4	
illustration_type_5	
instances_of_5	
translation

"""
# Read spreadsheet from sheet downloaded from Google drive
metadata_input = Path(f"metadata_input/METADATA - Proquest UCL - Judaica Batch 1 (C260_0003) - BENCHMARK.csv")

df = pd.read_csv(metadata_input)
# print(df)

metadata_output = Path(f"metadata_output")































