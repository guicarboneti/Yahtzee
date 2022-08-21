import socket
import sys
import os
import signal
from dice import *
from makeBet import *
from chipsTable import *
from parity import *

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

# Function to exit game
def exit_game(paridade=False):
    marker = STARTMARKER
    msgType = EXIT
    size = '0'
    parity = '0'
    message = str.encode(marker + msgType + size + parity)
    mySocket.sendto(message, (IP, ADDSEND))
    drawTable(chips)
    if paridade == True:
        print("Paridade errada")
    print("Saindo do jogo...")
    sys.exit(0)

# Handler function for exit case
def signal_handler(sig, frame):
    exit_game()

signal.signal(signal.SIGINT, signal_handler)

# Function that returns the data field over received data
def getRecvData(data):
    recv_size = data[2]
    if recv_size == '0':
        data_field = ''
    elif recv_size == '1':
        data_field = data[3]
    elif recv_size == '2':
        data_field = data[3] + data[4]
    elif recv_size == '3':
        data_field = data[3] + data[4] + data[5]

    return data_field

# Function that shows all possible bets and gets choice
def chooseBet():
    os.system("clear")
    print("Escolha uma das seguintes apostas (digite o número):")
    index = 1
    for bet in betNames:
        print(index, "- ", bet)
        index+=1

    choice = input()
    return (int(choice) - 1)

# Game function
def throwDices(data):
    gameResult = dice(betNames[int(data[4])])
    if gameResult == -1:
        return signal_handler

    if gameResult == int(data[4]):
        print("VOCÊ VENCEU A APOSTA")
        return betValues[gameResult] - int(data[5])
    else:
        print("VOCÊ PERDEU A APOSTA")
        return - int(data[5])

def updateValues(name, value):
    chips[name] = chips[name] + value
    if (chips[name] <= 0):
        exit_game()

drawTable(chips)
while True:
    if relayBaton:

        # Makes choice
        choice = chooseBet()
        os.system("clear")
        print("Esperando adversários...")

        # Sends to next
        marker = STARTMARKER
        msgType = BET
        size = '3'
        data = NAME + str(choice) + '1'
        parity = calcParity(data)
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
                if data[0] == STARTMARKER and data[1] == EXIT:
                    signal_handler(0,0)

        # Decides if it bets or passes to gambler
        if data[3] == NAME:
            # Plays game
            gameResult = throwDices(data)
            updateValues(NAME, gameResult)
            drawTable(chips)

            # End of round
            marker = STARTMARKER
            msgType = END
            size = '2' if gameResult > 0 and gameResult < 10 else '3'
            data = NAME + str(gameResult)
            parity = calcParity(data)
            message = str.encode(marker + msgType + size + data + parity)
            mySocket.sendto(message, (IP, ADDSEND))

        else:
            # Sends message to gambler
            marker = STARTMARKER
            msgType = PLAY
            size = '3'
            # 3: name, 4: bet made, 5: cost
            data = data[3] + data[4] + data[5]
            parity = calcParity(data)
            message = str.encode(marker + msgType + size + data + parity)
            mySocket.sendto(message, (IP, ADDSEND))
            drawTable(chips)

            # Awaits return
            awaitRet = True
            while awaitRet:
                data, addr = mySocket.recvfrom(1024)
                if addr[1] == ADDREC:
                    data = data.decode("utf-8")
                    if data[0] == STARTMARKER and data[1] == RESULT:
                        awaitRet = False
                    if data[0] == STARTMARKER and data[1] == EXIT:
                        signal_handler(0,0)

            # From size, detect if the number (starting on data[4]) has 1 or 2 digits
            # Then, call updateValues()
            if data[2] == '2':
                gameResult = int(data[4])
            elif data[2] == '3':
                gameResult = int(data[4] + data[5])
            updateValues(data[3], gameResult)
            drawTable(chips)

            # End of round
            marker = STARTMARKER
            msgType = END
            size = '2' if gameResult > 0 and gameResult < 10 else '3'
            data = data[3] + str(gameResult)
            parity = calcParity(data)
            message = str.encode(marker + msgType + size + data + parity)
            mySocket.sendto(message, (IP, ADDSEND))

        # Awaits other players be up-to-date
        awaitEnd = True
        while awaitEnd:
            data, addr = mySocket.recvfrom(1024)
            if addr[1] == ADDREC:
                data = data.decode("utf-8")
                if data[0] == STARTMARKER and data[1] == END:
                    awaitEnd = False
                if data[0] == STARTMARKER and data[1] == EXIT:
                    signal_handler(0,0)

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
            if data[0] == STARTMARKER and compareParity(calcParity(getRecvData(data)), int(data[(int(data[2])+3):len(data)])):

                # Message about new bet offer
                if data[1] == BET:
                    betDecision = makeBet(data, betNames, chips[NAME])
                    if betDecision:
                        marker = STARTMARKER
                        msgType = BET
                        size = '3'
                        newValue = int(data[5]) + 1
                        data = NAME + data[4] + str(newValue)
                        parity = calcParity(data)
                        message = str.encode(marker + msgType + size + data + parity)
                        mySocket.sendto(message, (IP, ADDSEND))
                        drawTable(chips)

                    else:
                        drawTable(chips)
                        mySocket.sendto(str.encode(data), (IP, ADDSEND))

                # Message to play game
                elif data[1] == PLAY:
                    if data[3] == NAME:
                        gameResult = throwDices(data)

                        # Send results to relay baton holder
                        marker = STARTMARKER
                        msgType = RESULT
                        size = '2' if gameResult > 0 and gameResult < 10 else '3'
                        data = NAME + str(gameResult)
                        parity = calcParity(data)
                        message = str.encode(marker + msgType + size + data + parity)
                        mySocket.sendto(message, (IP, ADDSEND))
                        drawTable(chips)

                    else:
                        mySocket.sendto(str.encode(data), (IP, ADDSEND))

                # Message with round results
                # Send it to the next player until it reaches relay baton holder
                elif data[1] == RESULT:
                    mySocket.sendto(str.encode(data), (IP, ADDSEND))

                # Message about end of round
                # Update values and send it to the next player until it reaches relay baton holder
                elif data[1] == END:
                    # From size, detect if the number (starting on data[4]) has 1 or 2 digits
                    # Then, call updateValues()
                    gameResult = int(data[4]) if int(data[2]) == 2 else int(data[4] + data[5])
                    updateValues(data[3], gameResult)
                    drawTable(chips)
                    mySocket.sendto(str.encode(data), (IP, ADDSEND))

                # Receive relay baton
                elif data[1] == BATON:
                    relayBaton = True

                # Message to exit
                # Sends message to next player and exits
                elif data[1] == EXIT:
                    exit_game()

            else:
                exit_game(True)
