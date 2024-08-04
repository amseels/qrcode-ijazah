from src.verificator import verifyDocument
from src.generator import generateDocument
from IBS import IdentityBasedSignature, Point
import src.keyManagement as keyManagement
from qreader import QReader

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from PIL import Image
import base64
from io import BytesIO
import numpy as np
import cv2
import traceback
# uvicorn API:app --reload

def __decodeImage(bytesImg):
	"""
	decode base64 img into Image file
	"""
	try:
		bytesDecoded = base64.b64decode(bytesImg + b"==")
		# img = Image.open(BytesIO(bytesDecoded))
		im_arr = np.frombuffer(bytesDecoded, dtype=np.uint8)  # im_arr is one-dim Numpy array
		img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
		return img
	except Exception as err:
		raise err


class generateQRinput(BaseModel):
	publicMsg: str
	authorID: str

class generateQRresult(BaseModel):
	 encodedQRimg : bytes

class verifyQRinput(BaseModel):
	encodedQRimg : bytes

class verifyQRresult(BaseModel):
	verificationStat : str
	verifyTime : str

ibs = IdentityBasedSignature(keyManagement.standard, keyManagement.Pub)
qreader = QReader()

app = FastAPI()

@app.post("/generateQR")
async def generateQR(data:generateQRinput):
	QRimg = generateDocument(ibs,
													 data.publicMsg,
													 data.authorID)
	result = generateQRresult(encodedQRimg=QRimg)
	return result

@app.post("/verifyQR")
async def verifyQR(data:verifyQRinput):
	try:
		res, verifyTime = verifyDocument(ibs,
												 qreader,
													__decodeImage(data.encodedQRimg))
		result = verifyQRresult(verificationStat=str(res), verifyTime=verifyTime)
		return result
	except Exception:
		print("ERROR")
		# print(traceback.format_exc())
		result = verifyQRresult(verificationStat="Error", verifyTime="-1")
		return result

