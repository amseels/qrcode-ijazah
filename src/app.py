from src.verificator import verifyDocument
from src.generator import generateDocument
from IBS import IdentityBasedSignature, Point
import keyManagement

from fastapi import FastAPI
from pydantic import BaseModel
from PIL import Image
import base64
from io import BytesIO

# uvicorn API:app --reload

def __decodeImage(bytesImg):
    """
    decode base64 img into Image file
    """
    bytesDecoded = base64.b64decode(bytesImg)
    img = Image.open(BytesIO(bytesDecoded))
    return img

class generateQRinput(BaseModel):
  documentTitle: str
  studentName: str
  studentID: str
  authorID: str

class generateQRresult(BaseModel):
   encodedQRimg : bytes

class verifyQRinput(BaseModel):
  encodedQRimg : bytes

class verifyQRresult(BaseModel):
   verificationStat : bool

ibs = IdentityBasedSignature(keyManagement.standard, keyManagement.Pub)

app = FastAPI()

@app.post("/generateQR")
async def generateQR(data:generateQRinput):
  QRimg = generateDocument(ibs,
                           data.documentTitle,
                           data.studentName,
                           data.studentID,
                           data.authorID)
  result = generateQRresult(encodedQRimg=QRimg)
  return result

@app.post("/verifyQR")
async def verifyQR(data:verifyQRinput):
  res = verifyDocument(ibs,
                        __decodeImage(data.encodedQRimg))
  result = verifyQRresult(verificationStat=res)
  return result

