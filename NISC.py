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

class NISC:
    def __init__(self, index, row, name):
        self.index = index
        self.row = row
        self.name = name
        print(f"\tNew NISC data: {self.name}")
        
    def update(self, index, row):
        self.index = index
        self.row = row