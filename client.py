import socket
import random
from threading import Thread
from datetime import datetime
from attr import Attribute
from colorama import Fore, init, Back
import re
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
print('Enter your private key in the order n then d')
privateMod = int(input('n: '))
privateExp = int(input('d: '))

print('Enter the public key of the receiver in the order n then e')
publicMod = int(input('n: '))
publicExp = int(input('e: '))


def listen_for_messages():
    while True:
        data = s.recv(1024).decode()
        data = json.loads(data)
        ciphertextArray = data.get("message")
        senderName = data.get("sendername")
        if (senderName != name):
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
    # encrypt message
    msgArray = RSA.splitString(message)
    ciphertextArray = []
    for msg in msgArray:
        ciphertextArray.append(RSA.getCiphertext(msg, publicMod, publicExp))
    # ciphertext = RSA.getCiphertext(message, publicMod, publicExp)
    # add the datetime, name & the color of the sender
    date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # finally, send the message
    data = json.dumps({"header": f"{client_color}[{date_now}] {name}: ",
                      "message": ciphertextArray, "footer": f"{Fore.RESET}", "sendername": name})
    s.send(data.encode())
    print(f"{client_color}[{date_now}] {name}: {message}{Fore.RESET}")
# close the socket
s.close()
