import io
import itertools
"""
Program untuk memisahkan shares codeword yang akan ditaruh di padding codeword
dan yang ditaruh pada content/cover codeword.

Masukan program ini adalah share codeword, block codeword

block codeword adalah jumlah block pada QR Code. Setiap versi memiliki jumlah block yang berbeda.
Setiap block memiliki jumlah codeword.
"""
class splitShare():
    def __init__(self,secure_share_codewords=None,qr_information=None, cover_qr=None, ec_level=None):
        self.secure_share_codewords = secure_share_codewords
        self.list_number_of_error = qr_information['list_number_of_error'][ec_level]
        self.list_number_of_data = qr_information['list_number_of_data'][ec_level]
        self.number_of_max_cover = qr_information['number_of_max_cover'][ec_level]
        self.cover_qr = str(cover_qr)
        self.ec_level = ec_level
        self.qr_version = qr_information['QR_Version'][ec_level]
        
        self.split_info_secure_share_codeword()
        self.split_secure_share_codeword()
        self.block_secure_share_codeword_on_cover()
        self.block_secure_share_codeword_on_padding()

    def split_info_secure_share_codeword(self):
        ## menambah bit cci, mode, terminal. CCI pada mode binari, dibawah versi 10 sebesar 1 byte dan 10 keatas sebesar 2 byte,
        ## mode + terminal sebesar 1 byte.
        """Karena pada kasus ini mode QR yang digunakan adalah Byte,
        Jika versi QR lebih kecil dari 10. maka perlu menambahkan 2 byte pada.
        Sedangkan jika veri QR adalah 10 atau lebih makan perlu menambahkan 3 byte
        """
        if self.qr_version < 10 :
            self.total_content_codeword = len(self.cover_qr) + 2
        else :
            self.total_content_codeword = len(self.cover_qr) + 3
        print("total content coderword : ",self.total_content_codeword)
        self.blocks_number = 0
        while self.total_content_codeword > self.list_number_of_data[self.blocks_number] :
            self.total_content_codeword -= self.list_number_of_data[self.blocks_number]
            self.blocks_number += 1
        if self.total_content_codeword != 0:
            self.last_address_content_codeword = self.total_content_codeword
        else : 
            self.last_address_content_codeword = 0
        print("Total block number for content : ", self.blocks_number, "last_address_codeword : ",self.last_address_content_codeword)

    def split_secure_share_codeword(self):
        total_secure_share_codeword_on_cover = 0
        for i in range(self.blocks_number):
            total_secure_share_codeword_on_cover += self.list_number_of_error[i]
            # print(self.last_address_content_codeword,self.list_number_of_error[self.blocks_number])
        if self.last_address_content_codeword > self.list_number_of_error[self.blocks_number] :
            total_secure_share_codeword_on_cover += self.list_number_of_error[self.blocks_number]
        else :
            total_secure_share_codeword_on_cover += self.last_address_content_codeword
        # print("total_share_codeword_on_cover :",total_secure_share_codeword_on_cover)
        self.secure_share_codeword_on_cover = self.secure_share_codewords[:total_secure_share_codeword_on_cover]
        # print("secure_share_codeword_on_cover : \n",self.secure_share_codeword_on_cover)
        self.secure_share_codeword_on_padding = self.secure_share_codewords[total_secure_share_codeword_on_cover:]
        # print("secure_share_codeword_on_padding : \n",self.secure_share_codeword_on_padding)

    def block_secure_share_codeword_on_cover(self):
        self.block_secure_share_codeword_on_cover = []
        secure_share_codeword_on_cover = self.secure_share_codeword_on_cover
        for i in range(self.blocks_number):
            self.block_secure_share_codeword_on_cover.append(secure_share_codeword_on_cover[:self.list_number_of_error[self.blocks_number]])
            secure_share_codeword_on_cover = secure_share_codeword_on_cover[self.list_number_of_error[self.blocks_number]:]
        self.block_secure_share_codeword_on_cover.append(secure_share_codeword_on_cover[:self.list_number_of_error[self.blocks_number]])
        # print("block_secure_share_codeword_on_cover : \n",self.block_secure_share_codeword_on_cover)

    def block_secure_share_codeword_on_padding(self):
       
        self.block_secure_share_codeword_on_padding = []
        secure_share_codeword_on_padding = self.secure_share_codeword_on_padding
        print("secure_share_codeword_on_padding : \n",secure_share_codeword_on_padding)
        first_padding_on_data_blocks = self.block_secure_share_codeword_on_cover[-1]

        # mengisi block pertama
        jumlah_value_block_pertama = self.list_number_of_data[self.blocks_number] - self.last_address_content_codeword
        print("jumlah_value_block_pertama :",jumlah_value_block_pertama)
        block_value = secure_share_codeword_on_padding[:jumlah_value_block_pertama]
        if len(block_value) != 0 :
            self.block_secure_share_codeword_on_padding.append(block_value)
            secure_share_codeword_on_padding = secure_share_codeword_on_padding[jumlah_value_block_pertama:]
        print("Block Value : ",block_value)
        if self.blocks_number + 1 < len(self.list_number_of_error):
            i = 0
            blocks_number = self.blocks_number + 1
            while blocks_number < len(self.list_number_of_data):
                if len(secure_share_codeword_on_padding) > self.list_number_of_data[blocks_number] :
                    block_value = secure_share_codeword_on_padding[:self.list_number_of_data[blocks_number]]
                    secure_share_codeword_on_padding = secure_share_codeword_on_padding[self.list_number_of_data[blocks_number]:]
                else :
                    block_value = secure_share_codeword_on_padding
                    blocks_number = len(self.list_number_of_data)
                self.block_secure_share_codeword_on_padding.append(block_value)
                blocks_number += 1
                i += 1
            # print("block_secure_share_codeword_on_padding : \n",self.block_secure_share_codeword_on_padding)

    def print_secure_share_codeword_on_cover(self):
        return self.secure_share_codeword_on_cover

    def print_secure_share_codeword_on_padding(self):
        return self.secure_share_codeword_on_padding

    def print_block_secure_share_codeword_on_cover(self):
        return self.block_secure_share_codeword_on_cover

    def print_block_secure_share_codeword_on_padding(self):
        return self.block_secure_share_codeword_on_padding


