#this file creates a valid RSA public key / private key pair and stores them in files
import hashlib
import sys, getopt
import random
from math import gcd
from paddingfunc import paddingFunc

def readInputs(commandl):
    pname = ''
    sname = ''
    cname = ''
    numbits =0
    try:
        opts, args = getopt.getopt(commandl, "p:s:n:c:", ["cfile=","pfile=", "sfile =", "numbits="])
    except getopt.GetoptError:
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-p", "--pfile"):
            pname = arg
        elif opt in ("-s", "--sfile"):
            sname = arg
        elif opt in ("-c", "--cfile"):
            cname = arg
        elif opt in ("-n", "--numbits"):
            numbits = arg
    if(pname == ''):
        print("you have to include a public key file")
        exit(1)
    if(sname == ''):
        print("you have to include a secret key file")
        exit(1)
    if(numbits == 0):
        print("you have to include a keylength")
        exit(1)
    
    return pname, sname, numbits, cname

#this is the function that implement miller rabin prime testing

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

def isPrime(bits, k):
    
    #k is the correctness factor
    if bits % 2 == 0:
        return 0
    
    #try to divide n-1 by 2 a bunch of times
    d =bits-1
    count = 0
    
    while True:
        quotient, remainder = divmod(d,2)
        
        if remainder ==1:
            break
        
        count += 1
        d = quotient
    
    for i in range (k):
        rand = random.randrange(2,bits)
        if compositeTest(bits, d, count,rand):
                return 0
    
    return 1

#this function tests for composites
def compositeTest(bits, d, count, rand):
    if pow(rand, d , bits)==1:
        return 0
    
    for i in range(count):
        if pow(rand, 2**i * d, bits)== bits-1:
            return 0
    
    return 1

#this is the function that gets random bits and then sends it to isPrime to see 
def makePrime(numbits):
    checkprime = 0
    k = 10
    idk = "1"
    #print("numbits is "+ str(numbits))
    numbits = numbits -2
    while(checkprime == 0):
        bits = random.getrandbits(numbits)
        #print("bits as int is")
        #print(bits)
        bits = '{0:b}'.format(bits)
        while(len(bits) != numbits):
            bits = "0"+bits
        #print("bits as bin is ")
        #print(bits)
        bits = idk+bits+idk
        #print(bits)
        #trying to set last bit to 1, but im bad
       # bits = bitarray(bits)
       # print(bits)
       # bits = str(bits)+ str("1")
        bits = int(bits,2)
        checkprime = isPrime(bits, k)

    #print('bits is ' + str(bits))
    return bits

def mulinv(e,N):
    g,x, q = egcd(e,N)
    if g!=1:
        print("modular inverse failure")
        exit(1)
    else:
        return x % N

def egcd(a,b):
    if a == 0:
        return (b,0,1)
    else:
        g, y, x = egcd(b%a,a)
        return (g, x-(b//a)* y,y)

def main():
    pname, sname, numbits, cname = readInputs(sys.argv[1:])

    #print("in rsa keygen")
    #print('numbits is "', numbits)
    
    pfile = open(pname,'w')
    sfile = open(sname,'w')
#    print(sfile)
    numbits = int(numbits)
    #numbits = numbits+2
    #print("numbits is" + str(numbits))
    p = makePrime(int(numbits/2))
    #print("numbits is" + str(numbits))
    
    q = makePrime(int(numbits/2))
    smalln = p*q

    #print("smalln is " + str(smalln))

    #print("length of small n is" + str(len(str(smalln))))
    N = (p-1) * (q-1)
    e = 0
    if gcd(N,3) ==1:
        e = 3
    elif gcd(N,5) ==1:
        e = 5
    elif gcd(N,7) ==1:
        e = 7
    elif gcd(N, 11) ==1:
        e =11
    elif gcd(N, 13) ==1:
        e=13
    else:
        print("unlucky N value")
    #need to compute e*d = 1 % N
    # d = e^-1 mod N
    ##d = pow(e, -1)
    ##d = d % N
    #f = (d * e) % N
    d = mulinv(e, N)
    numbits = str(numbits)
    #print("f is " + str(f))

    #print("p is " +str(p))
    #print("q is " +str(q))
    #print("e is " +str(e))
    #print("d is " +str(d))
    #print("N is " +str(N))

    pfile.write(numbits+"\n")
    pfile.write(str(smalln)+"\n")
    pfile.write(str(e)+"\n")
    sfile.write(numbits+"\n")
    sfile.write(str(smalln)+"\n")
    sfile.write(str(d)+"\n")
    pfile.close()
    sfile.close()
    
    pfile = open(pname,'r')

#    pubcontents = pfile.read()
#    print("1")
    signedpubfile = pname + "-casig"
#    print(signedpubfile)
    pubsigfile = open(signedpubfile, 'w')
 #   print(pubsigfile)
#    print("2")
    if(cname != ""):
        kfile = open(cname, 'r')
    else:
        kfile = open(sname, 'r')

    numbits = int(kfile.readline().rstrip())
    #print(numbits)
    n = int(kfile.readline().rstrip())
   # print(n)
    e = int(kfile.readline().rstrip())
    #print(e)
    message = pfile.read().rstrip()
#    print("3")
   # print("message is " + message)
    message = hashfunc(message)
    paddedmessage = paddingFunc(message, int(numbits/2))
  #  print("padmess is "+ str(paddedmessage))
    if(paddedmessage == 1):
        quit(1)
    else:
        int_mess = int.from_bytes(paddedmessage, byteorder='big')
 #       print("int mess is", int_mess)
        Exp = modexp(int_mess, e, n)
#    print("4")
#    print("exp is "+str(Exp))
    pubsigfile.write(str(Exp))
#    print("5")    
main()
