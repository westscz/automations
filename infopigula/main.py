import asyncio
import os
import pickle
import time
from enum import Enum
from pathlib import Path

import discord
import requests
from dotenv import load_dotenv
from markdownify import markdownify

load_dotenv()

default_headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:97.0) Gecko/20100101 Firefox/97.0",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://infopigula.pl/",
    "Origin": "https://infopigula.pl",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "Connection": "keep-alive",
}

INFOPIGULA_EMAIL = os.getenv("INFOPIGULA_EMAIL")
INFOPIGULA_PASS = os.getenv("INFOPIGULA_PASS")

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_GUILD = os.getenv("DISCORD_GUILD")
DISCORD_CHANNEL = os.getenv("DISCORD_CHANNEL")

DISC_MESSAGE_LIMIT = 2000


class GroupTarget(Enum):
    poland = 2
    world = 3
    russia = 50


def get_authorization():

    url = "https://api.infopigula.pl/user/login"
    headers = {
        **default_headers,
        "Content-Type": "application/json",
    }
    payload = {"_format": "json"}
    data = {"name": INFOPIGULA_EMAIL, "pass": INFOPIGULA_PASS}

    response = requests.post(url, headers=headers, params=payload, json=data).json()

    access_token = response["access_token"]
    csrf_token = response["csrf_token"]
    return access_token, csrf_token


def get_news(group_target, access_token, csrf_token):

    url = f"https://api.infopigula.pl/api/v1/news-app"
    headers = {
        **default_headers,
        "Host": "api.infopigula.pl",
        "X-CSRF-Token": csrf_token,
        "Authorization": f"Bearer {access_token}",
    }
    payload = {
        "_format": "json",
        "group_target_id": group_target,
        "page": "0",
        "show_last_release": "1",
    }

    response = requests.get(url, headers=headers, params=payload)
    if not response.ok:
        return []

    data = response.json()["rows"]
    return (news["field_news_content"] for news in data)


def split_msg(msg):
    string = ""
    res = []
    if len(msg) > DISC_MESSAGE_LIMIT:
        strings = msg.split("\n")
        for s in strings:
            if len(string) + len(s) < DISC_MESSAGE_LIMIT:
                string += "\n" + s
            else:
                res.append(string)
                string = "\n" + s
        res.append(string)
    else:
        res.append(msg)

    return res


async def send_section_msgs(channel, section, msgs):
    await channel.send(f"***{section.upper()}***")
    for msg in msgs:
        time.sleep(1)
        if msg:
            messages = split_msg(msg)
            for m in messages:
                m = markdownify(m, heading_style="ATX")
                try:
                    await channel.send(m)
                except Exception as e:
                    print(e, m)


client = discord.Client()


@client.event
async def on_ready():
    print("IM READY TO SERVE")


async def my_background_task():
    await client.wait_until_ready()
    while not client.is_closed():
        for guild in client.guilds:
            if guild.name == DISCORD_GUILD:
                break

        for channel in guild.channels:
            if channel.id == int(DISCORD_CHANNEL):
                break

        if Path("save.p").exists():
            with open("save.p", "rb") as f:
                last_msgs = pickle.load(f)
        else:
            last_msgs = dict()

        access_token, csrf_token = get_authorization()

        for target in GroupTarget:
            content = get_news(target.value, access_token, csrf_token)
            content = list(content)
            if not content:
                continue
            first_msg = content[0]
            if target.name not in last_msgs or last_msgs[target.name] != first_msg:
                last_msgs[target.name] = first_msg
                await send_section_msgs(channel, target.name, content)
            else:
                print(f"No update in {target.name}")

        with open("save.p", "wb") as f:
            pickle.dump(last_msgs, f)

        await asyncio.sleep(600)


if __name__ == "__main__":
    client.loop.create_task(my_background_task())
    client.run(DISCORD_TOKEN)
