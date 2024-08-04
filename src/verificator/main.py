from PIL import Image
from .extractor import extractFeature
from .IBSverifier import verifySignature
from .documentVerifier import verifyDocumentData
from IBS import IdentityBasedSignature
from qreader import QReader

# Additonal Libary to get execution time -LALA
import time
# we read images using pillow, numpy arrays do also work

def verifyDocument(ibs: IdentityBasedSignature, qreader: QReader, document):
    try:
        publicMsg, hiddenMsg, documentData = extractFeature(qreader, document)
        print("== PUBLIC MESSAGE ==")
        print(publicMsg)
        print("=====================")
        if hiddenMsg == "":
            return "Error"
        
        # start Timer
        start_time = time.time()
        # run Verify Function     
        hiddenMsgStat = verifySignature(ibs, publicMsg, hiddenMsg)
        documentStat = verifyDocumentData(publicMsg, documentData)
        # Calculate the elapsed time of Verify Function
        verifyTime =  str(time.time() - start_time)

        return (hiddenMsgStat and documentStat), verifyTime
    except Exception as err:
        raise err