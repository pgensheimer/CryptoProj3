import sys
import binascii as ba
from Crypto.Cipher import AES
from Crypto.Util import strxor
import random
from reuseFunc import readInputs
def main():
    kname, iname, oname, vname = readInputs(sys.argv[1:])
   

    blocksize = 16
    l = []
    isIV = 0
    if vname != '':
        vfile = open(vname, 'r')
        isIV = 1
    kfile = open(kname, 'r')
    ifile = open(iname, 'r')
    ofile = open(oname, 'wb')

    message = ifile.read()
    message = message.rstrip()

    key = kfile.read()
    key = key.rstrip()
    #print("key is " + str(key))
    ciphertext =''
    if isIV == 0:
        ran = random.randrange(10**80)
        myhex = "%64x" %ran
        myhex = myhex[:16]
    else:
        myhex = vfile.read()
        myhex = myhex.rstrip()
        myhex = myhex[:16]
    myhex = b'0000000000000000000000'
    #ciphertext += myhex
    #print("myhex prebytes is " + str(myhex))
    myhex = bytes(myhex, 'utf-8')
    ciphertext = b''.join([myhex])
    #print("myhex is " + str(myhex))

   
    #print("Unpadded message is " + message)
    padded = pad(message)

    #print("Padded message is " + padded.decode('utf-8'))
    #print("hex mesage " + str(ba.hexlify(padded)))
    for i in range(len(padded)):
        if(i%blocksize == blocksize-1 and i != 0):
            #print(padded[i-blocksize+1:i+1])
            l.append(padded[i-blocksize+1:i+1])
    
    #for i in range(len(l)):
        #print("hex is " + str((l[i])))
    
    #print("l is " + str(ba.hexlify(l[0]))) 
    #print()
    #print(ciphertext)
    #l[0] = bytearray()
    #z = bytearray()
    #z.extend(l[0].encode())
    #print("l 0 is  encoded z " + str(z))
    #c = strxor.strxor(str(myhex), str(l[0]))
    #print("myhex is " + str(myhex))
    #print("l0 is " + str(l[0]))
    #print("length myhex is " + str(len(myhex)))
    #print("length l0 is " + str(len(l[0])))
    c = strxor.strxor(myhex, (l[0]))
    #print(c)
    #h = strxor.strxor(myhex, c)
    #print("h is " +str((h)))
    #c = xor(myhex, (l[0]))
    #print("C is " +str(ba.hexlify(c)))
    
    cipher = encrypt(key, c)
    #print("cipher is " + str(cipher))
    #print("cipher len is " + str(len(cipher)))
    #cipher = str(cipher)
    ciphertext = createCipher(ciphertext, (cipher))
    #print(ciphertext)
    for i in range(1,len(l)):
        #print("xor of " + str(cipher) + " and " + str(l[i]))
        c = strxor.strxor(cipher,(l[i]))
        #test = str(c.decode('utf-8'))
        #print("test", test)
        #print("Xor res is " + str(c))
        cipher = encrypt(key, c)
        #print("cipher is " + str(cipher))
        ciphertext = createCipher(ciphertext, (cipher))

    #print(ciphertext)
    
    ofile.write((ciphertext))

def pad(message):
    
    padamount = 16 - len(message) % 16
    padbyte = chr(padamount)
    padded = (message + padbyte * padamount).encode('utf-8')
    return padded


def encrypt(key, message):
    cipher = AES.AESCipher(key[:32], AES.MODE_ECB)
    ciphertext = cipher.encrypt(message)
    return ciphertext
    #return ba.hexlify(bytearray(ciphertext)).decode('utf-8')

def createCipher(ciphertext, message):
    ciphertext = b''.join([ciphertext,message]);
    return ciphertext

main()
