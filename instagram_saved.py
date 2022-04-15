from InstagramAPI import InstagramAPI as InstaAPI
from urllib.request import urlretrieve
import requests
import json
import fire
import os
from tqdm import tqdm
from time import sleep

from pathlib import Path

class InstagramAPI(InstaAPI):
    def unsave(self, mediaId):
        data = json.dumps(
            {
                "_uuid": self.uuid,
                "_uid": self.username_id,
                "_csrftoken": self.token,
                "media_id": mediaId,
            }
        )
        return self.SendRequest(
            "media/" + str(mediaId) + "/unsave/", self.generateSignature(data)
        )


def log_in(username, password):
    api = InstagramAPI(username, password)
    api.login()
    return api


def create_directory(directory_path):
    try:
        os.stat(directory_path)
    except:
        os.mkdir(directory_path)


def download_saved_media(api, unsave=True, folder_name="output"):
    create_directory(folder_name)
    sleep(10)
    api.getSelfSavedMedia()
    saved_media = api.LastJson
    saved_media_list = saved_media["items"]

    for m in saved_media_list:
        print(m)
        m_info = m.get("media")

        m_id = m_info["id"]
        username = m_info.get("user").get("username")
        create_directory(os.path.join(folder_name, username))

        def download_media(media_json):
            media_id = media_json.get("id")
            url = media_json.get("image_versions2").get("candidates")[0].get("url")
            path = os.path.join(
                    "output", username, "{}_{}.jpg".format(username, media_id)
                )
            r = requests.get(url, stream=True)
            if r.status_code == 200:
                with open(path, 'wb') as f:
                    for chunk in r:
                        f.write(chunk)

        image = m_info.get("image_versions2")

        if image:
            download_media(m_info)
        else:
            for i in m_info.get("carousel_media"):
                download_media(i)
        if unsave:
            api.unsave(m_id)
    return saved_media["more_available"]


class InstagramCLI:
    """ InstagramCLI is used to dowload all your saved data on instagram and cleanup saved section"""

    def use_env(self):
        instagram_login = os.environ.get("INSTAGRAM_LOGIN", "")
        instagram_password = os.environ.get("INSTAGRAM_PASSWORD", "")
        if instagram_login and instagram_password:
            self._run(instagram_login, instagram_password)
        else:
            print(
                "Set environment variables to use this:"
                'export INSTAGRAM_LOGIN="login"'
                'export INSTAGRAM_PASSWORD="pass"'
            )

    def run(self, instagram_login, instagram_password):
        self._run(instagram_login, instagram_password)

    def _run(self, instagram_login, instagram_password):
        api = log_in(instagram_login, instagram_password)
        available = True
        while available:
            available = download_saved_media(api)

    def dump(self, instagram_login, instagram_password, user):
        api = log_in(instagram_login, instagram_password)
        id = 0
        api.getUserFeed(id)
        m_info = api.LastJson

        def download_media(media_json):
            media_id = media_json.get("id")
            url = media_json.get("image_versions2").get("candidates")[0].get("url")
            path = os.path.join(
                    "output", user, "{}_{}.jpg".format(user, media_id)
                )
            r = requests.get(url, stream=True)
            if r.status_code == 200:
                with open(path, 'wb') as f:
                    for chunk in r:
                        f.write(chunk)

        for item in m_info['items']:

            image = item.get("image_versions2")

            if image:
                print('one')
                download_media(item)
            else:
                for i in item.get("carousel_media"):
                    print(i)
                    download_media(i)

        if m_info['more_available']:
            next_max_id = m_info['next_max_id']

        # x = api.getProfileData(user)

        import pdb;pdb.set_trace()


if __name__ == "__main__":
    fire.Fire(InstagramCLI, name="InstagramSaved")

# TODO: Error 429 calm down for a minute man!
