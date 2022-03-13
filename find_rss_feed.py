import os

import requests
from lxml import html
import xml.etree.cElementTree as ET
from collections import namedtuple

from utills.directories import OUTPUT_DIRECTORY
from utills.logger import create_logger

FeedTuple = namedtuple("FeedTuple", ["title", "url", "feed"])

feed_postfix_list = [
    "/rss.xml",
    "/atom.xml",
    "/feed/atom",
    "/feed.atom",
    "/feed",
    "/feed.xml",
    "/feed.rss",
    "/atom/entries/",
    "/feed_rss.xml",
    "/rss",
    "/posts/rss.xml",
    "feeds/all_rss.xml",
]

LOGGER = create_logger(__name__)


def get_feed(url):
    content = requests.get(url)
    LOGGER.debug(content)
    if content.status_code != 200:
        LOGGER.warning("RSS is not available for {url}".format(url=url))
        return FeedTuple("", url, "")

    tree = html.fromstring(content.content)
    title = tree.xpath("//title").pop().text.strip()

    for feed_postfix in feed_postfix_list:
        rc = requests.get(url + feed_postfix).status_code
        if rc == 200:
            return FeedTuple(title, url, url + feed_postfix)

    rss = tree.xpath("//*[@type='application/rss+xml']")
    for i in rss:
        rss_url = i.attrib.get("href", None)
        if "/comments/" not in rss_url and requests.get(rss_url).status_code == 200:
            return FeedTuple(title, url, rss_url)

    LOGGER.warning("RSS is not available for {url}".format(url=url))
    return FeedTuple(title, url, "")


def create_template():
    root = ET.Element("opml", version="1.0")
    doc = ET.SubElement(root, "body")
    return root, doc


def add_subelement(doc, feed):
    ET.SubElement(
        doc,
        "outline",
        type="rss",
        text=feed.title,
        title=feed.title,
        xmlUrl=feed.feed,
        htmlUrl=feed.url,
    )
    return doc


def save(root):
    tree = ET.ElementTree(root)
    output_file = os.path.join(OUTPUT_DIRECTORY, "opml.xml")
    tree.write(output_file)


if __name__ == "__main__":
    root, doc = create_template()

    with open("rss.txt") as f:
        for rss in f:
            rss = rss.split().pop()
            LOGGER.info(f"Next website: {rss}")
            try:
                y = get_feed(rss)
                add_subelement(doc, y)
            except Exception as e:
                LOGGER.error(e)
                LOGGER.error(rss)

    save(root)
