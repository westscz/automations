"""
Script to move pocket files to netscape formated file which you can
export in webbrowser
"""

import argparse
import os
import datetime

from netscape import create_links_root, create_folder, create_file, create_term
from logger import configure_logger
from pocket_client import get_pocket_client

from tqdm import tqdm


log = configure_logger(__name__)


def configure_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--access-token",
        default=os.environ.get("POCKET_ACCESS_TOKEN", ""),
        metavar="POCKET_ACCESS_TOKEN",
    )
    parser.add_argument(
        "--consumer-key",
        default=os.environ.get("POCKET_CONSUMER_KEY", ""),
        metavar="POCKET_CONSUMER_KEY",
    )
    parser.add_argument("--articles-number", default=500)
    parser.add_argument("--archive", default=True)
    return parser


def get_last_articles(pocket, count: int = 500):
    """Fetch a list of articles"""
    try:
        result = pocket.retrieve(offset=0, count=count)
        articles = result.get("list")
    except Exception as e:
        log.exception(e)
        return {}
    return {
        k: v
        for k, v in sorted(articles.items(), key=lambda e: e[1].get("given_url", ""))
    }


def archive_posts(pocket, articles):
    for key in tqdm(articles.keys()):
        pocket.archive(key)
    pocket.commit()


def save_articles_to_netscape_file(articles):
    today = datetime.date.today()
    folder_name = f"POCKET_ESCAPE[{today}]"
    root = create_links_root()
    folder = create_folder(root, folder_name)

    uniq = set()
    for article in articles.values():
        given_title = article.get("given_title")
        resolved_title = article.get("resolved_title")

        url = article.get("given_url")
        title = given_title or resolved_title

        if url not in uniq:
            folder.append(create_term(title, url))
            uniq.add(url)
        else:
            log.info(f"Duplicate: {url}")

    return create_file(root, today)


def main():
    parser = configure_parser()
    args = parser.parse_args()

    pocket = get_pocket_client(args.consumer_key, args.access_token)
    articles = get_last_articles(pocket, args.articles_number)
    if not articles:
        log.info("No items to dump")
        return
    path = save_articles_to_netscape_file(articles)
    log.info("Saved in %s", path)


if __name__ == "__main__":
    main()
