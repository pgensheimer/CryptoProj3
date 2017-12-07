import sys
import binascii as ba
from Crypto.Cipher import AES
from Crypto.Util import strxor
import random
from reuseFunc import readInputs
def main():
    kname, mname, tname, vname = readInputs(sys.argv[1:])
   

    #print("here")
    blocksize = 16
    l = []
    isIV = 0
    if vname != '':
        vfile = open(vname, 'r')
        isIV = 1
    kfile = open(kname, 'r')
    mfile = open(mname, 'r')
    tfile = open(tname, 'wb')

    message = mfile.read()
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
    myhex = "000000000000000000000000000"
    myhex = myhex[:16]
    
    #ciphertext += myhex
    #print("myhex prebytes is " + str(myhex))
    
    myhex = bytes(myhex, 'utf-8')
    ciphertext = b''.join([myhex])
    
    #print("myhex is " + str(myhex))

   
    #print("Unpadded message is " + message)
    
    messagelength = len(message) %16
    if messagelength !=0:
        messagelength = int(len(message) / 16) +1
    else:
        messagelength = len(message) / 16

    #print("mlenght is " + str(messagelength))
    mlength = str(messagelength)
    
    while len(mlength) < 16:
        mlength = "0" + mlength
    #print("mlenght2 is " + mlength)
    message = mlength + message
    padded = pad(message)
    #NEED To ADD LENGTH TO START OF MESSAGE
    
    
    #print("message is "+ str(message))
    for i in range(len(padded)):
        if(i%blocksize == blocksize-1 and i != 0):
            l.append(padded[i-blocksize+1:i+1])
    #print("numblocks is " +str(i))
    
    #print("l(i) is "+ str(l[1])) 
    c = strxor.strxor(myhex, (l[0]))
    
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
    ciphertext = ciphertext[-16:] 

#    ciphertext = str(ciphertext)
    
  //  print("ciphertext is "+ str(ciphertext))
    
    tfile.write((ciphertext))

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
