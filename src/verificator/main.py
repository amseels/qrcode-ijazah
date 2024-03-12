from PIL import Image
from .extractor import extractFeature
from .IBSverifier import verifySignature
from .documentVerifier import verifyDocumentData
from IBS import IdentityBasedSignature
from qreader import QReader
# we read images using pillow, numpy arrays do also work

def verifyDocument(ibs: IdentityBasedSignature, qreader: QReader, document):
    try:
        publicMsg, hiddenMsg, documentData = extractFeature(qreader, document)
        print("== PUBLIC MESSAGE ==")
        print(publicMsg)
        print("=====================")
        if hiddenMsg == "":
            return False
        hiddenMsgStat = verifySignature(ibs, publicMsg, hiddenMsg)
        documentStat = verifyDocumentData(publicMsg, documentData)

        return (hiddenMsgStat and documentStat)
    except Exception as err:
        raise err