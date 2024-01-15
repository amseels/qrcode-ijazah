import requests
import json
from ast import literal_eval
import base64
from PIL import Image
from io import BytesIO
import os

from pyzbar import pyzbar
import numpy as np
import cv2

def __decodeImage(bytesImg):
	"""
	decode base64 img into Image file
	"""
	bytesDecoded = base64.b64decode(bytesImg)
	# img = Image.open(BytesIO(bytesDecoded))
	im_arr = np.frombuffer(bytesDecoded, dtype=np.uint8)  # im_arr is one-dim Numpy array
	img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
	return img


data = {"documentTitle": "Ijazah",
        "studentName": "Nuril Kaunaini R",
        "studentID": "1301181017",
        "authorID": "ADW00"}

urlGenerate = "http://127.0.0.1:8000/generateQR"
resp = requests.post(urlGenerate,json=data)
print(resp.content.decode())

QRimg_encoded = literal_eval(resp.content.decode())["encodedQRimg"]
# QRimg = __decodeImage(QRimg_encoded)
# QRimg.save("qrtest01.png")

# filename = "data/qrtest_from_app.jpeg"
# img_file = open(filename, "rb").read()
# QRimg_encoded = base64.b64encode(img_file).decode()
# print(QRimg_encoded)

data = {"encodedQRimg": QRimg_encoded}

urlVerify = "http://127.0.0.1:8000/verifyQR"
resp = requests.post(urlVerify,json=data)
stat = resp.content.decode()
print(stat)