from IBS import IdentityBasedSignature, Point
import keyManagement
# from ..database import keyManagement

# ...
"""
global varsTest
def setVarTest(x)
   this.varsTest = x
   return this.VarTest

def getCartest():
   return this.VarTest 
"""
# ...

def signDocument(ibs: IdentityBasedSignature, publicMsg: str, authorID: str):
  """
  Sign m by ID
  #TO_DO_LIST
  """
  authPrivKey = __getAuthPrivateKey(authorID)
  authPubKey = __getAuthPublicKey(authorID)
  cleanPublicMsg = __cleanPublicMessage(publicMsg)
  print("-- public message --")
  print(cleanPublicMsg)
  print("--------------------")
  S1_compressed, S2 = ibs.sign(authorID, cleanPublicMsg, authPrivKey, authPubKey)
  return S1_compressed, S2

def __getAuthPublicKey(authorID):
  """
  Z_ID
  #TO_DO_LIST 
  """
  authPubKey = keyManagement.Z_ID
  return authPubKey

def __getAuthPrivateKey(authorID):
  """
  d_ID
  #TO_DO_LIST
  """
  authPrivKey = keyManagement.d_ID
  return authPrivKey

def __cleanPublicMessage(public_message_raw):
    """
    Remove "Nama :" and "No. Cert" from public message.
    """
    import re
    public_message = re.sub(r'\b' + "Nama : " + r'\b' ,'', public_message_raw)
    public_message = re.sub(r'\b' + "No.Cert : " + r'\b' ,'', public_message)
    return public_message