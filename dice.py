from random import randint
import os
import time

def dice():
    dices = {
        0: False,
        1: False,
        2: False,
        3: False,
        4: False
    }

    diceValues = [0, 0, 0, 0, 0]

    for rounds in range(3):
        print("==== NOVA RODADA ====")
        for dice in range(5):
            if not dices[dice]:
                diceValues[dice] = randint(1, 6)
            print("Dado ", dice + 1, ": ", diceValues[dice])
            time.sleep(2)

        if rounds != 2:
            for dice in range(5):
                print("Travar dado ", dice + 1, "? (y/)")
                decision = input()
                if decision == "y":
                    dices[dice] = True

        time.sleep(2)
        os.system("clear")

    print("==== RESULTADOS ====")
    for i in range(5):
        print("Dado ", i + 1, ": ",diceValues[i])

    print("Combinação obtida é:")
    count = {}

    for i in diceValues:
        count[i] = diceValues.count(i)

    countValues = list(count.values())

    if countValues.count(2) == 1:
        print("Par")
        returnVal = 0

    if countValues.count(3) == 1 and countValues.count(2) != 1:
        print("Trio")
        returnVal = 1

    if countValues.count(2) == 2:
        print("2 Pares")
        returnVal = 2

    if countValues.count(3) == 1 and countValues.count(2) == 1:
        print("Full House")
        returnVal = 3

    if not 2 in countValues and not 3 in countValues and not 4 in countValues and not 5 in countValues and 1 in diceValues:
        print("Seq. Baixa")
        returnVal = 4

    if not 2 in countValues and not 3 in countValues and not 4 in countValues and not 5 in countValues and 6 in diceValues:
        print("Seq. Alta")
        returnVal = 5

    if countValues.count(4) == 1:
        print("Quadra")
        returnVal = 6

    if countValues.count(5) == 1:
        print("General")
        returnVal = 7

    time.sleep(2)
    return returnVal