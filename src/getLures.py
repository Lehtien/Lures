import os
import time

import requests
from bs4 import BeautifulSoup
import lxml
import json

from PIL import Image
import io
from concurrent.futures import ProcessPoolExecutor

items = {}

lureIconUrl = 'https://lurebank.com/item_list.php?type='
types = [
  'poper', 'pencil', 'crank', 'vibration', 
  'spin_tail_jig', 'metal_jig', 'inchiku', 'tairaba',
  'egi', 'rubber_jig', 'wirebait', 'shad',
  'minnow', 'jerkbait', 'jig_minnow', 'wake_bait',
  'prop_bait', 'swimbait', 'noisy', 'other_fish',
  'spoon', 'spiner', 'etc'
  ]
 
def getImage(type):
  item = {}

  lureIcon = lureIconUrl + type
  res = requests.get(lureIcon)
  soup = BeautifulSoup(res.text, 'lxml')

  elems = soup.find_all('div', class_='link_item_shousai')
  for elem in elems:
    name = elem.h4.text.translate(str.maketrans({'\t': None, '\n': None}))
    src = elem.img.get("data-original")

    image = Image.open(io.BytesIO(requests.get(src).content))
    image_name = src.replace('https://image.lurebank.com/', '').replace('/', '_', -1)

    if not os.path.isfile("IMAGE/" + image_name):
      image.save("IMAGE/" + image_name)

    item[name] = image_name

    # items[type] = item

  time.sleep(1)
  
  return item


if __name__ == '__main__':
  items = {}
  with ProcessPoolExecutor(max_workers=4) as executor:
      for type in types:
        future = executor.submit(getImage, type)
        items.update(future.result())

      with open("lures.json", "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False)

      executor.shutdown()