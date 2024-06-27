"""
File : main_validate_XML_from_csv.py

Author: Tim Schofield
Date: 28 May 2024

This starts with ChatGPT having generated ALTO XML from OCR in a single csv file - one line is one XML file
validate_XML_input_csv/Judaica_FULL_RUN_2024-06-03T19-03-08_full_278.csv (copied from the judaica_output folder)

The output is one XML file for each line in the input CSV
The XML is validated by this program and copied to the appropriate output folder:
seperate xml files
all_xml
valid_xml
invalid_xml

This is NOT the same folder structure as created by main_metadata.py


"""
from pathlib import Path 
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import xml.etree.ElementTree as ET
from helper_functions_judaica import validate_xml, get_file_timestamp


# FILE_NAME = "Judaica_2024-05-29T16-13-23_full_278.csv"
# FILE_NAME = "Judaica_ANALYSIS_2024-06-03T15-49-02_full_48.csv"
# FILE_NAME = "Judaica_ANALYSIS_Fix1_2024-06-03T17-47-45_full_48.csv"
FILE_NAME = "Judaica_FULL_RUN_2024-06-03T19-03-08_full_278.csv"


input_folder = Path("validate_XML_input_csv")
output_folder = Path(f"validate_XML_output/judaica_xml_ANALYSIS_{get_file_timestamp()}")
 
df = pd.read_csv(input_folder / FILE_NAME)

all_xml_root = Path(f"{output_folder}/all_xml/ocr")
valid_xml_root = Path(f"{output_folder}/valid_xml/ocr")
invalid_xml_root = Path(f"{output_folder}/invalid_xml/ocr")

all_xml_root.mkdir(parents = True, exist_ok = True)
valid_xml_root.mkdir(parents = True, exist_ok = True)
invalid_xml_root.mkdir(parents = True, exist_ok = True)

log_invalid = []
for index, row in df.iterrows():
    
    # https://lrfhec.maxcommunications.co.uk/LRF/JUDAICA/IMAGES/uni-ucl-heb-0015052/uni-ucl-heb-0015052-001/uni-ucl-heb-0015052-001-0001L.jpg
    url = row["source"]
    #print(f"****{url}****")
    
    if url == "none":  # why?
        continue

    url_list = url.split("/")
    # print(f"{url_list}")
    
    filename = Path(url_list[-1]).stem  # Get rid of the extension
    item_name = url_list[-2]
    section_name =  url_list[-3]
    # print(f"{section_name=}\n{item_name=}\n{filename=}\n")
    

    all_xml_path = Path(f"{all_xml_root}/{section_name}/{item_name}")
    valid_xml_path = Path(f"{valid_xml_root}/{section_name}/{item_name}")
    invalid_xml_path = Path(f"{invalid_xml_root}/{section_name}/{item_name}")
    
    all_xml_path.mkdir(parents = True, exist_ok = True)
    valid_xml_path.mkdir(parents = True, exist_ok = True)
    invalid_xml_path.mkdir(parents = True, exist_ok = True)
    
    # write everything whether valid or not to all_xml
    file_path_all = Path(f"{all_xml_path}/{filename}.xml")
    file_path_valid = Path(f"{valid_xml_path}/{filename}.xml")
    file_path_invalid = Path(f"{invalid_xml_path}/{filename}.xml") 
    #print(f"{file_path_all}")
    
    ocr_output = row["ocr content"]
    
    # 2% improvement
    ocr_output = ocr_output.replace("```xml", "")
    ocr_output = ocr_output.replace("```", "")
    
    # ensure all XML elements are properly closed and nested.
    
    
    
    # Do this again after fix-up
    # ocr_output = ocr_output.replace("```xml", "")
    # ocr_output = ocr_output.replace("```", "")
    
    with open(file_path_all, 'a') as the_file:
        the_file.write(ocr_output)
        
    is_valid, message = validate_xml(ocr_output)
    if is_valid:
        with open(file_path_valid, 'a') as the_file:
            the_file.write(ocr_output)
    else:
        # Invalid XML
        with open(file_path_invalid, 'a') as the_file:
            the_file.write(ocr_output)       
    
        this_invalid = dict()
        this_invalid["filename"] = file_path_invalid
        this_invalid["message"] = message
        this_invalid["xml"] = ocr_output
        log_invalid.append(this_invalid)

log_df = pd.DataFrame(log_invalid)
log_path = Path(f"{output_folder}/invalid_XML_log_{get_file_timestamp()}.csv")
with open(log_path, "w") as f:
    log_df.to_csv(f, index=False)

















