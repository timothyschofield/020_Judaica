"""
File : main_judaica.py

Author: Tim Schofield
Date: 23 May 2024

"""
import openai
from openai import OpenAI

from db import OPENAI_API_KEY
from judaica_urls_batch1 import URL_PATH_LIST
from helper_functions_judaica import encode_image, get_file_timestamp, is_json, create_and_save_dataframe
import base64
import requests
import os
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time
from datetime import datetime

try:
  my_api_key = OPENAI_API_KEY          
  client = OpenAI(api_key=my_api_key)
except Exception as ex:
    print("Exception:", ex)
    exit()

MODEL = "gpt-4o"































