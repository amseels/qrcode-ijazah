from .QRGenerator import generateQR
from IBS import IdentityBasedSignature

def generateDocument(ibs: IdentityBasedSignature, publicMsg: str, authorID: str):
    """
    generate Document
    #TO_DO_LIST
    """
    QRimg = generateQR(ibs, publicMsg, authorID)
    # document = generateDocument() #TO_DO_LIST
    
    return QRimg