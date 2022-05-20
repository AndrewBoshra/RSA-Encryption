import RSA
import jsonutils
import json
from Crypto.Util import number

#this function takes as input the number of test cases to generate and an array of equal size of plaintext and the json file name to be created with the testcases
def gentestCases(plaintextArr, filename):
    data = {"testcases": []}
    for i in range(len(plaintextArr)):
        p = number.getPrime(128)
        q = number.getPrime(128)
        e = number.getPrime(56)
        r = number.getPrime(28)
        cipherint = RSA.ConvertToInt(RSA.getCiphertext(plaintextArr[i], p*q, e))
        data.get("testcases").append({"p": p, "q": q, "e": e, "r": r, "cipherint": cipherint})
    with open(filename, 'w') as file:
        json.dump(data, file, indent=2)


def CCA(ciphertext, n, e, d, r):
    rInv = RSA.InvertModulo(r, n)
    r = RSA.PowMod(r, e, n)
    Cdash = RSA.PowMod(RSA.ConvertToInt(ciphertext)*r, 1, n)
    Cdash = RSA.ConvertToStr(Cdash)
    Y = RSA.getPlaintext(Cdash, n, d)
    M = RSA.PowMod(RSA.ConvertToInt(Y)*rInv, 1, n)
    M = RSA.ConvertToStr(M)
    return M


def selfCheck(optainedPlaintext, actualPlaintext):
    if len(optainedPlaintext) != len(actualPlaintext):
        return 'sizes mismatch'
    for i in range (len(optainedPlaintext)):
        if (optainedPlaintext[i] == actualPlaintext[i]):
            print(f"Optained plaintext: {optainedPlaintext[i]}, Actual plaintext: {actualPlaintext[i]}, Matched")
        else:
            print(f"Optained plaintext: {optainedPlaintext[i]}, Actual plaintext: {actualPlaintext[i]}, Mismatched")       

optainedPlaintext = []

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
    #create text cases file
    actualPlaintext = []
    testcasesCount = 0
    print('would you like to enter the test cases yourself?')
    wish = input('[Y/N]: ')
    if str.lower(wish) == 'n':
        actualPlaintext = ["hello", "hi", "wohaa"]
    if str.lower(wish) == 'y':
        print('once done hit q')
        testcase = input(f"testcase no.{testcasesCount+1}: ")
        if(str.lower(testcase) == 'q'):
            actualPlaintext = ["hello", "hi", "wohaa"]
        while(str.lower(testcase) != 'q'):
            actualPlaintext.append(testcase)
            testcasesCount += 1
            testcase = input(f"testcase no.{testcasesCount+1}: ")
    gentestCases(actualPlaintext, 'CCAtestcases.json')
    testCasesArr = jsonutils.getJsonData('CCAtestcases.json')
    for testcase in testCasesArr:
        p = testcase.get("p")
        q = testcase.get("q")
        e = testcase.get("e")
        r = testcase.get("r")
        ciphertext = RSA.ConvertToStr(testcase.get("cipherint"))
        n = p*q
        phi = (p-1)*(q-1)
        d = RSA.InvertModulo(e, phi)
        optainedPlaintext.append(CCA(ciphertext, n, e, d, r))
    selfCheck(optainedPlaintext, actualPlaintext)