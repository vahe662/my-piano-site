import os
from collections import deque
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup

START_URL = "http://127.0.0.1:8000/"
OUT = "downloaded"
MEDIA = {".mp3",".wav",".m4a",".aac",".ogg",".opus",".flac",".pdf"}

def ext(url):
    return os.path.splitext(urlparse(url).path.lower())[1]

def same_site(a, b):
    return urlparse(a).netloc == urlparse(b).netloc

def save(url, data):
    path = urlparse(url).path.lstrip("/")
    if not path: return
    target = os.path.join(OUT, path.replace("/", os.sep))
    os.makedirs(os.path.dirname(target), exist_ok=True)
    open(target, "wb").write(data)
    print("SAVED:", url, "->", target)

session = requests.Session()
queue = deque([START_URL])
visited = set()

while queue:
    url = queue.popleft()
    if url in visited: continue
    visited.add(url)
    print("PAGE:", url)
    try:
        r = session.get(url, timeout=10); r.raise_for_status()
    except requests.RequestException as e:
        print("ERROR:", e); continue
    if ext(url) in MEDIA:
        save(url, r.content); continue
    if "text/html" not in r.headers.get("Content-Type",""): continue
    soup = BeautifulSoup(r.text, "html.parser")
    for tag in soup.find_all("a", href=True):
        u = urljoin(url, tag["href"]).split("#")[0]
        if not same_site(u, START_URL): continue
        if ext(u) in MEDIA:
            try:
                x=session.get(u,timeout=10); x.raise_for_status(); save(u,x.content)
            except requests.RequestException as e: print("ERROR:", e)
        elif u not in visited: queue.append(u)
    for tag in soup.find_all("audio", src=True):
        u=urljoin(url,tag["src"])
        if same_site(u,START_URL):
            x=session.get(u,timeout=10); x.raise_for_status(); save(u,x.content)
    for tag in soup.find_all("source", src=True):
        u=urljoin(url,tag["src"])
        if same_site(u,START_URL) and ext(u) in MEDIA:
            x=session.get(u,timeout=10); x.raise_for_status(); save(u,x.content)

print("DONE. Pages visited:", len(visited))
