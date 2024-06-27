"""
    File: main_metadata_v2.py
    Author: Tim Schofield
    Date: 27 June 2024   
    
    This uses a double scan - first we collect the data from the input speadsheet and in a hierachical data structure of Books, Items, NISCs and Pages.
    Once we have the structured data we can go through it and write out the metadata xml in a sensible fashion.

    This is specificaly required to address the problem of linked data, where items in a book/volume need to know about one another's existance.
    A single scan is no good for this, because the earlyer items in a book/volume do not know about later items because the data has not been collected yet.

    OOPs approch required

    Required file hierachy

    uni-ucl-jud-0015052                             <<<<< this the book or volume level
        
        uni-ucl-jud-0015052-000                     <<<<< this item folder contains no XML but there is an ocr folder
            ocr
            *.jpg
            *.tiff
    
        uni-ucl-jud-0015052-001                     <<<<< this is the item level - contains NISC data for this item + data for all XML files in this item
            uni-ucl-jud-0015052-001.xml             <<<<< this is the metadata file for item 001
            *.jpg
            *.tiff
            ocr
                uni-ucl-jud-0015052-001-0001L.xml
                uni-ucl-jud-0015052-001-0001R.xml
                ...
                
         uni-ucl-jud-0015052-002                    <<<<<<< sceond item in Volume
            uni-ucl-jud-0015052-002.xml             <<<<< this is the metadata file for item 002
            
            etc.
             
        ... 

"""
from pathlib import Path 
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
from helper_functions_judaica import get_file_timestamp

from Book import Book


class App:
    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path
        self.df_metadata = None
        
        self.old_book_name = None
        self.current_book_name = None
        self.current_book = None
        self.books = dict() # A dictionary of Books indexed by the Book's name
        
        if os.path.exists(self.input_path) != True:
            print(f"ERROR: {self.input_path} file does not exits")
            exit()
        else:
            print(f"READING: {self.input_path}")       
        
        self.df_metadata = pd.read_csv(self.input_path)

        # Iterate through the metadata csv
        # And create a structured representation of the csv
        for index, row in self.df_metadata.iloc[0:].iterrows(): 
            self.update(index, row)

    """
    """        
    def update(self, index, row):        

        this_book_name = self.get_book_name(row)
        
        if this_book_name != self.current_book_name:
            self.old_book_name = self.current_book_name
            self.current_book_name = this_book_name
            
            self.current_book = Book(index, row, self.current_book_name)
            self.books[self.current_book_name] = self.current_book
            # print(f"Number of books: {len(self.books)}")
        else:
            self.current_book.update(index, row)
            

    """
    """
    def get_book_name(self, row):
            image_name = row["Image name"]                  
            file_name = Path(image_name).stem         
            
            file_name_list = file_name.split("-")
                           
            book_name = file_name_list[:-2]
            book_name = "-".join(book_name)
            
            return book_name



"""
    Create an instance of the App Class
    and pass it the input and output paths for the data
"""
input_folder = Path(f"metadata_input")
input_file = Path(f"METADATA - Proquest UCL - Judaica Batch 1 (C260_0003) - BENCHMARK.csv")
input_path = Path(f"{input_folder}/{input_file}")

output_folder = Path(f"metadata_output")
output_file = Path(f"judaica_xml_{get_file_timestamp()}")
output_path = Path(f"{output_folder}/{output_file}")

app1 = App(input_path=input_path, output_path=output_path)

























