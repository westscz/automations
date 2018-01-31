"""
download and clean all saved images on instagram account
"""

from InstagramAPI import InstagramAPI
import urllib.request
import json
import fire


class InstagramAPI2(InstagramAPI):
    def unsave(self, mediaId):
        data = json.dumps({'_uuid': self.uuid,
                           '_uid': self.username_id,
                           '_csrftoken': self.token,
                           'media_id': mediaId})
        return self.SendRequest('media/' + str(mediaId) + '/unsave/', self.generateSignature(data))


def login(username, password):
    api = InstagramAPI2(username, password)  # Instantiate the class
    api.login()  # Send a login request
    return api


def download_saved_media(x):
    x.getSelfSavedMedia()
    saved_media = x.LastJson
    saved_media_list = saved_media["items"]
    for m in saved_media_list:
        m_info = m.get('media')
        m_id = m_info['id']

        def xd(media_json):
            xd_id = media_json.get('id')
            ima = media_json.get('image_versions2')
            url = ima['candidates'][0]['url']
            urllib.request.urlretrieve(url, "{}.jpg".format(xd_id))

        print(m_id)
        image = m_info.get('image_versions2')
        if image:
            xd(m_info)
        else:
            for i in m_info.get('carousel_media'):
                xd(i)
        x.unsave(m_id)
    return saved_media["more_available"]


def fire_cli(logins, password):
    ap = login(logins, password)
    available = True
    while available:
        available = download_saved_media(ap)


if __name__ == '__main__':
    fire.Fire(fire_cli)
