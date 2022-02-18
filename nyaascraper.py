#!/bin/python3

from typing import Any, Dict, Optional
from bs4.element import ResultSet
from bs4 import BeautifulSoup
from urllib.parse import unquote

import os
import requests
import logging as LOGGER


# if you need additional info for the settings, look at the readme
GET_DEFAULT_ROWS: bool = True
GET_DANGER_ROWS: bool = True
TUI_MODE: bool = False
LOGGER_LEVEL: int = LOGGER.ERROR
SEARCH_URL: str = "https://nyaa.si/?q={query}&s=seeders&o=desc"
WEBTORRENT_ARGS: str = "--keep-seeding --mpv --playlist"
MAX_PAGE_NUM: int = 5
DMENU_ARGS: Dict[Any, Any] = {"font": "Ubuntu-15"}
PROXIES: Optional[Dict] = None


if not TUI_MODE:
    import dmenu

LOGGER.basicConfig()
LOGGER.getLogger().setLevel(LOGGER_LEVEL)


def getRows(
    soup: BeautifulSoup, getDefault=GET_DEFAULT_ROWS, getDanger=GET_DANGER_ROWS
) -> ResultSet:
    rows = soup.find_all("tr", class_="success")
    if getDefault:
        rows += soup.find_all("tr", class_="default")
    if getDanger:
        rows += soup.find_all("tr", class_="danger")
    return rows


def getTorrents(url: str) -> dict:
    torrents = []
    for pageNum in range(1, MAX_PAGE_NUM):
        pageUrl = f"{url}&p={pageNum}"
        LOGGER.info(f"Getting page {pageNum} with url {pageUrl}")

        try:  # from TheRealTechWiz, but in a slightly less dirty way
            pageHtml = requests.get(pageUrl, proxies=PROXIES)
        except:
            continue

        soup = BeautifulSoup(pageHtml.text, "html.parser")
        LOGGER.info(f"Got page {pageNum} !")

        rows = getRows(soup)
        LOGGER.info(f"Got {len(rows)} rows from page {pageNum}")

        for row in rows:
            td = row.find_all("td", class_="text-center")
            links = td[0].find_all("a")

            size = next((x for x in td if "GiB" in x.text or "$MiB" in x.text), None)
            try:
                size = "[" + size.get_text() + "] "
            except:
                size = ""

            magnet = unquote(links[1]["href"])
            name = row.find_all("a", text=True)[0].get_text()
            torrents.append({"name": size + name, "magnet": magnet})

        if len(rows) == 0:
            break

    return torrents


def _choiceD(dict: dict, subElem="") -> str:
    choice = dmenu.show((x.get(subElem) for x in dict), lines=25, **DMENU_ARGS)
    return next((x for x in dict if x.get(subElem) == choice), None)


def _choiceT(dict: dict, subElem="") -> str:
    elems = list((x.get(subElem) for x in dict))
    elemsReverse = list(elems)
    elemsReverse.reverse()
    for i, elem in enumerate(elemsReverse):
        print(f"{str(len(elems) - i)}: {elem}")
    # seems to be working
    index = int(input("Enter your choice: ")) - 1

    return dict[index]


def choice(dict: dict, subElem="") -> str:  # lazy
    return (_choiceT if TUI_MODE else _choiceD)(dict, subElem)


def ask(prompt: str) -> str:
    if TUI_MODE:
        return input(prompt)
    return dmenu.show([], prompt=prompt, **DMENU_ARGS)


def main(*args: str) -> int:
    query = (" ".join(args) if (args) else ask("Search tags:")).replace(" ", "+")

    torrents = getTorrents(SEARCH_URL.format(query=query))
    LOGGER.info(f"Got {len(torrents)} total entries")
    if len(torrents) == 0:
        return 1

    magnet = choice(torrents, subElem="name").get("magnet")
    LOGGER.info(f"Got magnet link: {magnet}")

    LOGGER.info("Loading webtorrent")
    if os.name == "posix":
        os.system(f'webtorrent "{magnet}" {WEBTORRENT_ARGS}')
    else:
        print(
            "TODO: find how to run webtorrent-cli on windows. don't make an issue for this except if it's been 2 months since the last commit"
        )
        # os.system(f"./webtorrent \"{magnet}\" {webtorrentArgs}")

    return 0


if __name__ == "__main__":
    import sys
    import traceback

    exit_code = 1

    try:
        exit_code = main(*sys.argv[1:])
    except KeyboardInterrupt:
        print("\n\nEnding execution due to user interaction.")
    except Exception as err:
        print()
        print("An error occured!")
        print(err)
        traceback.print_tb(err.__traceback__)
    finally:
        print()
        exit(exit_code)
