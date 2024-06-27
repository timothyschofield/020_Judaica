"""
    NISC.py

    NISC material is non-item metadata like a header for a Book
    It containes info on Back board, Front board, Spine etc.
    It is af variable length
    
    NISC material has two parts:
    The first part contains info to do with the outward appearance of the book:
    Back board, Front board, Spine, Head edge, Tail edge etc.
    The second part is infomation on Front and Back endpaper which cannot be seen when the book is closed
    but is still counts as a part of NISC.
    Both these parts are of variable length - including, in some cases, zero length
    
"""
from pathlib import Path
# The irst row is eaten by the init and subsequent rows are processed by update
# Call update at end of init
# Like wise for Book - we are missing the first row because the Book init is eating it
class NISC:
    def __init__(self, index, row, item_name):
        self.index = index
        self.row = row
        self.item_name = item_name
        
        self.image_name = Path(self.row["Image name"]).stem
        print(f"\tNew NISC data: {self.item_name}")
        print(f"\t\t{self.image_name}")
        
    def update(self, index, row):
        self.index = index
        self.row = row
        self.image_name = Path(self.row["Image name"]).stem
        print(f"\t\t{self.image_name}")