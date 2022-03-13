"""
Move directories with xboxunity ID to directory with game name
"""
import os
import requests
import shutil


def create_and_move_directory(cwd, new_dir, old_dir):
    print("ID:{} Name:{}".format(old_dir, new_dir))
    make_dir = os.path.join(cwd, new_dir)
    new_dir = os.path.join(cwd, new_dir, old_dir)
    old_dir = os.path.join(cwd, old_dir)
    if not os.path.exists(make_dir):
        os.makedirs(make_dir)
    shutil.move(old_dir, new_dir)


def main():
    """
    Xbox Unity Utility
    """
    cwd = os.getcwd()
    directories = [d for d in os.listdir(cwd) if os.path.isdir(d)]
    for d in directories:
        response = requests.get(
            "http://xboxunity.net/Resources/Lib/TitleList.php?page=0&search={}&sort=3&category=0&filter=0".format(
                d
            )
        )
        if response.status_code == 200:
            dictionary = response.json()
            create_and_move_directory(cwd, dictionary.get("Items")[0].get("Name"), d)


if __name__ == "__main__":
    main()
