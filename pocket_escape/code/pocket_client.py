import urllib
import webbrowser

import pocket
import requests

from logger import configure_logger


log = configure_logger(__name__)

BASE_URL = "https://getpocket.com"
REDIRECT_URL = "localhost"


def request_code(consumer_key):
    payload = {
        "consumer_key": consumer_key,
        "redirect_uri": REDIRECT_URL,
    }
    response = requests.post(f"{BASE_URL}/v3/oauth/request", payload)
    data = urllib.parse.parse_qs(response.text)
    return data["code"][0]


def request_access_token(consumer_key, code):
    payload = {
        "consumer_key": consumer_key,
        "code": code,
    }
    response = requests.post(f"{BASE_URL}/v3/oauth/authorize", payload)
    data = urllib.parse.parse_qs(response.text)
    return data["access_token"][0]


def request_authorization(code):
    url = f"{BASE_URL}/auth/authorize?request_token={code}&redirect_uri={REDIRECT_URL}"
    webbrowser.open(url, new=2)


def authenticate_pocket(consumer_key):
    log.info("ACCESS_TOKEN was not added, lets run interactive mode")
    code = request_code(consumer_key)
    request_authorization(code)
    input("Press enter after authorizing app...")
    return request_access_token(consumer_key, code)


def get_pocket_client(consumer_key, access_token) -> pocket.Pocket:
    if not access_token:
        access_token = authenticate_pocket(consumer_key)
        log.info(f"{access_token=}")

    return pocket.Pocket(consumer_key=consumer_key, access_token=access_token)
