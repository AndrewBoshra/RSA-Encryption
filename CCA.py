import RSA
import jsonutils

def CCA(ciphertext, n, e, d, r):
    rInv = RSA.InvertModulo(r, n)
    r = RSA.PowMod(r, e, n)
    Cdash = RSA.PowMod(RSA.ConvertToInt(ciphertext)*r, 1, n)
    Cdash = RSA.ConvertToStr(Cdash)
    Y = RSA.getPlaintext(Cdash, n, d)
    M = RSA.PowMod(RSA.ConvertToInt(Y)*rInv, 1, n)
    M = RSA.ConvertToStr(M)
    return M

print('Choose mode of operation test mode->1, terminal mode->2')
mode = int(input('mode: '))

if mode == 2:
    print("Enter p, q, e, c, r")
    p = int(input('P: '))
    q = int(input('q: '))
    e = int(input('e: '))
    r = int(input('r: '))
    n = p*q
    phi = (p-1)*(q-1)
    plaintext = input('plaintext: ')
    ciphertext = RSA.getCiphertext(plaintext, n , e)
    d = RSA.InvertModulo(e, phi)
    print(CCA(ciphertext, n, e, d, r))

elif mode == 1:
    testCasesArr = jsonutils.getJsonData()
    for testcase in testCasesArr:
        p = testcase.get("p")
        q = testcase.get("q")
        e = testcase.get("e")
        r = testcase.get("r")
        plaintext = testcase.get("plaintext")
        n = p*q
        phi = (p-1)*(q-1)
        ciphertext = RSA.getCiphertext(plaintext, n , e)
        d = RSA.InvertModulo(e, phi)
        print(CCA(ciphertext, n, e, d, r))


