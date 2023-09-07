import os
from flask import Flask , jsonify
from flask import request
from flask_cors import CORS

import mimetypes
from PIL import Image
import imagehash
import json
import base64

import requests
import io
from concurrent.futures import ProcessPoolExecutor

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 2097152

CORS(
    app,
    origins=["http://157.7.87.178/"],
    supports_credentials=True
)

@app.route("/search", methods=["POST"])
def search():
  input_text = request.form.get("input_text")
  if len(input_text) >= 100: 
    return jsonify({"error_message": "100文字まで入力できます。"}), 422
  
  with open("lures.json", "r", encoding="utf-8") as f:
    lures = json.load(f)

  with ProcessPoolExecutor(max_workers=2) as executor:
    result_lure = []
    for name, src in lures.items():
      if input_text in name:
        src = "./IMAGE/" + src
        result_lure.append({'name': name, 'src': src})       
  
  for lure in result_lure[0:3]:
      with open(lure["src"], "rb") as image_file:
        data = base64.b64encode(image_file.read()).decode('utf-8')
        lure["src"] = data

  return jsonify(result_lure[0:3])

@app.route("/upload", methods=["POST"])

def upload():
  upload_file = request.files['upload_file']

  # if ("image/" not in upload_file.content_type) or (upload_file.content_type != 'application/octet-stream'):
    # if 'image/' not in mimetypes.guess_type(upload_file.filename)[0]:
  if "image/" not in upload_file.content_type:
    return jsonify({"error_message": "png,jpg,gifのみアップロードできます。"}), 422

  upload_image_hash = imagehash.average_hash(Image.open(upload_file)) 
        
  with open("image_hash.json", "r", encoding="utf-8") as f:
    lures = json.load(f)
    
  min = None
  first_lure = None
  second_lure = None
  third_lure = None
  with ProcessPoolExecutor(max_workers=2) as executor:
    for lure in lures:
      future = executor.submit(comparison, upload_image_hash, lure['hash'])
      diff = future.result()

      name = lure['name']
      src = "./IMAGE/" + lure['src']

      if min is None:
        min = diff
        first_lure = {'name': name, 'src': src}
      if min > diff:
        min = diff
        third_lure = second_lure
        second_lure = first_lure
        first_lure = {'name': name, 'src': src}
      if min == 0:
        break
    
    executor.shutdown()
    
    result_lure = [first_lure, second_lure, third_lure]

    for lure in result_lure:
      with open(lure["src"], "rb") as image_file:
        data = base64.b64encode(image_file.read()).decode('utf-8')
        lure["src"] = data

  return jsonify(result_lure)  


def comparison(upload_image_hash, img_hash):
  diff = upload_image_hash -  imagehash.hex_to_hash(img_hash)
  return diff

if __name__ == "__main__":
  app.run(threaded=True)