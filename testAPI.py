import requests
import json
from ast import literal_eval

data = {"documentTitle": "Ijazah",
        "studentName": "Nuril Kaunaini R",
        "studentID": "1301181017",
        "authorID": "ADW00"}

urlGenerate = "http://127.0.0.1:8000/generateQR"
resp = requests.post(urlGenerate,json=data)
print(resp.content.decode())

QRimg = literal_eval(resp.content.decode())["encodedQRimg"]
data = {"encodedQRimg": QRimg}

urlVerify = "http://127.0.0.1:8000/verifyQR"
resp = requests.post(urlVerify,json=data)
stat = resp.content.decode()
print(stat)