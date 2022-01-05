#! /bin/python3

from bs4.element import ResultSet
from bs4 import BeautifulSoup
from urllib.parse import unquote

import sys
import os
import requests
import logging
#if you need additional info for the settings, look at the readme
getDefaultRows: bool = False
getDangerRows: bool = False
TUImode: bool = True
loggingLevel: int = logging.INFO
baseUrl: str = 'https://nyaa.si/?s=seeders&o=desc'
webtorrentArgs: str = "--keep-seeding --mpv"
maxPageNum: int = 5
dmenuArgs = {"font": "Ubuntu-15"}
proxies = None

if not TUImode:
    import dmenu

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
        pageHtml = requests.get(pageUrl, proxies=proxies)
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

def _choiceD(dict: dict, subElem = "") -> str:
    choice = dmenu.show((x.get(subElem) for x in dict), lines=25, **dmenuArgs)
    return next((x for x in dict if x.get(subElem) == choice), None)

def _choiceT(dict: dict, subElem = "") -> str:
    elems = list((x.get(subElem) for x in dict))
    elemsReverse = list(elems)
    elemsReverse.reverse()
    for i, elem in enumerate(elemsReverse):
        print(f"{str(len(elems) - i)}: {elem}")
    #seems to be working
    index = int(input("Enter your choice: ")) -1
    
    return dict[index]

def choice(dict: dict, subElem = "") -> str: #lazy
    if TUImode:
        return _choiceT(dict, subElem)
    return _choiceD(dict, subElem)

def ask(prompt: str) -> str:
    if TUImode:
        return input(prompt)
    return dmenu.show([], prompt=prompt, **dmenuArgs)
    

if __name__ == '__main__':
    query = " ".join(sys.argv[1:]).replace(" ", "+")
    if len(query) == 0:
        query = ask("Search tags: ").replace(" ", "+")

    torrents = getTorrents(f"{baseUrl}&q={query}")
    logging.info(f"Got {str(len(torrents))} total entries")
    if len(torrents) == 0:
        sys.exit(1)
    magnet = choice(torrents, subElem="name").get("magnet")
    logging.info(f"Got magnet link: {magnet}")
    
    logging.info("Loading webtorrent")
    if os.name == "posix":
        os.system(f"webtorrent \"{magnet}\" {webtorrentArgs}")
    else:
        print("TODO: find how to run webtorrent-cli on windows. don't make an issue for this except if it's been 2 months since the last commit")
        #os.system(f"./webtorrent \"{magnet}\" {webtorrentArgs}")