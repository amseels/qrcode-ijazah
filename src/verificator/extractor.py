from PIL import Image, ImageOps
import quirc
import QRDataHiding

def extractFeature(document):
    """
    #TO_DO_LIST

    Process 3.1
    input: signed document with QR
    output: QR Message, Document Data, Signature
    """
    publicMsg, hiddenMsg = QRDataHiding.extractQR(document)
    documentData = __extractDocumentData(document)
    return publicMsg, hiddenMsg, documentData


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