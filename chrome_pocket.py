# TODO: Check how and then get value from ENV / CONFIG / CLI

import json
import os
import subprocess

from pocket import Pocket, PocketException
from datetime import datetime
from tqdm import tqdm


def get_from_env(env_variable):
    return os.getenv(env_variable)


def get_pocket_client() -> Pocket:
    ACCESS_TOKEN = os.environ.get("POCKET_ACCESS_TOKEN", "")
    CONSUMER_KEY = os.environ.get("POCKET_CONSUMER_KEY", "")
    return Pocket(consumer_key=CONSUMER_KEY, access_token=ACCESS_TOKEN)


def get_last_articles(pocket: Pocket, count: int = 50):
    """ Fetch a list of articles"""
    result = None
    try:
        result = pocket.retrieve(offset=0, count=count)
    except PocketException as e:
        print(e)
    finally:
        return result.get("list")


def get_bookmarks_data(pocket_list):
    bookmarks_data = []
    for value in tqdm(pocket_list.values()):
        init = dict(
            type="url", name=value.get("resolved_title"), url=value.get("resolved_url")
        )
        if not init.get("url"):
            init["url"] = value.get("given_url")
        bookmarks_data.append(init)
        bookmarks_data.sort(key=lambda a: a.get("url"))
    return bookmarks_data


def prepare_data(bd):
    now = datetime.now()
    folder_name = f"P[{now.month:02d}:{now.day:02d}]"
    print(f"{folder_name} will be created")
    folder_dict = {"children": bd, "name": folder_name, "type": "folder"}

    return folder_dict


def add_data_to_chrome(data_to_add):
    path = get_chrome_path()
    data = get_data_from_chrome(path)
    bookmarks_bar = data.get("roots").get("bookmark_bar").get("children")
    bookmarks_bar.append(data_to_add)
    save_bookmarks_to_file(path, data)


def get_data_from_chrome(path):
    with open(path) as json_data:
        data = json.load(json_data)
    return data


def get_chrome_path(user="Default"):
    output = subprocess.check_output(["which", "chromium"]).decode("utf-8")
    env_home_path = os.getenv("HOME")
    if "snap" in output:
        return (
            f"{env_home_path}/snap/chromium/current/.config/chromium/{user}/Bookmarks"
        )
    else:
        return f"{env_home_path}/.config/chromium/{user}/Bookmarks"


def save_bookmarks_to_file(b_path, b_data):
    with open(b_path, "w") as fp:
        json.dump(b_data, fp)


def archive_posts(pocket, articles):
    for key in tqdm(articles.keys()):
        pocket.archive(key)
    pocket.commit()


if __name__ == "__main__":
    articles_number = 500
    p = get_pocket_client()
    articles_list = get_last_articles(p, articles_number)
    bd = get_bookmarks_data(articles_list)
    pd = prepare_data(bd)
    add_data_to_chrome(pd)
    archive_posts(p, articles_list)
