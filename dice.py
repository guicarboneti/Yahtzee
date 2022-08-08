from random import randint
import os
import time

dices = {
    0: False,
    1: False,
    2: False,
    3: False,
    4: False
}

diceValues = [0, 0, 0, 0, 0]

for rounds in range(3):
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

for i in range(5):
    print("Dado ", i + 1, ": ",diceValues[i])