import os
import pdb
from selenium import webdriver
import discord
import time
import asyncio
import pickle


class LoginPage:

    url = "https://infopigula.pl/#/user/login"

    def __init__(self, driver):
        self.driver = driver
        self.driver.get(self.url)
        self.infopigula_email = os.getenv("INFOPIGULA_EMAIL")
        self.infopigula_pass = os.getenv("INFOPIGULA_PASS")

    @property
    def email(self):
        return self.driver.find_element_by_css_selector('input[name="email"]')

    @property
    def password(self):
        return self.driver.find_element_by_css_selector('input[name="pass"]')

    @property
    def submit(self):
        return self.driver.find_element_by_css_selector('input[type="submit"]')

    def login_to_page(self):
        self.email.send_keys(self.infopigula_email)
        self.password.send_keys(self.infopigula_pass)
        self.submit.click()
        time.sleep(5)


class MainPage:

    url = "https://infopigula.pl/#/"

    def __init__(self, driver):
        self.driver = driver
        self.driver.get(self.url)

    @property
    def sections(self):
        return {
            "poland": self.driver.find_element_by_id("poland"),
            "global": self.driver.find_element_by_id("global"),
            # 'content': self.driver.find_element_by_id("myContent"),
            # 'live': self.driver.find_element_by_id("live"),
            "war": self.driver.find_element_by_id("Napaść Rosji"),
        }

    def get_content_from_section(self, section):
        time.sleep(3)
        self.sections[section].click()
        time.sleep(3)
        return [
            article.text
            for article in self.driver.find_elements_by_class_name("article__content")
        ]


# with webdriver.Firefox() as driver:
#     LoginPage(driver).login_to_page()
#     MainPage(driver).get_content_from_section('poland')


import os

import discord
from collections import defaultdict

from pathlib import Path


# from dotenv import load_dotenv
# $ pip install -U python-dotenv
# load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")
CHANNEL = os.getenv("DISCORD_CHANNEL")
client = discord.Client()

DISC_MESSAGE_LIMIT = 2000


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
                try:
                    await channel.send(m)
                except Exception as e:
                    print(e, m)


@client.event
async def on_ready():
    print("IM READY TO SERVE")


async def my_background_task():
    await client.wait_until_ready()
    while not client.is_closed():
        for guild in client.guilds:
            if guild.name == GUILD:
                break

        for channel in guild.channels:
            if channel.id == int(CHANNEL):
                break

        with webdriver.Firefox() as driver:
            LoginPage(driver).login_to_page()
            page = MainPage(driver)

            sections = page.sections.keys()

            if Path("save.p").exists():
                with open("save.p", "rb") as f:
                    last_msgs = pickle.load(f)
            else:
                last_msgs = dict()

            for section in sections:
                content = page.get_content_from_section(section)
                first_msg = content[0]
                if section not in last_msgs or last_msgs[section] != first_msg:
                    last_msgs[section] = first_msg
                    await send_section_msgs(channel, section, content)
                else:
                    print(f"No update in {section}")

            with open("save.p", "wb") as f:
                pickle.dump(last_msgs, f)

        await asyncio.sleep(600)


client.loop.create_task(my_background_task())
client.run(TOKEN)
