"""
Get URLs from evernote note
xml is starting with <en-note id="en-note" class="editable" g_editable="true" contenteditable="true">
"""
import re
import xml.etree.ElementTree as ET

tree = ET.parse("evernote.xml")
root = tree.getroot()
for child in root:
    if child.findall(".//span"):
        text = "# " + child.findall(".//span")[0].text
        print(text)
        print("")
    elif child.findall(".//a"):
        text = child.findall(".//a")[0].text
        print(re.sub("(\\n| +)", " ", text))
        print("<{}>".format(child.findall(".//a")[0].attrib["href"]))
        print("")
    else:
        print(child.findall(".//"))
