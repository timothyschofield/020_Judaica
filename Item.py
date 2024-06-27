"""
    Item.py

"""

class Item:
    def __init__(self, index, row, name):
        self.index = index
        self.row = row
        self.name = name
        print(f"New Item: {self.name}")
        
    def update(self, index, row):
        self.index = index
        self.row = row