import requests
import json
from ast import literal_eval
import base64
from PIL import Image
from io import BytesIO
import os

from pyzbar import pyzbar

def __decodeImage(bytesImg):
	"""
	decode base64 img into Image file
	"""
	bytesDecoded = base64.b64decode(bytesImg)
	img = Image.open(BytesIO(bytesDecoded))
	return img

data = {"documentTitle": "Ijazah",
        "studentName": "Nuril Kaunaini R",
        "studentID": "1301181017",
        "authorID": "ADW00"}

urlGenerate = "http://127.0.0.1:8000/generateQR"
resp = requests.post(urlGenerate,json=data)
print(resp.content.decode())

QRimg_encoded = literal_eval(resp.content.decode())["encodedQRimg"]
QRimg = __decodeImage(QRimg_encoded)
QRimg.save("qrtest01.png")

data = {"encodedQRimg": QRimg_encoded}

urlVerify = "http://127.0.0.1:8000/verifyQR"
resp = requests.post(urlVerify,json=data)
stat = resp.content.decode()
print(stat)