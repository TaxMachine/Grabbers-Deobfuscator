import requests, os


def DownloadFile(url):
    if not os.path.exists("temp"): os.makedirs("temp")
    local_filename = os.path.join("temp", url.split('/')[-1])
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    return local_filename