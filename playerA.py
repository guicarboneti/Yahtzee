import socket
import sys
import os
from dice import *

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
PORT = 5000

NAME = "A"
ADDREC = 5003
ADDSEND = 5001

# Controls relay baton
relayBaton = True

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
    os.system("clear")
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

    os.system("clear")
    return makeChoice
    

while True:
    if relayBaton:
        os.system("clear")

        # Makes choice
        choice = chooseBet()
        os.system("clear")

        # Sends to next
        marker = STARTMARKER
        msgType = BET
        size = '3'
        data = NAME + str(choice) + '1'
        parity = '0'
        message = str.encode(marker + msgType + size + data + parity)
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
            marker = STARTMARKER
            msgType = PLAY
            size = '3'
            # 3: name, 4: bet made, 5: cost
            data = data[3] + data[4] + data[5]
            parity = '0'
            message = str.encode(marker + msgType + size + data + parity)
            mySocket.sendto(message, (IP, ADDSEND))

            # Awaits return
            while awaitBet:
                data, addr = mySocket.recvfrom(1024)
                if addr[1] == ADDREC:
                    data = data.decode("utf-8")
                    if data[0] == STARTMARKER and data[1] == RESULT:
                        awaitBet = False

        # End of round    
        updateValues()
        marker = STARTMARKER
        msgType = END
        size = '0'
        parity = '0'
        message = str.encode(marker + msgType + size + parity)
        mySocket.sendto(message, (IP, ADDSEND))

        # Awaits other players be up-to-date
        awaitEnd = True
        while awaitEnd:
            data, addr = mySocket.recvfrom(1024)
            if addr[1] == ADDREC:
                data = data.decode("utf-8")
                if data[0] == STARTMARKER and data[1] == END:
                    awaitEnd = False

        # Sends baton
        marker = STARTMARKER
        msgType = BATON
        size = '0'
        parity = '0'
        message = str.encode(marker + msgType + size + parity)

        mySocket.sendto(message, (IP, ADDSEND))
        relayBaton = False

    else:
        data, addr = mySocket.recvfrom(1024)
        if addr[1] == ADDREC:
            data = data.decode("utf-8")
            if data[0] == STARTMARKER:

                # Message about new bet offer
                if data[1] == BET:
                    betDecision = makeBet(data)
                    if betDecision:
                        marker = STARTMARKER
                        msgType = BET
                        size = '3'
                        newValue = int(data[5]) + 1
                        data = NAME + data[4] + str(newValue)
                        parity = '0'
                        message = str.encode(marker + msgType + size + data + parity)
                        mySocket.sendto(message, (IP, ADDSEND))

                    else:
                        mySocket.sendto(str.encode(data), (IP, ADDSEND))

                # Message to play game
                elif data[1] == PLAY:
                    if data[3] == NAME:
                        throwDices()

                        # Send results to relay baton holder
                        marker = STARTMARKER
                        msgType = RESULT
                        size = '0'
                        parity = '0'
                        message = str.encode(marker + msgType + size + parity)
                        mySocket.sendto(message, (IP, ADDSEND))
                    else:
                        mySocket.sendto(str.encode(data), (IP, ADDSEND))

                # Message with round results
                # Send it to the next player until it reaches relay baton holder
                elif data[1] == RESULT:
                    mySocket.sendto(str.encode(data), (IP, ADDSEND))

                # Message about end of round
                # Update values and send it to the next player until it reaches relay baton holder
                elif data[1] == END:
                    updateValues()
                    mySocket.sendto(str.encode(data), (IP, ADDSEND))

                # Receive relay baton
                elif data[1] == BATON:
                    relayBaton = True

                # Message to exit
                # Sends message to next player and exits
                elif data[1] == EXIT:
                    marker = STARTMARKER
                    msgType = EXIT
                    size = '0'
                    parity = '0'
                    message = str.encode(marker + msgType + size + parity)
                    mySocket.sendto(message, (IP, ADDSEND))
                    sys.exit(0)