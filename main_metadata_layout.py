"""

A helper file for main_metadata.py
Helps with the XML layout

"""

from pathlib import Path 
import math

# The front matter of the book
def get_nsic_line(this_row, index):
    image_name = this_row["Image name"]
    file_name = Path(image_name).stem
    
    itemimagefile_element = f"<itemimagefile1>{file_name}</itemimagefile1>"
    imagenumber_element = f"<imagenumber>{index}</imagenumber>"
    
    order = 0
    if file_name[-2:] == "1L": order = 1
    if file_name[-2:] == "2R": order = 2
    if file_name[-2:] == "3L": order = 3
    if file_name[-2:] == "4R": order = 4
    
    #print(file_name[-2:])
    
    order_element = f"<order>{order}</order>"
    
    colour = this_row["Colour"]
    if type(colour).__name__ != "str": colour = "None"
    colour_element = f"<colour>{colour}</colour>"
        
    page_type = this_row["Page Type"]
    if type(page_type).__name__ != "str": page_type = "None"
    page_type_element = f"<pagetype>{page_type}</pagetype>"
        
    this_line = f"<itemimage>\n\t{itemimagefile_element}{order_element}{imagenumber_element}{colour_element}{page_type_element}\n</itemimage>"
    return  this_line


####################################################################
# Regular body of the book
def get_page_line(this_row, index, book_index):
    image_name = this_row["Image name"]
    file_name = Path(image_name).stem
    
    itemimagefile_element = f"<itemimagefile1>{file_name}</itemimagefile1>"
    imagenumber_element = f"<imagenumber>{index}</imagenumber>"
    
    order = book_index # because of the weird NISC numbering
   
    order_element = f"<order>{order}</order>"
    
    colour = this_row["Colour"]
    if type(colour).__name__ != "str": colour = "None"
    colour_element = f"<colour>{colour}</colour>"
        
    page_type = this_row["Page Type"]
    if type(page_type).__name__ != "str": page_type = "None"
    page_type_element = f"<pagetype>{page_type}</pagetype>"
        
    # This is the basic line - all tabs included even if value "None"
    this_line = f"{itemimagefile_element}{order_element}{imagenumber_element}{colour_element}{page_type_element}"
    
    ###########################################################################################
    # elements below here are not included in the output if they have no value
    page_number = this_row["Page number"]  
    if type(page_number).__name__ != "str": 
        order_label_element = ""
    else:
        order_label_element = f"<orderlabel>{page_number}</orderlabel>"
    
    this_line = f"{this_line}{order_label_element}"
    
    #######################
    # illustration_type_1 to illustration_type_5
    all_illustration_type = ""
    for i in range(1, 6):
        
        illustration_type = this_row[f"illustration_type_{i}"]  
        instances_of = this_row[f"instances_of_{i}"]
        
        if type(illustration_type).__name__ != "str": 
            illustration_type = ""
        else:
            if math.isnan(instances_of) != True:
                instances_of = int(instances_of)
            illustration_type = f'<pagecontent number="{instances_of}">{illustration_type}</pagecontent>'
            
        all_illustration_type = f"{all_illustration_type}{illustration_type}"
    
    this_line = f"{this_line}{all_illustration_type}"


    #######################
    translation = this_row["translation"]  
    if type(translation).__name__ != "str": 
        translation = ""
    else:
        translation = f"<translation>{translation}</translation>"
    
    this_line = f"{this_line}{translation}"

    # Wrap it in tags
    this_line = f"<itemimage>\n\t{this_line}\n</itemimage>\n"
    
    return  this_line


####################################################################
"""

"""
def get_front_tags(item_name):
    front_tags = f"<rec>\n\n<itemid>{item_name}</itemid>\n\n<subscription>\n\t<unit>unpublished</unit>\n\t<country>uni</country>\n</subscription>\n\n<itemimagefiles>\n"
    return front_tags

"""
    use item_name as index into rec_data.csv
    https://docs.google.com/spreadsheets/d/1hmBUjLONWi2XRhz45K3lJuNRNXr3IPJR/edit?gid=2000716270#gid=2000716270
    <title>{Title}</title>
    <author_name>{Author}</author_name>
    <startdate>{Year of Publication}</startdate>
    <enddate>{Year of Publication}</enddate>
    <displaydate>{extract the year}</displaydate>



"""
def get_back_tags(item_name):
    back_tags = (   f"</itemimagefiles>\n\n<rec_search>\n<pqid>{item_name}</pqid>\n"
                    f"<title>unknown</title>\n"
                    f"<author_main>\n\t<author_name>unknown</author_name>\n\t<author_corrected>unknown</author_corrected>\n\t<author_uninverted>unknown</author_uninverted>\n</author_main>\n"
                    f"<startdate>16170101</startdate>\n"
                    f"<enddate>16171231</enddate>\n"
                    f"<displaydate>1617</displaydate>\n"
                    f"<publisher_printer>unknown</publisher_printer>\n"
                    f"<pagination>unknown</pagination>\n"
                    f"<source_library>unknown</source_library>\n"
                    f"<illustrations>\n"
                    f"\t<illustration>Illuminated lettering</illustration>\n"
                    f"\t<illustration>Illustrated page borders</illustration>\n"
                    f"</illustrations>\n"
                    f"\n</rec_search>\n\n"
                    
                    f"<linksec>\n"
                    
                    f"<link>\n"
                    f"\t<linktitle>Title here</linktitle>\n"
                    f"\t<linkid>Link ID here</linkid>\n"
                    f"</link>\n"
                    
                    f"<link>\n"
                    f"\t<linktitle>Title here</linktitle>\n"
                    f"\t<linkid>Link ID here</linkid>\n"
                    f"</link>\n"
                    
                    f"</linksec>\n"
                    
                    
                    f"\n</rec>"
        
                    )
    
    return back_tags











