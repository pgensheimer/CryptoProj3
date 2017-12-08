#this file encrypts an integer using RSA

import math
import binascii as ba
import sys, getopt
from paddingfunc2 import paddingFunc

def readInputs(commandl):
    kname = ''
    iname = ''
    oname = ""
    try:
        opts, args = getopt.getopt(commandl, "k:i:o:", ["kfile=", "ifile =", "ofile="])
    except getopt.GetoptError:
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-k", "--kfile"):
            kname = arg
        elif opt in ("-i", "--ifile"):
            iname = arg
        elif opt in ("-o", "--ofile"):
            oname = arg
    if(oname == ''):
        print("you have to include an output file")
        exit(1)
    if(iname == ''):
        print("you have to include an input file")
        exit(1)
    if(kname == ''):
        print("must include fiel with RSA key in correct format")
        exit(1)
    
    return kname, iname, oname

def modexp(mess, e, n):
    count = 1
    while e:
        if e & 1:
            count = count * mess % n
        e >>= 1
        mess = mess * mess % n
    #print(count)
    return count

def main():
    kname, iname, oname = readInputs(sys.argv[1:])

    k = open(kname, 'r')
    i = open(iname, 'r')
    o = open(oname, 'w')

    numbits = int(k.readline().rstrip())
    n = int(k.readline().rstrip())
    e = int(k.readline().rstrip())
    message = i.read().rstrip()
    paddedmessage = paddingFunc(message, int(numbits/2))
    #print(paddedmessage)
    if(paddedmessage == 1):
        quit(1)
    else:
        int_mess = int.from_bytes(paddedmessage, byteorder='big')
        #print("int mess:", int_mess)
        #print("int mess % n:", int_mess % n)
        Exp = modexp(int_mess, e, n)

    o.write(str(Exp))
    

main()
