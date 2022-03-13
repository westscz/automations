import os
from dataclasses import dataclass

import requests
from lxml import html
from lxml.html import HtmlElement
from collections import namedtuple

from utills.netscape_file import NetscapeFileUrl
from utills.directories import OUTPUT_DIRECTORY
from tqdm import tqdm

HTMLAttr = namedtuple("HTMLAttr", ["xpath", "attr"])
URLData = namedtuple("URLData", ["name", "album", "source"])

PARSER_MAP = {}


def add_parser(cls):
    PARSER_MAP[cls.name] = cls


@dataclass
@add_parser
class DeviantartSource:
    name = "deviantart"
    album_name = HTMLAttr("//meta[@property='og:site_name']", "content")
    data_source = HTMLAttr("//img[@class='dev-content-full ']", "src")
    img_name = HTMLAttr("//img[@class='dev-content-full ']", "alt")


def get_data(data: HtmlElement, htmlattr: HTMLAttr):
    item = data.xpath(htmlattr.xpath)[0]
    data = item.attrib
    data["text"] = item.text
    return data[htmlattr.attr]


def get_scraper(url: str):
    website = url.split("/")[2].split(".")[-2]
    return PARSER_MAP[website]


def get_output_name(url_data: URLData):
    extension = url_data.source.rsplit(".")[-1]
    return (
        f"{url_data.album}-{url_data.name}.{extension}".lower()
        .replace(" ", "_")
        .replace("/", "_")
        .replace(":", "_")
    )


def get_data_for_url(url: str) -> URLData:
    content = requests.get(url)
    tree = html.fromstring(content.content)
    parser = get_scraper(url)
    data_source = get_data(tree, parser.data_source)
    album = get_data(tree, parser.album_name)
    name = get_data(tree, parser.img_name)
    return URLData(name, album, data_source)


def download_file(url: str, output_dir: str):
    urldata = get_data_for_url(url)
    output_name = get_output_name(urldata)
    response = requests.get(urldata.source, stream=True)
    output_file = f"{output_dir}/{output_name}"
    with open(output_file, "wb") as handle:
        for data in response.iter_content():
            handle.write(data)


if __name__ == "__main__":
    bookmarks_file = "/home/jarek/Documents/bookmarks_5_16_19.html"
    directory_name = "inspiration"
    urls = [
        u.get("url") for u in NetscapeFileUrl(bookmarks_file).get_folder(directory_name)
    ]

    output_directory = os.path.join(OUTPUT_DIRECTORY, directory_name)
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for url in tqdm(urls):
        try:
            download_file(url, output_directory)
        except IndexError:
            print(f"Error while downloading '{url}', object will be not downloaded ")
        except requests.exceptions.InvalidSchema:
            print(f"WTF: {url}")
