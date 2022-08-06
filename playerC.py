import socket
import sys
import os

# System variables
IP = "127.0.0.1"
PORT = 5002

NAME = "C"
ADDREC = 5001
ADDSEND = 5003

# Controls relay baton
relayBaton = True

# Configures DGRAM socket
mySocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
mySocket.bind((IP, PORT))

# Game variables
chips = 20
currentGambler = ""
betNames = ["Par", "Trio", "2 Pares", "Full House", "Seq. Baixa", "Seq. Alta", "Quadra", "General"]
betValues = [2, 3, 4, 5, 7, 7, 10, 15]

# Function that shows all possible bets and gets choice
def chooseBet():
    print("Escolha uma das seguintes apostas (digite o número):")
    index = 1
    for bet in betNames:
        print(index, "- ", bet)
        index+=1

    choice = input()
    return (int(choice) - 1)

while True:
    if relayBaton:
        os("clear")

        # Makes choice
        choice = chooseBet()
        os("clear")

        # Sends to next
        marker = b'9'
        msgType = b'2'
        size = b'2'
        data = str.encode(NAME + str(choice))
        parity = b'0'
        message = marker + msgType + size + data + parity
        mySocket.sendto(message, (IP, ADDSEND))

        # Awaits return

        # Decides if it bets or passes to gambler

        # Sends baton
        mySocket.sendto(b"bastao", (IP, ADDSEND))
        relayBaton = False
    else:
        data, addr = mySocket.recvfrom(1024)
        if addr[1] == ADDREC:
            data = data.decode("utf-8")