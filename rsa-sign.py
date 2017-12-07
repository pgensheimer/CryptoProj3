import math
import binascii as ba
import sys, getopt
from paddingfunc import paddingFunc

def readInputs(arguements):
    kname, mname, sname = '', '', ''
    try:
        opts, args = getopt.getopt(arguements, "k:m:s", ["kfile=", "mfile=", "sfile="])
    except getopt.GetoptError:
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-k", "--kfile"):
            kname = arg
        elif opt in ("-m","--mfile"):
            mname = arg
        elif opt in ("-s","--sfile"):
            sname = arg
    if(kname == ''):
        print("no key file")
        exit(1)
    if(mname == ''):
        print("no message file")
        exit(1)
    if(sname == ''):
        print("no signature file")
        exit(1)

    return kname, iname, oname
def modexp(mess, e, n):
    count = 1
    while e:
        if e & 1:
            count = count * mess % n
        e >>= 1
        mess = mess * mess % n
        return count

def main():
    kname, mname, sname = readInputs(sys.argv[1:])

    k = open(kname, 'r')
    m = open(mname, 'r')
    s = open(sname, 'w')
    
    numbits = int(k.readline().rstrip())
    n = int(k.readline().rstrip())
    e = int(k.readline().rstrip())
    message = m.read().rstrip()
    #question is do we hash before or after padding?
    #add library for hashing with sha256
    paddedmessage = paddingFunc(message, int(numbits/2))
    if(paddedmessage == 1):
        quit(1)
    else:
        int_mess = int.from_bytes(paddedmessage, byteorder='big')
        Exp = modexp(int_mess, e, n)

    s.write(str(Exp))

main()
