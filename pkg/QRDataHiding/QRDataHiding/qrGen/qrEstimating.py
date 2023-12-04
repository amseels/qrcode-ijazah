from __future__ import absolute_import, division, print_function, with_statement, unicode_literals

#import pyqrcode.tables as tables
try :
    from . import tables as tables
except :
    import tables
import io
import itertools
import math
import imghdr
from numpy import asarray
from PIL import Image

class EstimatedQR:
    def __init__(self,public_message,private_message):
        self.ec_symbol = ['L','M','Q','H']
        self.public_message = public_message
        self.private_message = private_message
        self.total_data = public_message + private_message
        self.len_total_data = len(self.total_data)
        self.QR_version()

    def QR_version(self):
        self.qr_info = {'L':[],'M':[],'Q':[],'H':[]}
        for i in range(len(tables.data_capacity)):
            for j in range(len(tables.data_capacity[i+1])):
                if int(self.len_total_data) < int(tables.data_capacity[i+1][self.ec_symbol[j]][4]) :
                    if len(self.qr_info[self.ec_symbol[j]])==0:
                        self.qr_info[self.ec_symbol[j]].extend([i+1,tables.data_capacity[i+1][self.ec_symbol[j]][4]])

    def print_qr_info(self):
        return self.qr_info

# public_message = """
# Magister Certificate
# Nama : Nabila Bilqisti Rodiah
# No.Cert : 114051234512345
# """

# private_message = """
# IOUTR.1EDCD7352773A58028A770E386488BFF
# BF2519D01906BEF0A.566F14F060828860C5FBB
# 4962CCE887804AC3E322D8C0F600BBF2441AEB
# 74B07C519BF3039D20B10D6BC1509982F8708
# .10/04/2023.0000
# """
# print(EstimatedQR(private_message,public_message).print_qr_info())
