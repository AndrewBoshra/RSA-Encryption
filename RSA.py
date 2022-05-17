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

# def Decrypt(c, p, q, e):
#     Q = (p-1)*(q-1)
#     d = InvertModulo(e, Q)
#     c = ConvertToInt(c)
#     m = ConvertToStr(PowMod(c, d, p*q))
#     return m


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

    

# cipertext = getCiphertext('hello', 523631656370745185641961785048490596607211047839379680209373)
# print(cipertext, getPlaintext(cipertext, 523631656370745185641961785048490596607211047839379680209373, 49479765162766405466857617351938170521288251316432691224293))

# p = 790383132652258876190399065097
# q = 662503581792812531719955475509
# e = 23917
# d = 49479765162766405466857617351938170521288251316432691224293
# n = 523631656370745185641961785048490596607211047839379680209373


# Q = (p-1)*(q-1)
# d = InvertModulo(23917, Q)
# print(d)
#49479765162766405466857617351938170521288251316432691224293 inverse of 23917 in mod 523631656370745185641961785048490596607211047839379680209373


# p2 = 656917682542437675078478868539
# q2 = 1263581691331332127259083713503
# e2 = 25969
# d2 = 340414976139489631127124457943643467611960690702259322262729
# n2 = 830069156372432509928666201723843242135846274670597876182117
# cipertext = getCiphertext('helloiiii', 830069156372432509928666201723843242135846274670597876182117, 25969)
# print(cipertext, getPlaintext(cipertext, 830069156372432509928666201723843242135846274670597876182117, 340414976139489631127124457943643467611960690702259322262729))