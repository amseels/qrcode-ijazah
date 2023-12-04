"""
Math functions used in Elliptic Curve function.
"""
import random
import hashlib
from gmpy2 import is_prime
#Hash
def Hash(m):
    m_clean = m.replace(" ", "")
    m_clean = m.lower()
    h = hashlib.sha3_256()
    h.update(str(m_clean).encode('utf-8'))
    h_int = int(h.hexdigest(), 16)
    return h_int

def __find_power_divisor(base, x, modulo=None):
        k = 0
        m = base
        while x % m == 0:
            k += 1
            m = pow(m * base, 1, modulo)
        return k

def __find_power(power_base, x, crib, modulo=None):
    k = 1
    r = power_base
    while pow(x, r, modulo) != crib:
        k += 1
        r *= power_base
    return k

def multiInv_ECC(a,b):
        (xt,ct,yt) = (0,0,0)
        x1=1
        x2=0
        y1=0
        y2=1
        c1=x1*a+y1*b
        c2=x2*a+y2*b
        while c2>1 :
            var_pengali = c1//c2
            ct,xt,yt = c1,x1,y1
            c1,x1,y1 = c2,x2,y2

            c2 = ct-(c2*var_pengali)
            x2 = xt-(x2*var_pengali)
            y2 = yt-(y2*var_pengali)
        return y2

def legendre_symbol(a, p):
        """
        Calculate Legendre Symbol using Euler's criterion
        """
        if gcd(a, p) != 1:
            return 0
        d = pow(a, ((p - 1) // 2), p)
        if d == p - 1:
            return -1
        return 1



def modinv(a, m):
    """
    Calculate Modular Inverse.
    - Find x satisfy ax \equiv 1 \mod m
    Args:
        a: target number
        n: modulus
    """
    if gcd(a, m) != 1:
        return 0
    if a < 0:
        a %= m
    return egcd(a, m)[1] % m

def gcd(x, y):
    """
    Calculate greatest common divisor
    """
    while y != 0:
        t = x % y
        x, y = y, t
    return x

def egcd(a, b):
    """
    Calculate Extended-gcd
    """
    x, y, u, v = 0, 1, 1, 0
    while a != 0:
        q, r = b // a, b % a
        m, n = x - u * q, y - v * q
        b, a, x, y, u, v = a, r, u, v, m, n
    return (b, x, y)


def calculate_square_root_modular(a, m):
  if is_prime(m):
    if legendre_symbol(a, m) == -1:
      return []
    # Tonelli-Shanks Algorithm
    if m % 4 == 3:
      r = pow(a, (m + 1) // 4, m)
      return [r, m - r]
    s = __find_power_divisor(2, m - 1)
    q = (m - 1) // 2**s
    z = 0
    while legendre_symbol(z, m) != -1:
      z = random.randint(1, m)
    c = pow(z, q, m)
    r = pow(a, (q + 1) // 2, m)
    t = pow(a, q, m)
    l = s
    while True:
      if t % m == 1:
        assert (r ** 2) % m == a
        return [r, m - r]
      i = __find_power(2, t, 1, m)
      power = l - i - 1
      if power < 0:
        power = modinv(2**-power, m)
      else:
        power = 2**power
      b = pow(c, power, m)
      r = (r * b) % m
      t = (t * (b**2)) % m
      c = pow(b, 2, m)
      l = i
  if m == 2:
    return a
  if m % 4 == 3:
    r = pow(a, (m + 1) // 4, m)
    return [r, m - r]
  if m % 8 == 5:
    v = pow(2 * a, (m - 5) // 8, m)
    i = pow(2 * a * v, 2, m)
    r = a * v * (i - 1) % m
    return [r, m - r]
  if m % 8 == 1:
    e = __find_power_divisor(2, m - 1)
    q = (m - 1) // 2**e
    z = 1
    while pow(z, 2**(e - 1), m) == 1:
      x = random.randint(1, m)
      z = pow(x, q, m)
    y = z
    r = e
    x = pow(a, (q - 1) // 2, m)
    v = a * x % m
    w = v * x % m
    while True:
      if w == 1:
        return [v, m - v]
      k = __find_power(2, w, 1, m)
      d = pow(y, 2**(r - k - 1), m)
      y = pow(d, 2, m)
      r = k
      v = d * v % m
      w = w * y % m