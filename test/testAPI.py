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

# data = {"documentTitle": "Ijazah",
#         "studentName": "Nuril Kaunaini R",
#         "studentID": "1301181017",
#         "authorID": "ADW00"}

# urlGenerate = "http://127.0.0.1:8000/generateQR"
# resp = requests.post(urlGenerate,json=data)
# print(resp.content.decode())

# QRimg_encoded = literal_eval(resp.content.decode())["encodedQRimg"]
# QRimg = __decodeImage(QRimg_encoded)
# QRimg.save("qrtest01.png")

# data = {"encodedQRimg": QRimg_encoded}

# urlVerify = "http://127.0.0.1:8000/verifyQR"
# resp = requests.post(urlVerify,json=data)
# stat = resp.content.decode()
# print(stat)

list_files = os.listdir("./data")
list_files = sorted(list_files)

# list_files = ["qrtest_01_distance_02.jpeg"]
print('{:40} \t| {} | {}'.format("FILENAME", "BY ZBAR", "BY QRcode-Ijazah"))
for filename in list_files:
	filename = "./data/" + filename
	with open(filename, "rb") as image_file:
		encoded_qr = base64.b64encode(image_file.read())
		
	image_file = Image.open(filename)
	zbar_res = str(len(pyzbar.decode(image_file)) > 0)


	data = {"encodedQRimg": encoded_qr.decode()}
	urlVerify = "http://127.0.0.1:8000/verifyQR"
	resp = requests.post(urlVerify,json=data)
	code = resp.status_code
	stat = code == 200
	print('{:40} \t| {:7} | {}'.format(filename, zbar_res, stat))