import requests
import json
from ast import literal_eval
import base64
from PIL import Image, ImageOps
from io import BytesIO
import os

import time
from pyzbar import pyzbar
import quirc
from qreader import QReader
import cv2
import numpy as np

def __decodeImage(bytesImg):
	"""
	decode base64 img into Image file
	"""
	bytesDecoded = base64.b64decode(bytesImg + b"==")
	# img = Image.open(BytesIO(bytesDecoded))
	im_arr = np.frombuffer(bytesDecoded, dtype=np.uint8)  # im_arr is one-dim Numpy array
	img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
	return img

list_files = os.listdir("./DB-QR")
list_files = sorted(list_files)
qreader = QReader()
# list_files = ["qrtest_from_app_01.jpeg"]
print("========================== QRCode-Ijazah test read from file ==========================")
print('{:40} \t| {} | {:27} | {}'.format("FILENAME", "DETECTED", "VERIFICATION STATUS", "RESPONSE TIME"))
for filename in list_files:
	if filename == "base64.txt":
		continue
	filename = "./DB-QR/" + filename
	with open(filename, "rb") as image_file:
		encoded_qr = base64.b64encode(image_file.read())

	#DETECT BY QREADER
	# image = cv2.imread(filename)
	# qreader_res = qreader.detect_and_decode(image=image)
	# qreader_res = str(qreader_res[0] != None)
	
	# DETECT BY QRCode-Ijazah
	data = {"encodedQRimg": encoded_qr.decode()}
	urlVerify = "http://127.0.0.1:8000/verifyQR"
	prev_time = time.time()	
	resp = requests.post(urlVerify,json=data)
	response_time = time.time() - prev_time
	code = resp.status_code
	stat = resp.content.decode()
	ijazah_res = str(code == 200)

	print('{:40} \t| {:8} | {:27} | {}'.format(filename, ijazah_res, stat, response_time))

print("=========================================================================================")
print()
## TEST FROM BASE 64
print("========================== QRCode-Ijazah test read from base64 ==========================")
qreader = QReader()
# list_files = ["qrtest_from_app.jpeg"]
print('{:40} \t| {} | {:27} | {}'.format("FILENAME", "DETECTED", "VERIFICATION STATUS", "RESPONSE TIME"))
list_files = []
exec(open("./dataset_from_app/base64.txt", "rb").read())
filename = "qrtest_from_app_"
for idx, img_file in enumerate(list_files):

	img_file = img_file + "=="
	
	# DETECT BY QRCode-Ijazah
	data = {"encodedQRimg": img_file}
	prev_time  = time.time()
	urlVerify = "http://127.0.0.1:8000/verifyQR"
	response_time = str(time.time() - prev_time)
	resp = requests.post(urlVerify,json=data)
	code = resp.status_code
	ijazah_res = str(code == 200)
	stat = resp.content.decode()

	print('{:40} \t| {:8} | {:27} | {}'.format(filename + str(idx + 1), ijazah_res, stat, response_time))
print("===============================================================")
