from parser_spotify import get_playlist
import requests
import time
import shutil
from selenium import webdriver
import os
from selenium.webdriver.common.keys import Keys
from pathlib import Path
from bs4 import BeautifulSoup

def download_music(playlist_id, user_id):
    user_id = str(user_id)
    folder = Path('songs')
    new_folder_path = folder / user_id
    playlist = get_playlist(playlist_id)
    browser = webdriver.Firefox()
    dont_downloaded_songs = []
    if not new_folder_path.exists():
        # Создаем папку
        new_folder_path.mkdir()

    for song in playlist:
        browser.get(f'https://hitster.fm/search/{song}')

        time.sleep(5)
        button = browser.find_element('xpath','//*[@id="main_page_songs"]/div/div[2]/ul/li[1]/em/i').click()
        button = browser.find_element('xpath','//*[@id="download"]').click()



    for song in playlist:
        if os.path.exists(f"C:/Users/atikc/Downloads/{song}.mp3"):
            shutil.move(f"C:/Users/atikc/Downloads/{song}.mp3", f'C:/Users/atikc/PycharmProjects/TgSpotify/songs/{user_id}' )

'''def download_music(playlist_url, user_id):
    firefox_profile = webdriver.FirefoxProfile()
    firefox_options = webdriver.FirefoxOptions()
    folder = Path('songs')
    new_path = folder / str(user_id)
    playlist = get_playlist_tracks(playlist_url)
    if not new_path.exists():
        new_path.mkdir()
    firefox_profile.set_preference("browser.download.folderList", 1)

    firefox_profile.set_preference("browser.download.dir", f'C:/Users/atikc/PycharmProjects/TgSpotify/songs/{user_id}')
    firefox_profile.set_preference("browser.download.manager.showWhenStarting", False)
    firefox_profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")
    firefox_options.profile = firefox_profile
    browser = webdriver.Firefox(options=firefox_options)

    for song in playlist:
        browser.get(f'https://hitster.fm/search/{song}')

        time.sleep(5)
        button = browser.find_element('xpath', '//*[@id="main_page_songs"]/div/div[2]/ul/li[1]/em/i').click()
        button = browser.find_element('xpath', '//*[@id="download"]').click()'''

def delete_path(user_id):
    shutil.rmtree(f'C:/Users/atikc/PycharmProjects/TgSpotify/songs/{user_id}')
a = webdriver.Firefox()






