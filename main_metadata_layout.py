from pathlib import Path 


# The front matter of the book
def get_nsic_line(this_row, index):
    image_name = this_row["Image name"]
    file_name = Path(image_name).stem
    
    itemimagefile1_element = f"<itemimagefile1>{file_name}</itemimagefile1>"
    imagenumber_element = f"<imagenumber>{index + 1}</imagenumber>"
    
    colour = this_row["Colour"]
    if type(colour).__name__ != "str": colour = "None"
    colour_element = f"<colour>{colour}</colour>"
        
    page_type = this_row["Page Type"]
    if type(page_type).__name__ != "str": page_type = "None"
    page_type_element = f"<pagetype>{page_type}</pagetype>"
        
    this_line = f"<itemimage>\n\t{itemimagefile1_element}{imagenumber_element}{colour_element}{page_type_element}\n</itemimage>"
    return  this_line



# Regular body of the book
def get_page_line(this_row, index):
    image_name = this_row["Image name"]
    file_name = Path(image_name).stem
    
    itemimagefile1_element = f"<itemimagefile1>{file_name}</itemimagefile1>"
    imagenumber_element = f"<imagenumber>{index + 1}</imagenumber>"
    
    colour = this_row["Colour"]
    if type(colour).__name__ != "str": colour = "None"
    colour_element = f"<colour>{colour}</colour>"
        
    page_type = this_row["Page Type"]
    if type(page_type).__name__ != "str": page_type = "None"
    page_type_element = f"<pagetype>{page_type}</pagetype>"
        

    # This is the basic line - all tabs included even if value "None"
    this_line = f"{itemimagefile1_element}{imagenumber_element}{colour_element}{page_type_element}"
    
    ###########################################################################################
    # elements below here are not included in the output if they have no value
    page_number = this_row["Page number"]  
    if type(page_number).__name__ != "str": 
        order_label_element = ""
    else:
        order_label_element = f"<orderlabel>{page_number}</orderlabel>"
    
    this_line = f"{this_line}{order_label_element}"
    
    #################
    
    
    
    
    # Wrap it in tags
    this_line = f"<itemimage>\n\t{this_line}\n</itemimage>\n"
    
    return  this_line



















