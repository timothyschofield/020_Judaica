"""

"""
from pathlib import Path 
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
from urllib.parse import urlparse

"""

uni-ucl-heb-0015052
    uni-ucl-heb-0015052-001
        uni-ucl-heb-0015052-001-0001L.xml
        uni-ucl-heb-0015052-001-0001R.xml   
        ...    
"""

FILE_NAME = "Judaica_many_words_2024-05-27T17-58-00-6.csv"
csv_folder = Path("output_gpt")

dest_folder = Path("xml_dest")

df = pd.read_csv(csv_folder / FILE_NAME)
# print(df) 

# https://lrfhec.maxcommunications.co.uk/LRF/JUDAICA/IMAGES/uni-ucl-heb-0015052/uni-ucl-heb-0015052-001/uni-ucl-heb-0015052-001-0001L.jpg
for index, row in df.iterrows():
    
    url = row["source"]
    # print(f"{url}")
    
    url_parsed = urlparse(url)
    file_name = os.path.basename(url_parsed.path)
    print(file_name)
    
    exit()

























