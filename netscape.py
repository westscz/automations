"""
Utils to work with netscape bookmark files
"""

from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from xml.dom import minidom


def prettify(elem):
    """Return a pretty-printed XML string for the Element."""
    rough_string = tostring(elem, "utf-8")
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


def create_root():
    top = Element("DL")
    root = SubElement(top, "p")
    return root


def create_folder(root, name):
    headline = SubElement(root, "DT")
    headline = SubElement(root, "H3")
    headline.text = name
    head_list = SubElement(root, "DL")
    return head_list


def add_link(folder, name, url):
    link = SubElement(folder, "p")
    link = SubElement(folder, "DT")
    link = SubElement(folder, "A", {"HREF": url})
    link.text = name


def create_file(root):
    header = """
    <!DOCTYPE NETSCAPE-Bookmark-file-1>
    <!-- This is an automatically generated file.
        It will be read and overwritten.
        DO NOT EDIT! -->
    <META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
    <TITLE>Bookmarks</TITLE>
    <H1>Bookmarks Menu</H1>
    """
    from datetime import date

    with open(f"{date.today()}.html", "w") as f:
        result = header + str(prettify(root))
        f.write(result)
