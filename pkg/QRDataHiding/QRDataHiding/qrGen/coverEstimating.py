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

class EstimatedQRCover:
    def __init__(self, content):
        #Melakukan cek apakah content image atau bukan
        self.content = content
        self.ec_symbol = ['L','M','Q','H']
        try :
            self.img = Image.open(self.content)
        except :
            raise ValueError('{0} is not a valid images.'.format(content))
        self.share_codeword()
        self.QRVersion()
        self.R_codewords()
        self.number_of_data()
        self.number_of_error()
        self.number_of_max_cover()

    def share_codeword(self):
        """
        b = ceil(M*N/8) + 1
        b = share codeword.
        """

        """
        Membutuhkan beberapa byte :
        1 byte untuk size image
        1 byte untuk nomer share.
        1 byte untuk total share yang diproduksi

        |s_share|...|n_share|t_share|
        """
        self.img = Image.open(self.content)
        self.img_size = self.img.size[1]
        self.b = math.ceil((self.img.size[0] * self.img.size[1])/8) + 3 #1 adalah 1 byte untuk byte size, 
 
    def QRVersion(self):   
        """
        QR Version T => b
        """
        self.qr_info = {'L':[],'M':[],'Q':[],'H':[]}
        for i in range(len(tables.data_capacity)):
            for j in range(len(tables.data_capacity[i+1])):
                if int(self.b) < int(tables.data_capacity[i+1][self.ec_symbol[j]][4]) :
                    if len(self.qr_info[self.ec_symbol[j]])==0:
                        self.qr_info[self.ec_symbol[j]].extend([i+1,tables.data_capacity[i+1][self.ec_symbol[j]][4]])
    
    def R_codewords(self):
        self.list_R = {'L':[],'M':[],'Q':[],'H':[]}
        for i in range(len(self.ec_symbol)):
            R = self.qr_info[self.ec_symbol[i]][1]-self.b 
            # self.qr_info[self.ec_symbol[i]].append(R)
            self.list_R[self.ec_symbol[i]].append(R)
    
    def number_of_data(self):
        #Perlu mengetahui total codeword per block,k,
        self.list_md = {'L':[],'M':[],'Q':[],'H':[]}
        for i in range(len(self.ec_symbol)):
            number_of_g1 = tables.eccwbi[self.qr_info[self.ec_symbol[i]][0]][self.ec_symbol[i]][1]
            number_of_d_codeword_g1 = tables.eccwbi[self.qr_info[self.ec_symbol[i]][0]][self.ec_symbol[i]][2]
            number_of_g2 = tables.eccwbi[self.qr_info[self.ec_symbol[i]][0]][self.ec_symbol[i]][3]
            number_of_d_codeword_g2 = tables.eccwbi[self.qr_info[self.ec_symbol[i]][0]][self.ec_symbol[i]][4]            
            #Group Block Pertama
            for kk in range(number_of_g1):
                m = number_of_d_codeword_g1
                self.list_md[self.ec_symbol[i]].append(m)
            #Group Block Kedua
            for kk in range(number_of_g2):
                m = number_of_d_codeword_g2
                self.list_md[self.ec_symbol[i]].append(m)
                # self.qr_info[self.ec_symbol[i]].append(R)

    def number_of_error(self):
        #Perlu mengetahui total codeword per block,k,
        self.list_m = {'L':[],'M':[],'Q':[],'H':[]}
        for i in range(len(self.ec_symbol)):
            ec_codeword = tables.eccwbi[self.qr_info[self.ec_symbol[i]][0]][self.ec_symbol[i]][0]
            number_of_g1 = tables.eccwbi[self.qr_info[self.ec_symbol[i]][0]][self.ec_symbol[i]][1]
            number_of_d_codeword_g1 = tables.eccwbi[self.qr_info[self.ec_symbol[i]][0]][self.ec_symbol[i]][2]
            number_of_g2 = tables.eccwbi[self.qr_info[self.ec_symbol[i]][0]][self.ec_symbol[i]][3]
            number_of_d_codeword_g2 = tables.eccwbi[self.qr_info[self.ec_symbol[i]][0]][self.ec_symbol[i]][4]
            e = tables.point_error_level[self.ec_symbol[i]]
            
            #Group Block Pertama
            for kk in range(number_of_g1):
                m = math.floor((ec_codeword + number_of_d_codeword_g1) * e) 
                self.list_m[self.ec_symbol[i]].append(m)
            #Group Block Kedua
            for kk in range(number_of_g2):
                m = math.floor((ec_codeword + number_of_d_codeword_g2) * e)
                self.list_m[self.ec_symbol[i]].append(m)
                # self.qr_info[self.ec_symbol[i]].append(R)

    def number_of_max_cover(self):
        self.list_C = {'L':[],'M':[],'Q':[],'H':[]}
        for i in range(len(self.ec_symbol)):
            number_of_d_codeword_g1 = tables.eccwbi[self.qr_info[self.ec_symbol[i]][0]][self.ec_symbol[i]][2]
            
            C = self.list_m[self.ec_symbol[i]][0]
            R = self.list_R[self.ec_symbol[i]][0]
            len_m = len(self.list_m[self.ec_symbol[i]])
            
            for j in range(len_m-1):
                kk = number_of_d_codeword_g1
                mm = self.list_m[self.ec_symbol[i]][j+1]
                R = R - (kk - mm)
                if R > 0 :
                    C = C + mm
            C = C - 2
            self.list_C[self.ec_symbol[i]].append(C)

    def print_share_codeword(self):
        return self.b, self.img_size  

    def print_QRVersion(self):
        return self.qr_info 
    
    def print_R_codewords(self):
        return self.list_R
    
    def print_number_of_data(self):
        return self.list_md
   
    def print_number_of_error(self):
        return self.list_m
    
    def print_number_of_max_cover(self):
        return self.list_C

    def print_QR_info(self):
        qr_inf = {
            'size_pixel' : self.img_size,
            'share_codeword' : self.b, 
            'QR_Version' : {
                'L' : self.qr_info['L'][0],
                'M' : self.qr_info['M'][0],
                'Q' : self.qr_info['Q'][0],
                'H' : self.qr_info['H'][0]
                },
            'codeword_capacity' :{
                'L' : self.qr_info['L'][1],
                'M' : self.qr_info['M'][1],
                'Q' : self.qr_info['Q'][1],
                'H' : self.qr_info['H'][1]
                },
            'remainder_codeword' :{
                'L' : self.qr_info['L'][0],
                'M' : self.qr_info['M'][0],
                'Q' : self.qr_info['Q'][0],
                'H' : self.qr_info['H'][0]
                },
            'list_number_of_error' : self.list_m,
            'list_number_of_data' : self.list_md,
            'number_of_max_cover' : {
                'L' : self.list_C['L'][0],
                'M' : self.list_C['M'][0],
                'Q' : self.list_C['Q'][0],
                'H' : self.list_C['H'][0]
                }
            }
        return qr_inf
    

