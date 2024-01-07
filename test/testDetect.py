import requests
import json
from ast import literal_eval
import base64
from PIL import Image, ImageOps
from io import BytesIO
import os

from pyzbar import pyzbar
import quirc
from qreader import QReader
import cv2

def __decodeImage(bytesImg):
	"""
	decode base64 img into Image file
	"""
	bytesDecoded = base64.b64decode(bytesImg)
	img = Image.open(BytesIO(bytesDecoded))
	return img

list_files = os.listdir("./data")
list_files = sorted(list_files)

qreader = QReader()
# list_files = ["qrtest_01.png"]
print('{:40} \t| {} | {} | {} | {}'.format("FILENAME", "BY QREADER" , "BY ZBAR","BY QUIRC", "BY QRcode-Ijazah"))
for filename in list_files:
	filename = "./data/" + filename
	with open(filename, "rb") as image_file:
		encoded_qr = base64.b64encode(image_file.read())
		
	#DETECT BY ZBAR
	image_file = Image.open(filename)
	zbar_res = str(len(pyzbar.decode(image_file)) > 0)

	#DETECT BY PYQUIRC-ORIGINAL
	img_grayscale = ImageOps.grayscale(image_file)
	quirc_res = str(len(quirc.decode(img_grayscale)) > 0)

	#DETECT BY QREADER
	image = cv2.cvtColor(cv2.imread(filename), cv2.COLOR_BGR2RGB)
	qreader_res = qreader.detect_and_decode(image=image)
	qreader_res = str(qreader_res[0] != None)

	# DETECT BY QRCode-Ijazah
	# data = {"encodedQRimg": encoded_qr.decode()}
	# urlVerify = "http://127.0.0.1:8000/verifyQR"
	# resp = requests.post(urlVerify,json=data)
	# code = resp.status_code
	# ijazah_res = code == 200
	
	print('{:40} \t| {:10} | {:7} | {:8} '.format(filename, qreader_res, zbar_res, quirc_res))