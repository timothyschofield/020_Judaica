"""
File : test_is_xml_valid.py

Author: Tim Schofield
Date: 29 May 2024

<alto xmlns="http://www.loc.gov/standards/alto/ns-v4#">

"""

# pip install xmlschema
#import xmlschema
#my_schema = xmlschema.XMLSchema("http://www.loc.gov/standards/alto/ns-v4")

import xml.etree.ElementTree as ET

def validate_xml(xml_text):
    try:
        ET.fromstring(xml_text)
        return True, "The XML is well-formed."
    except ET.ParseError as e:
        return False, f"XML is not well-formed: {e}"


# valid
xml_text = """<alto>
  <String CONTENT="156"/>
  <String CONTENT="בין"/>
  <String CONTENT="אנטיפטרוס"/>
  </alto>"""

# invalid &amp;
xml_text = """<alto>
  <String CONTENT="in" />
  <String CONTENT="templiofidi" />
  <String CONTENT="s:&" />
  <String CONTENT="quæ" />
  <String CONTENT="iudæis" />
</alto>"""

# valid
xml_text = """<alto>
  <String CONTENT="floiss." />
  <String CONTENT="JehHozon" />
  <String CONTENT="📷📷📷📷 📷📷📷" />
  <String CONTENT="Es" />
</alto>"""

# invalid - no end tag
xml_text = """<alto>
  <String CONTENT="Christum"/>
  <String CONTENT="lunam equer">
</alto>"""

# invalid - &c. 
xml_text = """<alto>
  <String CONTENT="auffsteen" />
  <String CONTENT="&c." />
</alto>"""

# invalid - </>
xml_text = """<alto>
            <String CONTENT="credebat"</>
            <String CONTENT="else"/>
</alto>"""

is_valid, message = validate_xml(xml_text)
print(is_valid)
print(message)




