from numpy import true_divide


def toBinary(a):
    m = ''.join(format(ord(x), 'b') for x in a)
    return m

def calcParity(data):
    data_by = toBinary(data)


    return parity

# def compareParity(par1, par2):