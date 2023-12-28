from PIL import Image
from .extractor import extractFeature
from .IBSverifier import verifySignature
from .documentVerifier import verifyDocumentData
from IBS import IdentityBasedSignature
# we read images using pillow, numpy arrays do also work

def verifyDocument(ibs: IdentityBasedSignature, document):
    try:
        publicMsg, hiddenMsg, documentData = extractFeature(document)
    except Exception as err:
        raise err
    
    hiddenMsgStat = verifySignature(ibs, publicMsg, hiddenMsg)
    documentStat = verifyDocumentData(publicMsg, documentData)

    return (hiddenMsgStat and documentStat)

