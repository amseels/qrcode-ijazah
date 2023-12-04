# Library for QR generation
from PIL import Image
from .  import qrGen
from .qrGen.qrEstimating import EstimatedQR as eQR
from .qrGen.generatingShares import vss
from .qrGen.generatingShareCodeword import ShareCodeword
from .qrGen.splitShare import splitShare

def generateQR(public_message: str, private_message: str):
	"""
	return QR with embedded public_message
	with option encode as 'base64'
	#TO_DO_LIST
	"""
	qr_version = eQR(private_message,public_message).print_qr_info()

	qr = qrGen.create(content=public_message,
						block_share_padding=__private_message_codeword(private_message),
						version=qr_version['H'][0],
						mode='binary',
						encoding='iso-8859-1',
						error='H')
	nowSize = qr.get_png_size()
	scale = 500 // nowSize
	qr_str = qr.png_as_base64_str(scale=scale)
	return qr_str

def __private_message_codeword(private_message):
	lists_codeword = []
	for i in range(len(private_message)):
		lists_codeword.append(ord(private_message[i]))
	return lists_codeword

