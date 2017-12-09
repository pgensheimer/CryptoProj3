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
    except getopt.GetoptError:
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-k", "--kfile"):
            kname = arg
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

def modexp(mess, e, n):
    count = 1
    while e:
        if e & 1:
            count = count * mess % n
        e >>= 1
        mess = mess * mess % n
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
    o = open(oname, 'r')

    numbits = int(k.readline().rstrip())
   # print(numbits)
    n = int(k.readline().rstrip())
    #print(n)
    e = int(k.readline().rstrip())
   # print(e)
    message = i.read().rstrip()
    signat = o.read().rstrip()
    #print("right before hashing\n")
   # print("message is "+message)
    message = hashfunc(message)
    paddedmessage = paddingFunc(message, int(numbits/2))
   # print("padfunc is " +str(paddedmessage))
    if(paddedmessage == 1):
        quit(1)
    else:
        int_mess = int.from_bytes(paddedmessage, byteorder='big')
   #     print("int mess:", int_mess)
        #print("int mess % n:", int_mess % n)
        Exp = modexp(int_mess, e, n)
  #  print("Exp is "+ str(Exp))
 #   print("sig is "+ str(signat))
    
    if(str(Exp) == signat):
        print("True")
    else:
        print("False")
        
    #o.write(str(Exp))
    

main()
