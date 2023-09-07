import os
import time

import requests
from bs4 import BeautifulSoup
import lxml
import json

from PIL import Image
import io

items = {}


base_url = "https://www.backlash.co.jp/"
item_list = "item_list/"
list_number = ["00101", "00105", "00202", "00102" , "00103"]

for number in list_number:
  url = base_url + item_list + number
  
  while True:
    print(url)
    res = requests.get(url)
    soup = BeautifulSoup(res.content, "lxml")
    
    try:
      next_url = soup.select_one("li.next > a").get("href")
      url = base_url + next_url
    except AttributeError:
      print("--------end page--------")
      break
    
    elems = soup.find_all("div", class_="item")
    for elem in elems:
      img = elem.find("p", class_="img")
      src = img.find("img").get("src")  # SRC
      name = elem.find(class_="pn").get_text()  # NAME

      src = src.replace("/images/item/thumb/110x82/", "")
      src_url = base_url + "images/item/original/" + src
      
      try:
        image = Image.open(io.BytesIO(requests.get(src_url).content))
      except Image.UnidentifiedImageError:
        continue

      if not os.path.isfile("IMAGE/" + src):
        image.save("IMAGE/" + src)
        items[name] = src

    time.sleep(1)

with open("lures.json", "a", encoding="utf-8") as f:
    f.seek(f.tell() - 1, os.SEEK_SET)
    f.truncate()
    f.write(' ,')
    json.dump(items, f, ensure_ascii=False)

