import sys, threading
import numpy as np

sys.setrecursionlimit(10**7)
threading.stack_size(2**27)

def ConvertToInt(message_str):
  res = 0
  for i in range(len(message_str)):
    res = res * 256 + ord(message_str[i])
  return res

def ConvertToStr(n):
    res = ""
    while n > 0:
        res += chr(n % 256)
        n //= 256
    return res[::-1]

def GCD(a, b):
  if b == 0:
    return a
  return GCD(b, a % b)

def ExtendedEuclid(a, b):
    if b == 0:
        return (1, 0)
    (x, y) = ExtendedEuclid(b, a % b)
    k = a // b
    return (y, x - k * y)

# this is an R2L recursive implementation that works for large integers
def PowMod(a, n, mod): 
    if n == 0:
        return 1 % mod
    elif n == 1:
        return a % mod
    else:
        b = PowMod(a, n // 2, mod)
        b = b * b % mod
        if n % 2 == 0:
          return b
        else:
          return b * a % mod

def InvertModulo(a, n):
    (b, x) = ExtendedEuclid(a, n)
    if b < 0:
        b = (b % n + n) % n # we don't want -ve integers
    return b

# %% Question 1
def Encrypt(m, n, e):
    c = ConvertToStr(PowMod(ConvertToInt(m), e, n))
    return c

def Decrypt(c, p, q, e):
    Q = (p-1)*(q-1)
    d = InvertModulo(e, Q)
    c = ConvertToInt(c)
    m = ConvertToStr(PowMod(c, d, p*q))
    return m


def getCiphertext(message, p = 790383132652258876190399065097, q = 662503581792812531719955475509, exponent = 23917):
    modulo = p * q
    ciphertext = Encrypt(message, modulo, exponent)
    # message = Decrypt(ciphertext, p, q, exponent)
    # print(message)
    return ciphertext

def getPlaintext(ciphertext, p = 790383132652258876190399065097, q = 662503581792812531719955475509, exponent = 23917):
    message = Decrypt(ciphertext, p, q, exponent)
    return message

cipertext = getCiphertext('hello')
print(cipertext, getPlaintext(cipertext))

