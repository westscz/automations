"""
Simply implementation of instagram bot to like media from tags

"""
from InstagramAPI import InstagramAPI
import time
import fire


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
    print(tag)
    ap.tagFeed(tag)
    i = ap.LastJson['items'][0]
    print(i)
    ap.like(i['id'])

    time.sleep(80)


def fire_cli(logins, password):
    ap = login(logins, password)
    like_new_from_tags(ap, ["35mm", 'filmisnotdead'], 100)


if __name__ == '__main__':
    fire.Fire(fire_cli)
