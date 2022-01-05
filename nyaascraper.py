#! /bin/python3

from bs4.element import ResultSet
from bs4 import BeautifulSoup
from urllib.parse import unquote

import sys
import os
import requests
import logging
import dmenu #linux only


getDefaultRows: bool = False #get default (white) rows on nyaa
getDangerRows: bool = False #get danger (red) rows on nyaa
TUImode: bool = False #use a tui instead of dmenu
loggingLevel: int = logging.INFO #print debug
baseUrl: str = 'https://nyaa.si/?s=seeders&o=desc' #base url (by default searches by most seeders)
webtorrentArgs: str = "--mpv" #args (by default starts mpv)
maxPageNum: int = 5 #max page to get on nyaa (by default 5), if your number is too big you may encounter some delay
dmenuArgs = {"font": "Ubuntu-15"} #additional args for dmenu


logging.basicConfig()
logging.getLogger().setLevel(loggingLevel)

def getRows(soup : BeautifulSoup, getDefault = getDefaultRows, getDanger = getDangerRows) -> ResultSet:
    rows = soup.find_all('tr', class_='success')
    if getDefault:
        rows += soup.find_all('tr', class_='default')
    if getDanger:
        rows += soup.find_all('tr', class_='danger')

    return rows

def getTorrents(url: str) -> dict:
    torrents = []
    for pageNum in range(1, maxPageNum): 
        pageUrl = f"{url}&p={str(pageNum)}"
        logging.info(f"Getting page {str(pageNum)} with url {pageUrl}")
        pageHtml = requests.get(pageUrl)
        soup = BeautifulSoup(pageHtml.text, 'html.parser')
        logging.info(f"Got page {str(pageNum)} !")

        rows = getRows(soup)
        logging.info(f"Got {str(len(rows))} rows from page {str(pageNum)}")

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
def choiceD(dict: dict, getSubElem = False, subElem = "") -> str: #lazy
    if getSubElem:
        choice = dmenu.show((x.get(subElem) for x in dict), lines=25, **dmenuArgs)
        return next((x for x in dict if x.get(subElem) == choice), None)
    choice = dmenu.show((x for x in dict), lines=25, **dmenuArgs)
    return next((x for x in dict if x == choice), None)
#linux only
def askD(prompt: str) -> str:
    return dmenu.show([], prompt=prompt, **dmenuArgs)

if __name__ == '__main__':
    query = " ".join(sys.argv[1:]).replace(" ", "+")
    if len(query) == 0:
        query = askD("Search tags")

    torrents = getTorrents(f"{baseUrl}&q={query}")
    logging.info(f"Got {str(len(torrents))} total entries")
    if len(torrents) == 0:
        sys.exit(1)
    magnet = choiceD(torrents, getSubElem=True, subElem="name")["magnet"]

    #linux only
    logging.info("Loading webtorrent")
    os.system(f"webtorrent \"{magnet}\" {webtorrentArgs}")