"""
    NISC.py

    NISC material is non-Item information andacts as a header for a Book
    It containes info on Back board, Front board, Spine etc.
    It is of variable length
    
    NISC material has two parts:
    The first part contains info to do with the outward appearance of the book:
    Back board, Front board, Spine, Head edge, Tail edge etc.
    The second part is infomation on Front and Back endpaper which cannot be seen when the book is closed
    but still counts as a part of NISC.
    Both these parts are of variable length - including, in some cases, zero length
    
    Items in a Book "share" NISC data. This means that when an Item's XML file is written, the same NISC data is
    copied in at the start of each XML file within a Book.
    
"""
from pathlib import Path
# The irst row is eaten by the init and subsequent rows are processed by update
# Call update at end of init
# Like wise for Book - we are missing the first row because the Book init is eating it
class NISC:
    def __init__(self, index, row, item_name):
        #self.index = index
        #self.row = row
        self.item_name = item_name
        #self.image_name = Path(self.row["Image name"]).stem
        self.first_part = dict()  
        self.second_part = dict()
        
        print(f"\tNew NISC item: {self.item_name}")
        #print(f"\t\t{self.image_name}")
        
    def update(self, index, row):
        #self.index = index
        #self.row = row
        image_name = Path(row["Image name"]).stem
        
        # The only distinction I can think of between first_part and second_part is 
        # that first_part images contain four zeros in the final section like "0000S" as opposed to three zeros like "0003L"
        end_bit = image_name.split("-")[-1]
        if "0000" in end_bit:
            # first_part
            print(f"\t\t{image_name} part 1")
            self.first_part[image_name] = row
        else:
            # second_part
            print(f"\t\t{image_name} part 2")
            self.second_part[image_name] = row

        
        
    