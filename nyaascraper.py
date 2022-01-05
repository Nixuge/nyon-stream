#! /bin/python3

from bs4.element import ResultSet
from bs4 import BeautifulSoup
from urllib.parse import unquote

import sys
import os
import requests
import dmenu #linux only


#success = green (always true)
#default = white
#danger = red
def getRows(soup : BeautifulSoup, getDefault = False, getDanger = False) -> ResultSet:
    rows = soup.find_all('tr', class_='success')
    if getDefault:
        rows += soup.find_all('tr', class_='default')
    if getDanger:
        rows += soup.find_all('tr', class_='danger')

    return rows

def getTorrents(url: str) -> dict:
    torrents = []
    for page_number in range(1, 100): 
        page_url = f"{url}&p={str(page_number)}"
        page_html = requests.get(page_url)
        soup = BeautifulSoup(page_html.text, 'html.parser')

        rows = getRows(soup)

        for row in rows:
            td = row.find_all('td', class_='text-center')
            links = td[0].find_all('a')

            size = next((x for x in td if "GiB" in x.text or "$MiB" in x.text), None)
            try:
                size = "[" + size.get_text() + "] "
            except:
                size = ""

            magnet = unquote(links[1]['href'])
            name = row.find_all('a',text=True)[0].get_text()
            torrents.append({"name": size + name, "magnet": magnet})

        if len(rows) == 0:
            break
        
    return torrents

#linux only
def choice(dict: dict) -> str:
    choice = dmenu.show((x["name"] for x in dict), lines=25)
    return next((x for x in dict if x["name"] == choice), None)["magnet"]


if __name__ == '__main__':
    query = " ".join(sys.argv[1:]).replace(" ", "+")
    base_url = 'https://nyaa.si/?s=seeders&o=desc'

    torrents = getTorrents(f"{base_url}&q={query}")
    magnet = choice(torrents)

    #linux only
    os.system(f"webtorrent \"{magnet}\" --mpv")
