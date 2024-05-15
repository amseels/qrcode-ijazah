from PIL import Image, ImageOps
import QRDataHiding
from qreader import QReader

def extractFeature(Qreader: QReader, document):
    """
    #TO_DO_LIST

    Process 3.1
    input: signed document with QR
    output: QR Message, Document Data, Signature
    """
    try:
        publicMsg, hiddenMsg = QRDataHiding.extractQR(Qreader, document)
        documentData = __extractDocumentData(document)
        return publicMsg, hiddenMsg, documentData
    except Exception as err:
        raise err


def __extractDocumentData(document):
    """
    #TO_DO_LIST

    Process 3.1.2
    extract document data
    - scan document text by OCR
    - remove template text
    - get document data
    """
    return None
