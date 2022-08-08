import socket
import sys
import os

# Types
BATON = '1'
BET = '2'
RESULT = '3'
EXIT = '4'
PLAY = '5'
END = '6'
STARTMARKER = '9'

# System variables
IP = "127.0.0.1"
PORT = 5001

NAME = "B"
ADDREC = 5000
ADDSEND = 5002

# Controls relay baton
relayBaton = False

# Configures DGRAM socket
mySocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
mySocket.bind((IP, PORT))

# Game variables
chips = {
    "A": 20,
    "B": 20,
    "C": 20,
    "D": 20
}
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

# Game function
def throwDices():
    print("throw dices")

def updateValues():
    print("update values")

def makeBet(data):
    print("Deseja fazer a seguinte aposta? (y/n)")
    print("Aposta: " + betNames[int(data[4])])
    price = int(data[5]) + 1
    print("Custo: " + str(price))

    awaitChoice = True
    makeChoice = False

    while awaitChoice:
        choice = input()
        if choice == "y" or choice == "Y":
            print("Yes")
            awaitChoice = False
            makeChoice = True
        elif choice == "n" or choice == "N":
            print("No")
            awaitChoice = False
        else:
            print("Não entendi, escolha entre y/n")

    return makeChoice
    

while True:
    if relayBaton:
        os.system("clear")

        # Makes choice
        choice = chooseBet()
        os.system("clear")

        # Sends to next
        marker = str.encode(STARTMARKER)
        msgType = str.encode(BET)
        size = b'3'
        data = str.encode(NAME + str(choice)+ '1')
        parity = b'0'
        message = marker + msgType + size + data + parity
        mySocket.sendto(message, (IP, ADDSEND))

        # Awaits return
        awaitBet = True
        while awaitBet:
            data, addr = mySocket.recvfrom(1024)
            if addr[1] == ADDREC:
                data = data.decode("utf-8")
                if data[0] == STARTMARKER and data[1] == BET:
                    awaitBet = False

        # Decides if it bets or passes to gambler
        if data[3] == NAME:
            # Plays game
            throwDices()
        else:
            # Sends message to gambler
            marker = str.encode(STARTMARKER)
            msgType = str.encode(PLAY)
            size = b'3'
            data = str.encode(data[3] + data[4] + data[5])
            parity = b'0'
            message = marker + msgType + size + data + parity
            mySocket.sendto(message, (IP, ADDSEND))

            # Awaits return
            while awaitBet:
                data, addr = mySocket.recvfrom(1024)
                if addr[1] == ADDREC:
                    data = data.decode("utf-8")
                    if data[0] == STARTMARKER and data[1] == RESULT:
                        awaitBet = False

        # End of round    
        #updateValues()
        #marker = str.encode(STARTMARKER)
        #msgType = str.encode(END)
        #size = b'0'
        #parity = b'0'
        #message = marker + msgType + size + parity
        #mySocket.sendto(message, (IP, ADDSEND))

        # Sends baton
        marker = str.encode(STARTMARKER)
        msgType = str.encode(BATON)
        size = b'0'
        parity = b'0'
        message = marker + msgType + size + parity

        mySocket.sendto(message, (IP, ADDSEND))
        relayBaton = False

    else:
        data, addr = mySocket.recvfrom(1024)
        if addr[1] == ADDREC:
            data = data.decode("utf-8")
            if data[0] == STARTMARKER:

                # Message about new bet
                if data[1] == BET:
                    betDecision = makeBet(data)
                    if betDecision:
                        marker = str.encode(STARTMARKER)
                        msgType = str.encode(BET)
                        size = b'3'
                        newValue = int(data[5]) + 1
                        data = str.encode(NAME + data[4] + str(newValue))
                        parity = b'0'
                        message = marker + msgType + size + data + parity
                        mySocket.sendto(message, (IP, ADDSEND))

                    else:
                        mySocket.sendto(str.encode(data), (IP, ADDSEND))

                # Message to play game
                elif data[1] == PLAY:
                    throwDices()
                    updateValues()

                elif data[1] == RESULT:
                    updateValues()

                elif data[1] == BATON:
                    relayBaton = True

                elif data[1] == EXIT:
                    print("EXIT")