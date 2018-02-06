"""
Simply implementation of instagram bot to like media from tags

"""
from InstagramAPI import InstagramAPI
import time
import fire
import logging
import pprint
import yaml

logger = logging.getLogger('spam_application')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)

pp = pprint.PrettyPrinter(indent=4)


class YamlConfig:
    tags = None
    comments = None

    def __init__(self):
        with open("config.yml", 'r') as ymlfile:
            self.cfg = yaml.load(ymlfile)
        self.__dict__.update(self.cfg)
        pp.pprint(self.cfg)


def login(username, password):
    api = InstagramAPI(username, password)  # Instantiate the class
    api.login()  # Send a login request
    return api


def like_new_from_tags(ap, tags_list, likes_number):
    number = int(likes_number / len(tags_list))
    for i in range(0, likes_number):
        for tag in tags_list:
            like_new_from_tag(ap, tag)


def like_new_from_tag(ap, tag):
    logger.info("Like new from tag: {}".format(tag))
    i = get_media_from_tag(ap, tag, newest=False)
    show_info_for_media_item(i)
    ap.like(i['id'])

    time.sleep(80)


def comment_new_from_tag(ap, tag):
    logger.info("Comment new from tag: {}".format(tag))
    d = {"lomography":["Nice picture!"]}

    i = get_media_from_tag(ap, tag, last_count=-1, newest=False)
    show_info_for_media_item(i)
    ap.comment(i['id'], "I love this analog vibe :D")
    time.sleep(80)


def follow_new_from_tag_author(ap, tag):
    logger.info("Follow new from tag: {}".format(tag))
    i = get_media_from_tag(ap, tag, newest=False)
    show_info_for_media_item(i)
    user = i.get("user").get("pk")
    print("www.instagram.com/{}".format(i.get("user").get("username")))
    ap.follow(user)
    time.sleep(100)
    ap.unfollow(user)


def get_media_from_tag(ap, tag, last_count=20, newest=True):
    ap.tagFeed(tag)
    if newest:
        return ap.LastJson['items'][0]
    else:
        like_count = 0
        item = None
        for x in ap.LastJson['items'][:last_count]:
            if x['like_count'] > like_count and not x['has_liked']:
                item = x
                like_count = x['like_count']
        return item


def show_info_for_media_item(item):
    full_name = item.get("user").get("full_name")
    media_id = item.get('code')
    url = "https://instagram.com/p/{}".format(media_id)
    logger.info("{fn}: {url}".format(fn=full_name, url=url))


def fire_cli(logins, password):
    config = YamlConfig()


    ap = login(logins, password)
    comment_new_from_tag(ap, "lomography")
    follow_new_from_tag_author(ap, "lomography")
    like_new_from_tags(ap, config.tags, 156)
    # get_media_from_tag(ap, "lomography")


if __name__ == '__main__':
    fire.Fire(fire_cli)
