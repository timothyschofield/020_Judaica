"""
File : main_pmetadata.py

Author: Tim Schofield
Date: 30 May 2024

# I don't have authenication for an Max account
sheet_url = "https://docs.google.com/spreadsheets/d/1hmvDZgrYD2JA6NuI7lkSXwx7EzK_ENyDf5sDFmtNQlo/edit#gid=0"
csv_export_url = sheet_url.replace('/edit#gid=', '/export?format=csv&gid=')
pd.read_csv(csv_export_url)
print(pd)

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

Required file hierachy

uni-ucl-heb-0015052                             <<<<< this the book level
    
    uni-ucl-heb-0015052-000                     <<<<< this item folder contains NO XML
        *.jpg
        *.tiff
   
    uni-ucl-heb-0015052-001                     <<<<< this is the item level - contains NISC data for this item + data for all XML files in this item
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



# The front matter of the book
def get_nsic_line(this_row, index):
    image_name = this_row["Image name"]
    file_name = Path(image_name).stem
    
    itemimagefile1_element = f"<itemimagefile1>{file_name}</itemimagefile1>"
    imagenumber_element = f"<imagenumber>{index + 1}</imagenumber>"
    
    colour = this_row["Colour"]
    if type(colour).__name__ != "str": colour = "None"
    colour_element = f"<colour>{colour}</colour>"
        
    page_type = this_row["Page Type"]
    if type(page_type).__name__ != "str": page_type = "None"
    page_type_element = f"<pagetype>{page_type}</pagetype>"
        
    this_line = f"<itemimage>\n\t{itemimagefile1_element}{imagenumber_element}{colour_element}{page_type_element}\n</itemimage>"
    return  this_line

# Regular body of the book
def get_page_line(this_row, index):
    image_name = this_row["Image name"]
    file_name = Path(image_name).stem
    
    itemimagefile1_element = f"<itemimagefile1>{file_name}</itemimagefile1>"
    imagenumber_element = f"<imagenumber>{index + 1}</imagenumber>"
    
    colour = this_row["Colour"]
    if type(colour).__name__ != "str": colour = "None"
    colour_element = f"<colour>{colour}</colour>"
        
    page_type = this_row["Page Type"]
    if type(page_type).__name__ != "str": page_type = "None"
    page_type_element = f"<pagetype>{page_type}</pagetype>"
        
    this_line = f"<itemimage>\n\t{itemimagefile1_element}{imagenumber_element}{colour_element}{page_type_element}\n</itemimage>\n"
    return  this_line

# Read spreadsheet from sheet downloaded from Google drive
metadata_input = Path(f"metadata_input/METADATA - Proquest UCL - Judaica Batch 1 (C260_0003) - BENCHMARK.csv")

df = pd.read_csv(metadata_input)
# print(df)

metadata_output = Path(f"metadata_output/judaica_xml_{get_file_timestamp()}")

old_item_name = None
old_item_name_path = None
old_book_name = None
item_data = None
nisc_data = None

first_time_in = True


for index, row in df.iterrows():
    # uni-ucl-heb-0015052-000-0000B.jpg image_name
    # uni-ucl-heb-0015052-000-0000B     file_name
    # uni-ucl-heb-0015052-000           item_name
    # uni-ucl-heb-0015052               book_name
    
    image_name = row["Image name"]                  
    file_name = Path(image_name).stem         
    
    file_name_list = file_name.split("-")
    
    item_name = file_name_list[:-1]
    item_name = "-".join(item_name)                 
    
    book_name = file_name_list[:-2]
    book_name = "-".join(book_name)
    
    # We only need this to check if it is NISC data 000
    item_000 = file_name_list[-2:-1][0]

    # Make the folders
    book_name_path = Path(f"{metadata_output}/{book_name}")
    item_name_path = Path(f"{metadata_output}/{book_name}/{item_name}")
    if item_000 != "000":
        ocr_path = Path(f"{metadata_output}/{book_name}/{item_name}/ocr")
        ocr_path.mkdir(parents = True, exist_ok = True)
    
    book_name_path.mkdir(parents = True, exist_ok = True)
    item_name_path.mkdir(parents = True, exist_ok = True)
    
    if book_name != old_book_name:
        # We have encountered a new book
        old_book_name = book_name
        print(f"New book {book_name}")
        
        # NISC data is at the start of a new book and all images are 000
        if item_000 == "000":
            # Which it will be
            # print(f"Old NISC data: {nisc_data}\n")
            nisc_data = [get_nsic_line(row, index)]
    else:
        if item_000 == "000":
            nisc_data.append(get_nsic_line(row, index))
        else:
            if item_name != old_item_name:
                # We have encountered a new non NISC item
                
                # The first time in - before data has been accumulated - you don't want it to write
                # The second time in you want it to write the data that's been accumulated (the old data) to the old path
                print(f"New non NISC item {item_name=}\n")
                if first_time_in != True:
                    first_time_in = True
                    # print(f"Old item data {item_data=}\n")
                    file_to_write = f"{old_item_path}/{old_item_name}.xml"
                    print(f"{file_to_write=}")
                    
                    items_on_lines = '\n'.join(item_data)
                    with open(file_to_write, 'a') as the_file:
                        the_file.write(items_on_lines)
                
                first_time_in = False
                # So start the new item's data off by inserting the NISC data for that book
                item_data = []
                item_data.extend(nisc_data)
                item_data.append(get_page_line(row, index))

                old_item_name = item_name
                old_item_path = item_name_path
            else:
                # Not new item OR NISC data
                item_data.append(get_page_line(row, index))
    

# print(f"Last Old item data ****{item_data}****\n") 
file_to_write = f"{old_item_path}/{old_item_name}.xml"

print(f"{file_to_write=}")

items_on_lines = '\n'.join(item_data)
with open(file_to_write, 'a') as the_file:
     the_file.write(items_on_lines)
     
     
    
   
   
    
   























