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


class InstagramBot(object):
    def __init__(self):
        self.IAPI = None

    def login(self, username, password):
        self.IAPI = InstagramAPI(username, password)  # Instantiate the class
        self.IAPI.login()  # Send a login request

    def like_new_from_tags(self, tags_list, likes_number):
        number = int(likes_number / len(tags_list))
        for i in range(0, likes_number):
            for tag in tags_list:
                self.like_new_from_tag(tag)

    def like_new_from_tag(self, tag):
        logger.info("Like new from tag: {}".format(tag))
        i = self.get_media_from_tag(tag, newest=False)
        self.show_info_for_media_item(i)
        self.IAPI.like(i['id'])

        time.sleep(80)

    def comment_new_from_tag(self, tag):
        logger.info("Comment new from tag: {}".format(tag))
        d = {"lomography": ["Nice picture!"]}

        i = self.get_media_from_tag(tag, last_count=-1, newest=False)
        self.show_info_for_media_item(i)
        self.IAPI.comment(i['id'], "I love this analog vibe :D")
        time.sleep(80)

    def follow_new_from_tag_author(self, tag):
        logger.info("Follow new from tag: {}".format(tag))
        i = self.get_media_from_tag(tag, newest=False)
        self.show_info_for_media_item(i)
        user = i.get("user").get("pk")
        print("www.instagram.com/{}".format(i.get("user").get("username")))
        self.IAPI.follow(user)
        time.sleep(100)
        self.IAPI.unfollow(user)

    def get_media_from_tag(self, tag, last_count=20, newest=True):
        self.IAPI.tagFeed(tag)
        if newest:
            return self.IAPI.LastJson['items'][0]
        else:
            like_count = 0
            item = None
            for x in self.IAPI.LastJson['items'][:last_count]:
                if x['like_count'] > like_count and not x['has_liked']:
                    item = x
                    like_count = x['like_count']
            return item

    def show_info_for_media_item(self, item):
        full_name = item.get("user").get("full_name")
        media_id = item.get('code')
        url = "https://instagram.com/p/{}".format(media_id)
        logger.info("{fn}: {url}".format(fn=full_name, url=url))


def fire_cli(user_login, user_password):
    config = YamlConfig()

    ibot = InstagramBot()
    ibot.login(user_login, user_password)
    ibot.comment_new_from_tag("lomography")
    ibot.follow_new_from_tag_author("lomography")
    ibot.like_new_from_tags(config.tags, 156)
    # get_media_from_tag(ap, "lomography")


if __name__ == '__main__':
    fire.Fire(fire_cli)
