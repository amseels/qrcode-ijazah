from .IBSsigner import signDocument
import datetime
from IBS import IdentityBasedSignature
import QRDataHiding

def generateMsg(ibs: IdentityBasedSignature, publicMsg:str, authorID: str):
    # publicMsg = __generatePublicMsg(documentTitle, name, studentID)
    hiddenMsg = __generateHiddenMsg(ibs, publicMsg, authorID)
    return publicMsg, hiddenMsg

def generateQR(ibs: IdentityBasedSignature, publicMsg, authorID: str):
    publicMsg, hiddenMsg = generateMsg(ibs, publicMsg, authorID)
    QRimg = QRDataHiding.generateQR(publicMsg, hiddenMsg)
    return QRimg

# Convert Data to Qr hidden data
def __generateHiddenMsg(ibs: IdentityBasedSignature, publicMsg: str, authorID: str):
    """
    #TO_DO_LIST: copyNum
    """
    S1_compressed, S2 = signDocument(ibs, publicMsg, authorID)
    s1Hex = '{:x}'.format(int(S1_compressed))
    s2Hex = '{:x}'.format(int(S2))
    date = str(datetime.datetime.today().strftime('%d%m%y'))
    copyNum = '0000' #TO_DO_LIST
    
    hiddenMsg = str(authorID) + s1Hex + '|' + s2Hex + str(date) + str(copyNum)
    return hiddenMsg

def __generatePublicMsg(documentTitle: str, name:str, studentID: str):
    """
    #TO_DO_LIST: create more general document data
    """
    publicMsg = "{}\nNama : {}\nNo.Cert : {}".format(documentTitle, name, studentID)
    return publicMsg
