# nyon-stream
<b>A python script that uses webtorrent to stream nyaa videos directly to mpv.</b>

# usage
<b>python3 nyaascraper.py \<keywords - optional\></b>


# config
#### edit the script on lines 14-21 to change your config
### values:

<details>
<summary><b>getDefaultRows</b></summary>
    <i><b>type</i></b>: boolean (bool)<br/>
    <i><b>default value</i></b>: False<br/>
    <i><b>description</i></b>: Get default (white) rows on nyaa<br/>
</details>

<details>
<summary><b>getDangerRows</b></summary>
    <i><b>type</i></b>: boolean (bool)<br/>
    <i><b>default value</i></b>: False<br/>
    <i><b>description</i></b>: Get danger (red) rows on nyaa<br/>
</details>

<details>
<summary><b>TUImode</b></summary>
    <i><b>type</i></b>: boolean (bool)<br/>
    <i><b>default value</i></b>: False<br/>
    <i><b>description</i></b>: Use a tui instead of dmenu, made for windows users and linux users without dmenu<br/>
</details>

<details>
<summary><b>loggingLevel</b></summary>
    <i><b>type</i></b>: integer (int)<br/>
    <i><b>default value</i></b>: logging.ERROR<br/>
    <i><b>description</i></b>: Change the logging level, use logging.INFO or logging.DEBUG to get debug info<br/>
</details>

<details>
<summary><b>maxPageNum</b></summary>
    <i><b>type</i></b>: integer (int)<br/>
    <i><b>default value</i></b>: 5<br/>
    <i><b>description</i></b>: Max page to get on nyaa, if your page number is too high you may encounter some delay<br/>
</details>

<details>
<summary><b>baseUrl</b></summary>
    <i><b>type</i></b>: string (str)<br/>
    <i><b>default value</i></b>: "https://nyaa.si/?s=seeders&o=desc"<br/>
    <i><b>description</i></b>: Change the base url for nyaa, by default searches for most seeders<br/>
</details>

<details>
<summary><b>webtorrentArgs</b></summary>
    <i><b>type</i></b>: string (str)<br/>
    <i><b>default value</i></b>: "--mpv"<br/>
    <i><b>description</i></b>: Arguments to pass to webtorrent, by default startes mpv<br/>
</details>
 
<details>
<summary><b>dmenuArgs</b></summary>
    <i><b>type</i></b>: dictionary (dict)<br/>
    <i><b>default value</i></b>: {"font": "Ubuntu-15"}<br/>
    <i><b>description</i></b>: Additional arguments to pass to the dmenu python wrapper<br/>
</details>


# dependencies
### python dependencies <b>
BeautifulSoup<br/>
requests<br/>
dmenu<br/>
</b>

### external dependencies <b>
dmenu ([arch](https://archlinux.org/packages/community/x86_64/dmenu/))<br/>
webtorrent ([arch aur](https://aur.archlinux.org/packages/webtorrent-cli))<br/>
</b>


# Demo
https://user-images.githubusercontent.com/33488576/148145434-03d97e83-1ff2-4370-a5a1-70e75d04d6fd.mp4


# important info
#### For now the script only works on Linux with dmenu and webtorrent (webtorrent-cli) installed.