import itertools
import os
import random
import subprocess
import time

import requests
from bs4 import BeautifulSoup

HOME = os.path.expanduser("~")
WALLPAPER = os.path.join(HOME, "wallpaper.jpg")
OLD_WALLPAPER = os.path.join(HOME, "old_wallpaper.jpg")
NEW_WALLPAPER = os.path.join(HOME, "new_wallpaper.jpg")
TODAY_WALLPAPER = os.path.join(HOME, "today_wallpaper.jpg")
UPDATE_TIME_FILE = os.path.join(HOME, ".wallpaper_update_time")


def download_image(url, file_path):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(file_path, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        return True
    except Exception as e:
        print(f"Error downloading image: {e}")
        return False


def set_wallpaper(image_path):
    subprocess.run(
        ["gsettings", "set", "org.gnome.desktop.background", "picture-uri-dark", f"file://{image_path}"]
    )
    subprocess.run(
        ["gsettings", "set", "org.gnome.desktop.background", "picture-uri", f"file://{image_path}"]
    )


def update_wallpaper(url):
    if download_image(url, NEW_WALLPAPER):
        if os.path.exists(WALLPAPER):
            os.rename(WALLPAPER, OLD_WALLPAPER)
        os.rename(NEW_WALLPAPER, WALLPAPER)
        set_wallpaper(WALLPAPER)
        print("Updated wallpaper")
        with open(UPDATE_TIME_FILE, "w") as f:
            f.write(str(int(time.time())))
    else:
        print("Skipping to the next wallpaper")


def prev_wallpaper():
    if os.path.exists(OLD_WALLPAPER):
        os.rename(WALLPAPER, NEW_WALLPAPER)
        os.rename(OLD_WALLPAPER, WALLPAPER)
        os.rename(NEW_WALLPAPER, OLD_WALLPAPER)
        set_wallpaper(WALLPAPER)
        print("Reverted to the previous wallpaper")


def today_wallpaper(url):
    if download_image(url, TODAY_WALLPAPER):
        if os.path.exists(WALLPAPER):
            os.rename(WALLPAPER, OLD_WALLPAPER)
        os.rename(TODAY_WALLPAPER, WALLPAPER)
        set_wallpaper(WALLPAPER)
        print("Updated wallpaper to today's image")


def check_and_update_wallpaper(urls, interval=0):
    last_update = 0
    if os.path.exists(UPDATE_TIME_FILE):
        with open(UPDATE_TIME_FILE, "r") as f:
            last_update = int(f.read().strip())

    current_time = int(time.time())
    if current_time - last_update > interval:
        today_wallpaper(random.choice(urls))


def fetch_wallpaper_urls(webpage_url):
    try:
        response = requests.get(webpage_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        section = soup.find("section", class_="post-content")
        if not section:
            return []
        img_tags = section.find_all("img")
        urls = [img["src"] for img in img_tags if "src" in img.attrs]
        return urls
    except Exception as e:
        print(f"Error fetching wallpaper URLs: {e}")
        return []


sources = [
    "https://willguimont.github.io/photo/2023/07/27/maizerets-2.html",
    "https://willguimont.github.io/photo/2022/10/15/maizerets.html",
    "https://willguimont.github.io/photo/2019/02/14/ducks.html",
    "https://willguimont.github.io/photo/2019/01/28/squirrels.html",
]
wallpaper_urls = itertools.chain.from_iterable(fetch_wallpaper_urls(source) for source in sources)
website_root = "https://willguimont.github.io"
wallpaper_urls = [website_root + url for url in wallpaper_urls]

check_and_update_wallpaper(wallpaper_urls)
