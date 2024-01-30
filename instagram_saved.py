from instagrapi import Client
import requests
import fire

from pathlib import Path


def log_in(username, password):
    client = Client()
    client.delay_range = [1, 3]
    file = username+"_session.json"
    try:
        session = client.load_settings(file)
    except FileNotFoundError:
        session = None
    if session:
        try:
            client.set_settings(session)
            client.login(username, password)
            client.get_timeline_feed()
        except Exception:
            old_session = client.get_settings()
            client.set_settings({})
            client.set_uuids(old_session["uuids"])
            client.login(username, password)
            client.dump_settings(file)
    else:
        client.login(username, password)
        client.dump_settings(file)
    return client


def download_media(post, filepath):
    if post.image_versions2:
        url = post.image_versions2["candidates"][0]["url"]
    else:
        url = post.thumbnail_url
    path = filepath.with_suffix('.jpg')
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(path, 'wb') as f:
            for chunk in r:
                f.write(chunk)

def download_video(post, filepath):
    url = post.video_url
    path = filepath.with_suffix('.mp4')
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(path, 'wb') as f:
            for chunk in r:
                f.write(chunk)

def download_description(post, filepath):
    path = filepath.with_suffix('.txt')
    with open(path, 'w') as f:
        f.write(post.caption_text)


def download_post_media(api, post, root_dir):
    username = post.user.username
    filename = f"{username.replace('.', '')}_{post.code}_{post.id}"
    (root_dir/username).mkdir(parents=True, exist_ok=True)
    filepath = root_dir/username/filename
    print(filename)

    if post.image_versions2:
        download_media(post, filepath)
    elif post.resources:
        for i, resource in enumerate(post.resources):
            filepath = root_dir/username/(filename+str(i))
            download_media(api.media_info(resource.pk), filepath)
    elif post.video_url:
        download_video(post, filepath)
    else:
        raise Exception("Unexpected type", post.product_type, filepath)
    download_description(post, filepath)


def unsave_media(api, post, collection):
    collection_pk = api.collection_pk_by_name(collection.name)
    if collection_pk == 'ALL_MEDIA_AUTO_COLLECTION':
        collection_pk = 0
    api.media_unsave(post.id, collection_pk)


def collection_medias_by_name(api, name):
    try:
        return api.collection_medias_by_name(name)
    except Exception: #CollectionNotFound
        return []


def download_saved_media(api, unsave=True, folder_name="output"):
    root_dir = Path(folder_name)
    for collection in api.collections():
        while posts := collection_medias_by_name(api, collection.name):
            for post in posts:
                download_post_media(api, post, root_dir)
                if unsave:
                    unsave_media(api, post, collection)


class InstagramCLI:
    """ InstagramCLI is used to dowload all your saved data on instagram and cleanup saved section"""

    def use_env(self):
        instagram_login = "niepaczenawet" #os.environ.get("INSTAGRAM_LOGIN", "niepaczenawet")
        instagram_password = "$#oh#sST4mAn6J" #os.environ.get("INSTAGRAM_PASSWORD", "$#oh#sST4mAn6J")
        if instagram_login and instagram_password:
            self.run(instagram_login, instagram_password)
        else:
            print(
                "Set environment variables to use this:"
                'export INSTAGRAM_LOGIN="login"'
                'export INSTAGRAM_PASSWORD="pass"'
            )

    def run(self, instagram_login, instagram_password):
        api = log_in(instagram_login, instagram_password)
        available = True
        while available:
            available = download_saved_media(api, folder_name=instagram_login)

    def dump(self, instagram_login, instagram_password, user):
        api = log_in(instagram_login, instagram_password)
        raise NotImplemented("Function is not available")


if __name__ == "__main__":
    fire.Fire(InstagramCLI, name="InstagramSaved")
