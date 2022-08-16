def toBinary(a):
    l,m=[],[]
    for i in a:
        l.append(ord(i))
    for i in l:
        x = bin(i)[2:]
        while(len(x) < 8):
            x = '0' + x
        m.append(x)
    return m

def calcParity(data):
    parity = [0]*8
    data_bin = toBinary(data)
    for i in data_bin:
        for j in range(8):
            if (i[j] == '1'):
                parity[j] += 1

    for i in range(8):
        if (parity[i]%2 == 0):
            parity[i] = 0
        else:
            parity[i] = 1
    
    s = str(int(''.join(str(x) for x in parity), 2))
    return s

# Returns 1 if parities are equal, 0 instead
def compareParity(parCalc, parRecv):
    if (int(parCalc) != int(parRecv)):
        return 0
    return 1