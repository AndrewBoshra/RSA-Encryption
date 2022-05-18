import socket
import random
from threading import Thread
from datetime import datetime
from colorama import Fore, init, Back
import RSA
import json

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
victumName = input("Enter your victum name: ")
print('Enter the public key of your victum in the order n then e')
publicMod = int(input('n: '))
publicExp = int(input('e: '))

r = input("Enter a rundom number r such that gcd(r, n) = 1: ")
r = RSA.ConvertToInt(r)
rInv = RSA.InvertModulo(r, publicMod)
# raise the randomly choosen integer 'r' to power 'e' in modulo 'n'
# note: the victum's public key is (e, n), gdc(r, n) = 1
r = RSA.PowMod(r, publicExp, publicMod)


while True:
    # intercept between Alice and Bob
    data = s.recv(1024).decode()
    data = json.loads(data)
    # get the mesage chunks
    header = data.get("header")
    ciphertextArray = data.get("message")
    footer = data.get("footer")
    senderName = data.get("sendername")

    if (senderName != victumName and senderName != name and not(data.get("hacker")) and data.get("receiverName") == "everyone"):
        # encrypt message
        for i in range(len(ciphertextArray)):
            intCipher = RSA.ConvertToInt(ciphertextArray[i])
            msg = RSA.ConvertToStr(RSA.PowMod(intCipher*r, 1, publicMod))
            ciphertextArray[i] = msg #RSA.getCiphertext(msg, publicMod, publicExp)
        # add the datetime, name & the color of the sender
        date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # finally, send the message
        data = json.dumps({"header": f"{client_color}[{date_now}] {name}: ",
                        "message": ciphertextArray, "footer": f"{Fore.RESET}",
                        "sendername": name, "ignore": True, "hacker": True, "receiverName": f"{victumName}"})
        s.send(data.encode())
    
    elif (senderName == victumName and data.get("hacker") and data.get("receiverName") == "hacker"):
        message = ''
        for msg in ciphertextArray:
            intMsg = RSA.PowMod(RSA.ConvertToInt(msg)*rInv, 1, publicMod)
            message += RSA.ConvertToStr(intMsg)
        print('\n' + data.get("header") + message + data.get("footer"))
    
    
