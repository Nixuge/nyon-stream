# nyon-stream
A python script that uses webtorrent to stream nyaa videos directly to mpv.

## usage
`python3 nyaascraper.py [<keywords>]`

## important info
This script was made to be a [notflix](https://github.com/Bugswriter/notflix), nyaa edition. It was also designed to be Linux-only at first.<br/>
You can however run it on other OSes by setting the "TUI_MODE" value to True in [the config](#config), at the cost of the fancy menu shown in the demo (you'll have to use your terminal instead)


**We can't ensure that this script will work properly using Windows.**


## config
Edit the script on lines 14-21 to change your config

**Values**:

| name             | type | default                                       | description                                                                                                                                |
| -----------------|------|-----------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------- |
| GET_DEFAULT_ROWS | bool | `False`                                       | get default (white) rows on nyaa                                                                                                           |
| GET_DANGER_ROWS  | bool | `False`                                       | get danger (red) rows on nyaa                                                                                                              |
| TUI_MODE         | bool | `False`                                       | use a TUI instad of dmenu. Made for Windows users or Linux users without dmenu                                                             |
| LOGGER_LEVEL     | int  | `ERROR` (40)                                  | logging level, according to the `logging` module. Use INFO or DEBUG to get the debug messages                                              |
| MAX_PAGE_NUM     | int  | `5`                                           | max pages to scrape on nyaa, you may encounter some delay if the number is too high                                                        |
| SEARCH_URL       | str  | `https://nyaa.si/?q={query}&s=seeders&o=desc` | the nyaa search url, by default searches by the most seeders with the 'q' argument being the query                                         |
| WEBTORRENT_ARGS  | str  | `--keep-seeding --mpv`                        | arguments to pass to webtorrent, starts mpv and keeps seeding by default                                                                   |
| DMENU_ARGS       | str  | `{ "font": "Ubuntu-15" }`                     | arguments to pass to the dmenu python wrapper                                                                                              |
| PROXIES          | dict | `None`                                        | proxies to use (**for nyaa, not for the torrents!**), example: `{ "http": "socks5://127.0.0.1:9050", "https": "socks5://127.0.0.1:9050" }` |


## dependencies
### python dependencies

- **BeautifulSoup**
- **requests**
- **dmenu** *only if TUImode is disabled*

### external dependencies

- **dmenu** ([arch official repo][dmenu]) *only if TUImode is disabled*
- **webtorrent** ([arch user repo][webtorrent])


## demo
https://user-images.githubusercontent.com/33488576/148145434-03d97e83-1ff2-4370-a5a1-70e75d04d6fd.mp4


<!-- Links -->
[dmenu]: https://archlinux.org/packages/community/x86_64/dmenu/ "dmenu arch repo link"
[webtorrent]: https://aur.archlinux.org/packages/webtorrent-cli "webtorrent arch user repo link"
