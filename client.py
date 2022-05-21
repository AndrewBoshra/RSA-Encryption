import socket
import random
from threading import Thread
from datetime import datetime
from attr import Attribute
from colorama import Fore, init, Back
import RSA
import json
import jsonutils

# init colors
init()

# set the available colors
colors = [Fore.BLUE, Fore.CYAN, Fore.GREEN, Fore.LIGHTBLACK_EX,
          Fore.LIGHTBLUE_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTGREEN_EX,
          Fore.LIGHTMAGENTA_EX, Fore.LIGHTRED_EX, Fore.LIGHTWHITE_EX,
          Fore.LIGHTYELLOW_EX, Fore.MAGENTA, Fore.RED, Fore.WHITE, Fore.YELLOW
          ]

# choose a random color for the client
client_color = random.choice(colors)

# server's IP address
# if the server is not on this machine,
# put the private (network) IP address (e.g 192.168.1.2)
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5002  # server's port

# initialize TCP socket
s = socket.socket()
print(f"[*] Connecting to {SERVER_HOST}:{SERVER_PORT}...")
# connect to the server
s.connect((SERVER_HOST, SERVER_PORT))
print("[+] Connected.")

# prompt the client for a name
name = input("Enter your name: ")

def getInput(msg,onErrorMsg,validator):
    inp=input(msg)
    while not validator(inp):
        inp=input(onErrorMsg)
    return inp

def yesNoQuestion(msg):
    def validateYesNo(inp:str):
        return inp.lower()=='n' or inp.lower()=='y'
    answer=getInput(msg+" y/n","Invalid choice : "+msg,validateYesNo)
    return answer.lower()=='y'




print('There are two modes 1-> all keys auto generated, mode 2 choose p, q, e or just all')
mode = -1
privateMod = 23
privateExp = 7
while not mode==1 and not mode==2:
    modeStr=input('Please Enter a mode of Operation (1 or 2): ')
    if modeStr.isnumeric():
        mode = int(modeStr)
    
if mode == 1:
    print('======================= Mode 1 ========================')
    privateMod, privateExp, randomE = RSA.generateKeys()
    publicKey = {
        "name": name,
        "publicmod": privateMod,
        "publicexp": randomE
    }
    jsonutils.writeJson(publicKey, 'PublicKeys.json')
elif mode==2:
    while True:
        p=1 ; q=1 ; e=1
        print('======================= Mode 2 ========================')
        if yesNoQuestion("Would you like to enter q?"):
            q=int(getInput("Please Enter q: ","q must be prime, please enter a valid q:",RSA.isPrime))
        else:
            q=RSA.generatePrime()
        print(f"q={q}")
        if yesNoQuestion("Would you like to enter p?"):
            p=int(getInput("Please Enter p: ","p must be a prime number, please enter a valid p:  ",RSA.isPrime))
        else:
            p=RSA.generatePrime()
        print(f"p={p}")
        
        n=p*q
        phi=(p-1)*(q-1)
        
        print(f"phi={phi}")
        if p>=phi and q>=phi:
            # no valid e
            print("invalid combination")
            continue            
        
        elif yesNoQuestion("Would you like to enter e?"):
            def validateExp(e:str):
                if not e.isnumeric():
                    return False
                e=int(e)
                return e>1 and e<phi and RSA.GCD(e,phi)==1
            e=int(getInput(f"Please Enter e: ","Invalid e : e must be coprime with phi={phi} and less than it e=",validateExp))
        else:
            #has not included 2 so that if p=3 and q=5 --> phi=8 so we cant choose e=2
            e=RSA.generatePrime(3,phi)
        print(f"e={e}")
        break
    privateMod=n
    privateExp=RSA.InvertModulo(e,phi)
    randomE=e

print(privateMod, privateExp)
recvName = input('Enter the receiver name: ')
publicMod = 11
publicExp = 3

def listen_for_messages():
    while True:
        data = s.recv(1024).decode()
        data = json.loads(data)
        ciphertextArray = data.get("message")
        senderName = data.get("sendername")
        if (data.get("ignore") and data.get("receiverName") == name):
            message = []
            for msg in ciphertextArray:
                message.append(RSA.getPlaintext(msg, privateMod, privateExp))
            date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            data = json.dumps({"header": f"{client_color}[{date_now}] {name}: ",
                      "message": message, "footer": f"{Fore.RESET}",
                      "sendername": name, "ignore": False, "hacker": True, "receiverName": "hacker"})
            s.send(data.encode())
            
        elif (senderName != name and not(data.get("hacker")) and data.get("receiverName") == "everyone"):
            plaintextArray = ''
            for ciphertext in ciphertextArray:
                plaintextArray += RSA.getPlaintext(ciphertext, privateMod, privateExp)
            print('\n' + data.get("header") + plaintextArray + data.get("footer"))


# make a thread that listens for messages to this client & print them
t = Thread(target=listen_for_messages)
# make the thread daemon so it ends whenever the main thread ends
t.daemon = True
# start the thread
t.start()

while True:
    # input message we want to send to the server
    message = input()
    # a way to exit the program
    if message.lower() == 'q':
        break
    publicMod, publicExp = jsonutils.getUserPU(recvName)
    # encrypt message
    msgArray = RSA.splitString(message)
    ciphertextArray = []
    for msg in msgArray:
        ciphertextArray.append(RSA.getCiphertext(msg, publicMod, publicExp))
    # add the datetime, name & the color of the sender
    date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # finally, send the message
    data = json.dumps({"header": f"{client_color}[{date_now}] {name}: ",
                      "message": ciphertextArray, "footer": f"{Fore.RESET}",
                      "sendername": name, "ignore": False, "hacker": False, "receiverName": "everyone"})
    s.send(data.encode())
    print(f"{client_color}[{date_now}] {name}: {message}{Fore.RESET}")
# close the socket
s.close()
