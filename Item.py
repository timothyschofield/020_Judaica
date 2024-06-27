"""
    Item.py

    Contains information of on the regualr (non NISC) pages of a Book

"""

class Item:
    def __init__(self, index, row, name):
        self.index = index
        self.row = row
        self.name = name
        print(f"\tNew Item: {self.name}")
        
    def update(self, index, row):
        self.index = index
        self.row = row