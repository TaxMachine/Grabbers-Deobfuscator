import os
import requests
from bs4 import BeautifulSoup

from typing import Dict, Callable


def TryDownload(url):
    URL_TABLES: Dict[str, Callable[[str], str]] = {
        "https://www.mediafire.com/file/": MediafireDownload,
        "https://tinyurl.com/": GetTinyUrl
    }
    for func in URL_TABLES:
        if url.startswith(func):
            return URL_TABLES[func](url)
    return DownloadFile(url)


def DownloadFile(url: str) -> str:
    if not os.path.exists("temp"):
        os.makedirs("temp")
    local_filename = os.path.join("temp", url.split('/')[-1]) if not "mediafire" \
        in url else \
        os.path.join("temp", url.split('/')[-1])
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    return local_filename


def MediafireDownload(url: str) -> str:
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    download = soup.find("a", {"aria-label": "Download file"})
    return DownloadFile(download.attrs["href"])


def GetTinyUrl(url: str) -> str:
    r = requests.get(url)
    b = BeautifulSoup(r.text, "lxml")
    return b.find("a").attrs["href"]
