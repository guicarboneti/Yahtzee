import os

def makeBet(data, betNames, chips):
    os.system("clear")
    price = int(data[5]) + 1
    if (price > chips):
        return False
    print("Deseja fazer a seguinte aposta? (y/n)")
    print("Aposta: " + betNames[int(data[4])])
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