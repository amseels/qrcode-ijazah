from .QRGenerator import generateQR
from IBS import IdentityBasedSignature

def generateDocument(ibs: IdentityBasedSignature, documentTitle: str, name: str , studentID: str, authorID: str):
    """
    generate Document
    #TO_DO_LIST
    """
    QRimg = generateQR(ibs, documentTitle, name, studentID, authorID)
    # document = generateDocument() #TO_DO_LIST
    
    return QRimg