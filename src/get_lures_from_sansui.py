import os
import time

import requests
from bs4 import BeautifulSoup
import lxml
import json

from PIL import Image
import io

items = {}


for i in range(1, 10):
    url = f"https://sansui1902.jp/category/550303/{i}/1.html"

    res = requests.get(url)

    soup = BeautifulSoup(res.text, "lxml")
    elems = soup.find_all("img", class_="img-responsive")

    for elem in elems:
        name = elem.get("alt")
        if name is None:
            continue

        src = elem.get("src")
        image_name = src.replace("/images/goods/", "")
        src_url = "https://sansui1902.jp" + src

        image = Image.open(io.BytesIO(requests.get(src_url).content))

        if not os.path.isfile("IMAGE/" + image_name):
            image.save("IMAGE/" + image_name)
            items[name] = image_name

with open("lures.json", "a", encoding="utf-8") as f:
    json.dump(items, f, ensure_ascii=False)

    time.sleep(1)
