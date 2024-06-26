"""
    Book.py
    e.g.
        uni-ucl-jud-0015052
        uni-ucl-jud-0015063

"""
from pathlib import Path

from NISC import NISC
from Item import Item

class Book:
    def __init__(self, index, row, name):
        self.index = index
        self.row = row
        self.name = name
        print(f"New Book: {self.name}")
         
        self.old_item_name = None
        self.current_item_name = None
        self.current_item = None
        self.items = dict() # A dictionary of Items indexed by the Item's name
        
        self.is_nisc = False
        self.nisc_data = None
        
    def update(self, index, row):
        self.index = index
        self.row = row
        
        this_item_name = self.get_item_name(row)
        if this_item_name != self.current_item_name:
            self.old_item_name = self.current_item_name
            self.current_item_name = this_item_name
            
            # If the last three characters of the current_item_name = "000"
            # Then this is NISC data associated with the Book not a new Item
            if self.current_item_name[-3:] == "000": self.is_nisc = True
            else: self.is_nisc = False
            
            # Create either a new NISC instance for this Book or
            # A new Item for the items list
            if self.is_nisc:
                self.nisc_data = NISC(index, row, self.current_item_name)
                self.nisc_data.update(index, row)
            else:
                self.current_item = Item(index, row, self.current_item_name)
                self.items[self.current_item_name] = self.current_item
                self.current_item.update(index, row) 
        else:
            if self.is_nisc:  
                self.nisc_data.update(index, row)
            else:
                self.current_item.update(index, row)

        
    def get_item_name(self, row):
        image_name = row["Image name"]                  
        file_name = Path(image_name).stem         
        
        file_name_list = file_name.split("-")
                        
        item_name = file_name_list[:-1]
        item_name = "-".join(item_name) 
        
        return item_name 
        
        