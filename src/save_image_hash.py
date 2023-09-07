import os
from PIL import Image
import imagehash
import json
from concurrent.futures import ProcessPoolExecutor

image_pash  = "IMAGE/"

# image_hashの取得
def get_image_hash(src):
  if os.path.isfile(src):
    return imagehash.average_hash(Image.open(src))
  else:
    return None


# main関数
def main():
  with open("lures.json", "r", encoding="utf-8") as f:
    lures = json.load(f)

  items = []
  with ProcessPoolExecutor(max_workers=4) as executor:
      for name, src in lures.items():
        future = executor.submit(get_image_hash, image_pash + src)
        img_hash = future.result()
        
        if img_hash is not None:
          items.append({"hash": str(img_hash), "name": name, "src": src})

  with open("image_hash.json", "w", encoding="utf-8") as f:
      json.dump(items, f, ensure_ascii=False)


# 実行
if __name__ == "__main__":
  main()