# secret = [30,35,40,45,50,55,60,65,70,75,80,85,90,95,100]
# path = 'SecretShares/hit'
# data = {'size image':secret,
#         'estimated share codeword':[],

#         'estimated qr version L':[],
#         'maksimum cover character L':[],
        
#         'estimated qr version M':[],
#         'maksimum cover character M':[],

#         'estimated qr version Q':[],
#         'maksimum cover character Q':[],

#         'estimated qr version H':[],
#         'maksimum cover character H':[],
#         }
# for i in range(len(secret)):
#     files = path+'/hit%s/hit%s_bw.png'%(secret[i],secret[i])
#     ec = EstimatedQRCover(content=files)
#     data['estimated share codeword'].append(ec.print_share_codeword()[0])
#     data['estimated qr version L'].append(ec.print_QRVersion()["L"][0])
#     data['maksimum cover character L'].append(ec.print_number_of_max_cover()["L"][0])

#     data['estimated qr version M'].append(ec.print_QRVersion()["M"][0])
#     data['maksimum cover character M'].append(ec.print_number_of_max_cover()["M"][0])

#     data['estimated qr version Q'].append(ec.print_QRVersion()["Q"][0])
#     data['maksimum cover character Q'].append(ec.print_number_of_max_cover()["Q"][0])

#     data['estimated qr version H'].append(ec.print_QRVersion()["H"][0])
#     data['maksimum cover character H'].append(ec.print_number_of_max_cover()["H"][0])
#     # print("Estimate Share Codeword : ",ec.print_share_codeword()[0],"Codeword")
#     # print("Estimate QR Version  : ",ec.print_QRVersion())
#     # print("Number of Cover Characters : ",ec.print_number_of_max_cover(),"Characters")
# print(data,"\n")

# import pandas as pd
# # Membuat DataFrame
# df = pd.DataFrame(data)

# # Menulis data ke file Excel
# filename = 'data.xlsx'
# writer = pd.ExcelWriter(filename, engine='openpyxl')
# df.to_excel(writer, sheet_name='Data', index=False)
# writer.save()

# print(f'File {filename} berhasil dibuat')
##############################################################

# secret = [35,40,45,50,55,60,65,70,75,80,85,90,95,100]
# # secret = [55]

# path = 'SecretShares/hit'

# import os
# for i in range (len(secret)):
#     files = path+'/hit%s/hit%s_bw.png'%(secret[i],secret[i])
#     # print(files)
#     x = EstimatedQRCover(files)
#     # print(x.print_share_codeword())
#     # print(x.print_QRVersion())
#     # print(x.print_R_codewords())
#     # print(x.print_number_of_error())
#     print(
#         # secret[i],
#         x.print_share_codeword(),
#         x.print_QRVersion()['H'], 
#         x.print_R_codewords()['H'],
#         # x.print_number_of_data()['H'],
#         # x.print_number_of_error()['H'],
#         x.print_number_of_max_cover()
#     )
#     # print(x.print_QR_info())