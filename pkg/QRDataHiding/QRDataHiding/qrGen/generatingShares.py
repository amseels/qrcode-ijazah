from numpy import asarray,uint8, random,bitwise_xor
from PIL import Image

class vss():
    """
    def __init__(self,secret_img,k=2,n=3):
        self.secret_img = asarray(Image.open(secret_img).convert("1")).astype(int)
        self.k = k
        self.n = n
        self.x= len(self.secret_img)
        self.y= len(self.secret_img[0])
        self.generate_kn()
    def generate_kn(self): 
        self.dm = {}
        ## Step 2. Create Matrix s1,s2, sb, ... ,sn, with same size to S
        for a in range (self.n):
            self.dm['s{}'.format(a+1)] = random.choice([3],size=(self.x,self.y))
        
        #inisiasi s2 baris pertama dengan s1 baris ke 2 sampai terakhir
        #s(n-1) baris pertama
        self.dm["s%s"%(self.n-1)][0] = self.secret_img[0]
        #s1 baris ke 2 sampai baris terakhir
        for a1 in range(1,self.x):
            self.dm["s1"][a1] = self.secret_img[a1]

        ## Random bit baris pertama dari S1 sampai S(N-2)
        for b in range(self.n-2):
            self.dm["s%s"%(b+1)][0] = random.choice([0,1],size=(1,self.y))
            #print(self.dm["s%s"%(b+1)])
        
        for c in range(2,self.y):
            self.dm["s%s"%(self.n)][c] = random.choice([0,1],size=(1,self.y))
            #print(dm["s%s"%(self.n)])

        #sn-1 baris pertama dan sn baris ke 2
        for d in range(self.n-2):
            self.dm["s%s"%(self.n-1)][0] = bitwise_xor(self.dm["s%s"%(self.n-1)][0],self.dm["s%s"%(d+1)][0])
        self.dm["s%s"%(self.n)][1] = self.dm["s%s"%(self.n-1)][0]

        #mengisi data dari s1 sampai sn-2
        ### CEK LAGI HANANG
        for e in range(1,self.x): #melakukan pengisian dari baris 2 sampai baris terakhir
            for f in range(self.n - 1): #melakukan pengisian pada sn-1 sampai s1
                if (self.n-1)-f != 1: #untuk sn-1 sampai sn-2
                    self.dm["s%s"%((self.n-1)-f)][e] = bitwise_xor(self.dm["s%s"%((self.n-1)-f-1)][e-1],self.dm["s%s"%((self.n-1)-f+1)][e])
                else :
                    for g in range(1,self.n-1):
                        self.dm["s1"][e] = bitwise_xor(self.dm["s1"][e],self.dm["s%s"%(g+1)][e])
        self.dm["s%s"%(self.n)][0] = self.dm["s1"][self.x-1]              
    def print_share_mtx(self):
        return self.dm
    def print_secret_img_mtx(self):
        return self.secret_img     
    def print_mtx_to_img(self):
        j = Image.fromarray(uint8(self.secret_img)*255)
        return j
    def generate_share_image(self):
        for a in range(self.n):
            j = Image.fromarray(uint8(self.dm["s%s"%(a+1)])*255)
            j.save('%s.png'%(a+1))
    """

    """
    Semua baris s2, sn-1 di xor dengan sebelum dan sesudah
    """
    def __init__(self,secret_img,k=2,n=3):
        self.secret_img = asarray(self.binarize(secret_img)).astype(int)
        self.k = k
        self.n = n
        self.x= len(self.secret_img)
        self.y= len(self.secret_img[0])
        self.generate_kn()
        self.generate_share_image()

    def binarize(self,images):
        #initialize threshold
        thresh=128
        #convert image to greyscale
        
        img=Image.open(images).convert('L') 
        width,height=img.size
        #traverse through pixels 
        for x in range(width):
            for y in range(height):
            #if intensity less than threshold, assign white
                if img.getpixel((x,y)) < thresh:
                    img.putpixel((x,y),0)
            #if intensity greater than threshold, assign black 
                else:
                    img.putpixel((x,y),255)
        return img

    def print_secret_img_asarray(self):
        return self.secret_img
    
    def generate_kn(self):
        self.dm = {}
        ## Step 2. Create Matrix s1,s2, sb, ... ,sn, with same size to S
        for a in range (self.n):
            self.dm['s{}'.format(a+1)] = random.choice([3],size=(self.x,self.y))
        
        ## fill s(n-1) 1st with self.secret_img[0]
        self.dm['s{}'.format(self.n-1)][0] = self.secret_img[0]

        # print("first eow sn-1 : ",self.dm['s{}'.format(self.n-1)][0])
        ### Generate random matrix s1,...,s(n-2) in first row
        for a in range (self.n - 2):
            self.dm['s{}'.format(a+1)][0] = random.choice([0,255],size=(1,self.y))
            self.dm['s{}'.format(self.n-1)][0] = bitwise_xor( self.dm['s{}'.format(self.n-1)][0],self.dm['s{}'.format(a+1)][0])


        #fill s(n) row 2 with 1st row in s(n-1) 
        self.dm['s{}'.format((self.n))][1] = self.dm['s{}'.format((self.n-1))][0]

        # generate ranbom 2nd row until last row in s(n)
        for a in range(2,self.x):
            self.dm['s{}'.format(self.n)][a] = random.choice([0,255],size=(1,self.y))
        

        # print(self.dm)
        # # # mengisi s1,..., s(n-1)
        for b in range(1,self.x):
            self.dm['s1'][b] = self.secret_img[b] #me-inisialiasasi setiap baris pada s1 dari baris 2 ke baris terakhir adalah secret
            
            # memgisi seluruh baris pada setiap share
            for a in range(1,self.n - 1):
                print("mengisi baris ke %s pada share ke %s"%(b+1,(self.n)-a))
                print(("share ke : {} , baris ke : {} ".format((((self.n)-a)-1) , b-1+1), self.dm['s{}'.format(((self.n)-a)-1)][b-1]))
                print(("share ke : {} , baris ke : {} ".format((((self.n)-a)+1),b+1), self.dm['s{}'.format(((self.n)-a)+1)][b]))
                
                self.dm['s{}'.format((self.n)-a)][b] = bitwise_xor(self.dm['s{}'.format(((self.n)-a)-1)][b-1], self.dm['s{}'.format(((self.n)-a)+1)][b])
                print(("share ke : {} , baris ke : {} ".format((((self.n)-a)),b+1), self.dm['s{}'.format((self.n)-a)][b]))

                
                self.dm['s1'][b] = bitwise_xor(self.dm['s1'][b],self.dm['s{}'.format((self.n)-a)][b])
                # print('s', b, self.dm['s1'][b])
                print("\n")
        self.dm['s{}'.format(self.n)][0] = self.dm['s1'][self.x-1]

    def generate_share_image(self):
        for a in range(self.n):
            j = Image.fromarray(uint8(self.dm["s%s"%(a+1)]))
            j.save('%s.png'%(a+1))

    def print_array_shares(self):
        # self.dm
        return self.dm


class vss_rekonstruct:
    def __init__(self, list_image):
        self.list_image = list_image
    
    def binarize(self,images):
        #initialize threshold
        thresh=128
        #convert image to greyscale
        
        img=Image.open(images).convert('L') 
        width,height=img.size
        #traverse through pixels 
        for x in range(width):
            for y in range(height):
            #if intensity less than threshold, assign white
                if img.getpixel((x,y)) < thresh:
                    img.putpixel((x,y),255)
            #if intensity greater than threshold, assign black 
                else:
                    img.putpixel((x,y),0)
        return img

    def list_array(self):
        array_img = self.binarize(self.list_image[0])
        for i in range(1,len(self.list_image)): 
           array_img = bitwise_xor(array_img,self.binarize(self.list_image[i]))

        print(array_img)
        # Image.fromarray(uint8(array_img)).show()

"""Uji coba membuat share dari file PNG"""

# x = vss('5px.png',k=4,n=5)
# print(x.print_array_shares())
# print(x.secret_img)

# list_image = ['1.png','2.png','3.png','4.png']
# y = vss_rekonstruct(list_image)
# print(y.list_array())
