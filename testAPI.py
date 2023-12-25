import requests
import json
from ast import literal_eval

data = {"documentTitle": "Ijazah",
        "studentName": "Nuril Kaunaini R",
        "studentID": "1301181017",
        "authorID": "ADW00"}

urlGenerate = "https://qrcode-ijazah.vercel.app/generateQR"
resp = requests.post(urlGenerate,json=data)
print(resp.content.decode())

QRimg = literal_eval(resp.content.decode())["encodedQRimg"]
data = {"encodedQRimg": QRimg}

urlVerify = "https://qrcode-ijazah.vercel.app/verifyQR"
resp = requests.post(urlVerify,json=data)
stat = resp.content.decode()
print(stat)