import os

def drawTable(data):
    os.system("clear")
    # print("Jogadores       Fichas")
    # for player in data:
    #         print('    ', player, '           ', data[player])

    # Print the names of the columns.
    print("{:<10} {:<10}".format('PLAYER', 'CHIPS'))
 
    # print each data item.
    for key, value in data.items():
        print("{:<12} {:<10}".format(key, value))
