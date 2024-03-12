from dataclasses import dataclass
import hashlib
from .EllipticCurve import Point, EllipticCurve
import random

@dataclass
class IdentityBasedSignature:
	"""
		Identity-based Signature.
		Attributes:
		EC: EllipticCurve used
		s: system master key
		Pub: master public parameter
	"""
	EC: EllipticCurve
	Pub: Point

	def __init__(self, curveStd: str, Pub = Point):
		"""
		inisiasi dengan security k based on curve standard:
			bn158, toyF13, typeG, p224, sect163k1
		setup by KGC
		s is master secret paramater; s = {1,..q-1}
		Pub is master public paraemetr; Pub = s*generator point in choosen curve
		"""
		self.EC = EllipticCurve(curveStd)
		self.Pub = Pub

	# def __init__(self, curveStd: str):
	#   """Pub
	#   inisiasi dengan security k based on curve standard:
	#       bn158, toyF13, typeG, p224, sect163k1
	#   """
	#   self.EC = EllipticCurve(curveStd)

	def sign(self, ID, m, d_ID: int, Z_ID: Point):
		"""
		User sign the message using geenrtae secret key VA and they ID
		Pick a random number r_mid E Z/L* //r E {0,1,..l-1}
		at random corresponding to m and ID
		"""
		x_ID = self.__getRmid() % self.EC.n
		S1 = self.EC.multiplication_point(x_ID, Z_ID) #x_ID*Z_ID
		S1_compressed = self.EC.pointCompression(S1)
		h = self.H2(m, ID, Z_ID, self.Pub)
		S2 = ((x_ID + h) % self.EC.n) * d_ID
		print("=== IBS SIGN ===")
		print("n", self.EC.n)
		print("Z_ID", Z_ID)
		print("Pub", self.Pub)
		print("P", self.EC.P)
		print("h", h)
		print("S1", S1)
		print("S2", S2)
		print()
		return S1_compressed, S2

	def verify(self, S1_compressed: str, S2: int, m, ID, Z_ID: Point):
		"""
		#TO_DO_LIST
		"""
		S1 = self.EC.pointDecompression(S1_compressed)
		h = self.H2(m, ID, Z_ID, self.Pub)

		

		a1 = self.EC.multiplication_point(S2, self.EC.P)
		temp = self.EC.multiplication_point(h, Z_ID)
		a2 =  self.EC.addition_point(S1, temp)
		print("== IBS VERIFY ===")
		print("n", self.EC.n)
		print("Z_ID", Z_ID)
		print("Pub", self.Pub)
		print("P", self.EC.P)
		print("h", h)
		print("S1", S1)
		print("S2", S2)
		print("a1", a1)
		print("a2", a2)
		verifyStat = (a2 == a1)
		print('verifyStat',verifyStat)
		return verifyStat
	

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
