from xml.etree.ElementTree import Element, SubElement, tostring, Comment
from xml.dom import minidom


def create_links_root():
    return Element("DL")


def create_folder(root, name):
    term = SubElement(root, "DT")
    SubElement(term, "h3").text = name
    description_list = SubElement(root, "DL")
    return description_list


def create_term(name, url):
    name = name or url
    term = Element("DT")
    SubElement(term, "a", {"HREF": url}).text = name
    return term


def prettify(root):
    """Return a pretty-printed XML string for the Element."""
    rough_string = tostring(root, encoding="UTF-8")
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


def create_file(data, name):
    doctype = "<!DOCTYPE NETSCAPE-Bookmark-file-1>"
    root = Element("root")
    comment = Comment(
        """This is an automatically generated file.
        It will be read and overwritten.
        DO NOT EDIT! """
    )
    root.append(comment)

    head = SubElement(root, "head")
    SubElement(
        head,
        "meta",
        {"HTTP-EQUIV": "Content-Type", "CONTENT": "text/html; charset=UTF-8"},
    )
    SubElement(head, "title").text = "Bookmarks"

    body = SubElement(root, "body")
    SubElement(body, "h1").text = "Bookmarks Menu"
    body.extend(data)

    filename = f"{name}.html"
    with open(filename, "w") as f:
        result = doctype + str(prettify(root))
        f.write(result)

    return filename
