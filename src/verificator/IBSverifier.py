from IBS import IdentityBasedSignature, Point
import keyManagement


def verifySignature(ibs: IdentityBasedSignature, publicMsg, hiddenMsg):
  """
  #TO_DO_LIST: Description
  verify
  """
  cleanPublicMsg = __cleanPublicMessage(publicMsg)
  ID, s1_compressed, S2, date, copyNum = __splitHiddenData(hiddenMsg)
  Z_ID = __getAuthPublicKey(ID)
  print("-- public message --")
  print(cleanPublicMsg)
  print("--------------------")
  signatureStat = ibs.verify(s1_compressed, S2, cleanPublicMsg, ID, Z_ID)
  return signatureStat


def __splitHiddenData(hiddenQRData):
  """
  Split variable from extracted QR data
  """
  ID =  hiddenQRData[:5]
  Sign = hiddenQRData[5:-10]
  signComp = Sign.split('|')
  
  s1_compressed = signComp[0]
  s1_compressed = str(int(s1_compressed, 16))
  S2 = signComp[1]
  S2 = int(S2, 16)

  date = hiddenQRData[-10:-4]
  copyNum = hiddenQRData[-4:]

  return ID, s1_compressed, S2, date, copyNum

def __cleanPublicMessage(public_message_raw):
    """
    Remove "Nama :" and "No. Cert" from public message.
    """
    import re
    public_message = re.sub(r'\b' + "Nama : " + r'\b' ,'', public_message_raw)
    public_message = re.sub(r'\b' + "No.Cert : " + r'\b' ,'', public_message)
    # public_message = public_message[1:-1]
    return public_message

def __getAuthPublicKey(ID):
  """
  Z_ID
  #TO_DO_LIST
  """
  authPubKey = keyManagement.Z_ID
  return authPubKey