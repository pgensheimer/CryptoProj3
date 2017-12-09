<<<<<<< HEAD
import math
import binascii as ba
import sys, getopt
from paddingfunc import paddingFunc

def readInputs(arguements):
    kname, mname, sname = '', '', ''
    try:
        opts, args = getopt.getopt(arguements, "k:m:s", ["kfile=", "mfile=", "sfile="])
=======
#this file encrypts an integer using RSA

import math
import binascii as ba
import sys, getopt
import hashlib
from paddingfunc import paddingFunc

def readInputs(commandl):
    kname = ''
    iname = ''
    oname = ""
    #print("aqui")
    try:
        opts, args = getopt.getopt(commandl, "k:m:s:", ["kfile=", "mfile =", "sfile="])
>>>>>>> origin/Parkerbranch
    except getopt.GetoptError:
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-k", "--kfile"):
            kname = arg
<<<<<<< HEAD
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
=======
        elif opt in ("-m", "--mfile"):
            iname = arg
        elif opt in ("-s", "--sfile"):
            oname = arg
    #print("222")
    if(oname == ''):
        print("you have to include a signature file")
        exit(1)
    if(iname == ''):
        print("you have to include a message file")
        exit(1)
    if(kname == ''):
        print("must include fiel with RSA key in correct format")
        exit(1)
    #print(oname + " and " + kname + "and " + iname)
    return kname, iname, oname

>>>>>>> origin/Parkerbranch
def modexp(mess, e, n):
    count = 1
    while e:
        if e & 1:
            count = count * mess % n
        e >>= 1
        mess = mess * mess % n
<<<<<<< HEAD
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
=======
    #print(count)
    return count
def hashfunc(message):
    m = hashlib.sha256()
    message = message.encode('utf-8')
    m.update(message)
    ret = m.digest()
    #ret = ret.decode('utf-8')
    return ret
def main():
    #print("?????????")
    kname, iname, oname = readInputs(sys.argv[1:])
    #print("n main")
    k = open(kname, 'r')
    i = open(iname, 'r')
    o = open(oname, 'w')

    numbits = int(k.readline().rstrip())
    n = int(k.readline().rstrip())
    e = int(k.readline().rstrip())
    message = i.read().rstrip()
    #print("right before hashing\n")
    
    message = hashfunc(message)
    paddedmessage = paddingFunc(message, int(numbits/2))
    #print(paddedmessage)
>>>>>>> origin/Parkerbranch
    if(paddedmessage == 1):
        quit(1)
    else:
        int_mess = int.from_bytes(paddedmessage, byteorder='big')
<<<<<<< HEAD
        Exp = modexp(int_mess, e, n)

    s.write(str(Exp))
=======
        #print("int mess:", int_mess)
        #print("int mess % n:", int_mess % n)
        Exp = modexp(int_mess, e, n)

    o.write(str(Exp))
    
>>>>>>> origin/Parkerbranch

main()
