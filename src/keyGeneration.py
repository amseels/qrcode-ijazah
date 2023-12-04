from dataclasses import dataclass
import hashlib
from IBS import Point, EllipticCurve
import random

@dataclass
class CADummy:
	EC: EllipticCurve
	standard: str
	Pub: Point
	__s: int

	def __init__(self, curveStd: str, s = int):
		"""
		inisiasi dengan security k based on curve standard:
			bn158, toyF13, typeG, p224, sect163k1
		setup by KGC
		s is master secret paramater; s = {1,..q-1}
		Pub is master public paraemetr; Pub = s*generator point in choosen curve
		"""
		self.EC = EllipticCurve(curveStd)
		self.standard = curveStd
		self.__s = s
		self.Pub = self.__setup(self.EC, self.__s)


	def __setup(self, EC: EllipticCurve, s):
		"""
		setup by KGC
		s is master secret paramater; s = {1,..q-1}
		Pub is master public paraemetr; Pub = s*generator point in choosen curve
		"""
		print('SETUP')
		Pub = EC.multiplication_point(s, EC.P) #s*P
		return Pub

	def extract(self, ID):
		"""
		– CA computes
		public key: QID = H1(ID) ∈ Zq∗.
		– CA computes
		private key: dID = (r_ID + sQID) ∈ Zq∗.
		– CA sends dID to the signer securely.
		– CA also compute V_ID = r_ID*P  and Z_ID = d_ID*P ∈ G.
		– CA announces ZID and
		VID as public parameter.
		"""
		Q_ID =  self.H1(str(ID))
		r_ID = self.__getRmid() % self.EC.p
		d_ID = ((r_ID + self.__s) * Q_ID) % self.EC.p
		V_ID = self.EC.multiplication_point(r_ID, self.EC.P) #r_ID*P
		Z_ID = self.EC.multiplication_point(d_ID, self.EC.P) #d_ID*P
		print("=== IBS EXTRACT ===")
		print("s =", self.__s)
		print("Q_ID =", r_ID)
		print("d_ID =", d_ID)
		print("V_ID =", V_ID)
		print("Z_ID =", Z_ID)
		print("Pub =", self.Pub)
		print("ID = \"" + ID + "\"")
		print("standard = \"" + self.standard + "\"")
		print()

		return d_ID, V_ID, Z_ID
	

	def H1(self, m):
		"""
		a futnion to map the message or binary string to the Field (Zp) element
		"""
		h = int(self.__hash(str(m)))
		h_int = h % self.EC.n
		return h_int

	def H2(self, m1, m2, G1: Point, G2: Point):
		"""
		Hash function H2 will map the space of all TWO bit strings ({0,1}*) and TWO element in G (G) into {1,..l-1}    
		"""
		h1 = int(self.__hash(m1)) % self.EC.n
		h2 = int(self.__hash(m2)) % self.EC.n
		G1_ = self.EC.multiplication_point(h1, G1)
		G2_ = self.EC.multiplication_point(h2, G2)
		xVal = G1_.x + G2_.x
		xVal_int = int(xVal) % self.EC.n
		return xVal_int
	
	def __hash(self, m):
		m_clean = m.replace(" ", "")
		m_clean = m.lower()
		h = hashlib.sha3_256()
		h.update(str(m_clean).encode('utf-8'))
		h_int = int(h.hexdigest(), 16)
		return h_int

	def __getRmid(self):
		from random import SystemRandom
		cryptogen = SystemRandom()
		randInt = cryptogen.randrange(int((self.EC.n-1)/2))
		return randInt