from PIL import Image
from .extractor import extractFeature
from .IBSverifier import verifySignature
from .documentVerifier import verifyDocumentData
from IBS import IdentityBasedSignature
# we read images using pillow, numpy arrays do also work

def verifyDocument(ibs: IdentityBasedSignature, document):
    publicMsg, hiddenMsg, documentData = extractFeature(document)

    hiddenMsgStat = verifySignature(ibs, publicMsg, hiddenMsg)
    documentStat = verifyDocumentData(publicMsg, documentData)

    return (hiddenMsgStat and documentStat)

