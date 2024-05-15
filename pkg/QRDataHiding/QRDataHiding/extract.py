from PIL import Image, ImageOps
from .QRData import QRData
# import quirc
from qreader import QReader

def extractQR(qreader: QReader, img):
    """
    return public_message, hidden_message
    #TO_DO_LIST
    """
    # we need to convert to grayscale for quirc
    # img = ImageOps.grayscale(img)
    
    # the image must support the 2d buffer protocal with data type uint8
    # decoded_codes = quirc.decode(img)

    # Modification for Qreader()
    decoded_codes = qreader.detect_and_decode(image=img)[0]

    if decoded_codes == None :
        error_message = "No QR Detected"
        raise Exception(error_message)

    # _, data = decoded_codes[0]
    data = QRData(decoded_codes[0])
    public_message, hidden_message = __extractHiddenData(data)

    return public_message, hidden_message

def __extractHiddenData(qrcode: QRData):
    """
    return public_message, hidden_message
    #TO_DO_LIST
    """
    arr = list(qrcode.payload_after_ecc)
    len_content = len(qrcode.payload)

    if int(qrcode.version) > 9 :
        padding = arr[len_content+3:]
        data = arr[:len_content+3]
    else:
        padding = arr[len_content+2:]
        data = arr[:len_content+2]

    data_stream = "" 
    for h in range(len(data)):
        data_stream = data_stream + '{0:08b}'.format(data[h])

    if int(qrcode.version) > 9 :
        data = data_stream[20:-4]
    else : 
        data = data_stream[12:-4]

    public_message = __getPublicMessage(data)
    hidden_message = __decodePadding(padding)
   
    return public_message, hidden_message

def __getPublicMessage(data):
    """
    #TO_DO_LIST: description
    """
    public_message_raw = ""
    while len(data) > 0 :
        if int(data[:8],2) < 127 and int(data[:8],2) > 31 :
            public_message_raw = public_message_raw + chr(int(data[:8],2))
        elif int(data[:8],2) == 10 :
            public_message_raw = public_message_raw + "\n"
        data = data[8:]
    return public_message_raw

def __decodePadding(padding):
    """
    #TO_DO_LIST: description
    """
    hidden_message = ""
    for i in range(len(padding)):   
        if int(padding[i]) != 236 and int(padding[i]) != 17:
            hidden_message = hidden_message + chr(int(padding[i]))
    return hidden_message