## for debug
# from coverEstimating import EstimatedQRCover as eCov
# x = eCov('1.png')
# ec = 'H'
# cover = 'Hanang ww'

# # print(x.print_QR_info())
# y = [91, 85, 44, 11, 110, 132, 106, 0, 67, 150, 154, 23, 193, 70, 145, 226, 50, 162, 167, 234, 108, 51, 122, 20, 114, 1, 186, 181, 43, 196, 97, 40, 160, 136, 112, 113, 93, 14, 219, 120, 159, 169, 9, 74, 124, 232, 148, 224, 211, 9, 138, 125, 170, 206, 90, 46, 103, 225, 27, 222, 190, 55, 41, 82, 142, 137, 143, 9, 145, 230, 170, 122, 58, 50, 169, 96, 246, 63, 10, 72, 154, 176, 26, 212, 189, 131, 246, 153, 106, 222, 172, 69, 121, 103, 174, 213, 79, 80, 133, 197, 202, 188, 243, 10, 164, 93, 159, 207, 82, 216, 245, 88, 42, 123, 62, 15, 148, 80, 170, 195, 85, 27, 235, 26, 149, 242, 21, 193, 221, 177, 195, 84, 99, 52, 50, 236, 148, 123, 192, 90, 41, 127, 28, 21, 252, 20, 28, 93, 74, 123, 52, 168, 57, 7, 212]
# ss = splitShare(secure_share_codewords=y,qr_information=x.print_QR_info(),cover_qr=cover,ec_level=ec)
# print("block_secure_share_codeword_on_cover : \n",ss.block_secure_share_codeword_on_cover)
# print("block_secure_share_codeword_on_padding : \n",ss.block_secure_share_codeword_on_padding)