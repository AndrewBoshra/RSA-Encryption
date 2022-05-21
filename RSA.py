import sys, threading
import numpy as np
import sympy

sys.setrecursionlimit(10**7)
threading.stack_size(2**27)
def isPrime(numStr):
    if not numStr.isnumeric():
        return False
    num=int(numStr)
    if num<=1:
        return False
    
    for n in range(2,int(num**0.5)+1):
        if num%n==0:
            return False
    return True
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

def generatePrime(min=1000000000, max=1000000000000):
    return sympy.randprime(min, max)

def generateKeys(min=1000000000, max=1000000000000):
    p = generatePrime(min, max)
    q = generatePrime(min, max)
    n = p*q
    phi = (p-1)*(q-1)
    e = generatePrime(2, phi)
    d = InvertModulo(e, phi)
    return n, d, e

def Encrypt(m, n, e):
    c = ConvertToStr(PowMod(ConvertToInt(m), e, n))
    return c



def Decrypt(c, n, d):
    c = ConvertToInt(c)
    m = ConvertToStr(PowMod(c, d, n))
    return m

def getCiphertext(message, modulo = 17, exponent = 23917):
    ciphertext = Encrypt(message, modulo, exponent)
    return ciphertext

def getPlaintext(ciphertext, modulo = 17, exponent = 23917):
    message = Decrypt(ciphertext, modulo, exponent)
    return message

def splitString(str, n = 20):
    chunks = [str[i:i+n] for i in range(0, len(str), n)]
    return chunks

    