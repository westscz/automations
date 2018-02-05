"""
Simply implementation of instagram bot to like media from tags

"""
from InstagramAPI import InstagramAPI
import time
import fire
import logging
import pprint

logger = logging.getLogger('spam_application')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)

pp = pprint.PrettyPrinter(indent=4)


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
    ap.tagFeed(tag)
    i = ap.LastJson['items'][0]
    # pp.pprint(i)
    ap.like(i['id'])

    time.sleep(80)


def comment_new_from_tag(ap, tag):
    logger.info("Comment new from tag: {}".format(tag))
    d = {"lomography":["Nice picture!"]}

    ap.tagFeed(tag)
    i = ap.LastJson['items'][0]

    # pp.pprint(i)
    ap.comment(i['id'], "I love this analog vibe :D")
    time.sleep(80)


def follow_new_from_tag_author(ap, tag):
    logger.info("Follow new from tag: {}".format(tag))
    ap.tagFeed(tag)
    i = ap.LastJson['items'][0]
    # pp.pprint(i)
    user = i.get("user").get("pk")
    print("www.instagram.com/{}".format(i.get("user").get("username")))
    ap.follow(user)
    time.sleep(100)
    ap.unfollow(user)

def fire_cli(logins, password):
    ap = login(logins, password)
    # comment_new_from_tag(ap, "lomography")
    # follow_new_from_tag_author(ap, "lomography")
    like_new_from_tags(ap, ["lomography", "35mm", 'filmisnotdead'], 156)


if __name__ == '__main__':
    fire.Fire(fire_cli)
