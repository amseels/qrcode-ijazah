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
import bitarray
from numpy import asarray,bitwise_xor,binary_repr,append
from PIL import Image

class ShareCodeword:
    def __init__(self, content,temporary_passcode,number_share):
        #Melakukan cek apakah content image atau bukan
        self.content = content
        self.tp = str(temporary_passcode)
        self.number_share = number_share
        try :
            self.img = asarray(Image.open(content).convert("1")).astype(int)
        except :
            raise ValueError('{0} is not a valid images.'.format(content))
        self.share_codewords()
        self.secure_share_codewords()

    def grouper(self, n, iterable, fillvalue=None):
        """This generator yields a set of tuples, where the
        iterable is broken into n sized chunks. If the
        iterable is not evenly sized then fillvalue will
        be appended to the last tuple to make up the difference.
        This function is copied from the standard docs on
        itertools.
        """
        args = [iter(iterable)] * n
        if hasattr(itertools, 'zip_longest'):
            return itertools.zip_longest(*args, fillvalue=fillvalue)
        return itertools.izip_longest(*args, fillvalue=fillvalue)

    def share_codewords(self):
        from math import sqrt
        import io
        share_stream_bit = self.img.flatten()
        # print("share_stream_bit : ",sqrt(len(share_stream_bit)))
        self.len_share_decimal = int(sqrt(len(share_stream_bit)))
        # print(self.len_share_decimal)
        self.share_stream_bit = ''.join([str(elem) for elem in share_stream_bit])
        while (len(self.share_stream_bit) % 8) != 0 :
            self.share_stream_bit = self.share_stream_bit + '0'
        # print(len(self.share_stream_bit))
        self.share_codeword = [int(''.join(x),2) for x in self.grouper(8, self.share_stream_bit)]
    
    def secure_share_codewords(self):
        self.secure_share_codeword = self.share_codeword.copy()
        for i in range(len(self.share_codeword)):
            self.secure_share_codeword[i] = self.secure_share_codeword[i] ^ ord(self.tp[i%len(self.tp)])
        # karena M = N, maka cukup memasukan informasi M atau N pada alamat pertama dalam list. 
        self.secure_share_codeword.insert(0,self.len_share_decimal+self.number_share)

    def print_share_codeword(self):
        return self.share_codeword
    
    def print_temp_pass(self):
        return self.tp
    
    def print_secure_share_codeword(self):
        return self.secure_share_codeword
        
# x = ShareCodeword('1.png','xMdpT',1)
# print(x.print_share_codeword())
# print(x.print_temp_pass())
# print(x.print_secure_share_codeword())
    
    