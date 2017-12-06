import sys
import binascii as ba
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Util import strxor
import random
import multiprocessing as mp
from reuseFunc import readInputs
def main():

    kname, iname, oname, vname = readInputs(sys.argv[1:])

    blocksize = 8
    l = []

    isIV = 0
    if(vname != ''):
        vfile = open(vname, 'r')
        isIV = 1
    kfile = open(kname, 'r')
    ifile = open(iname, 'r')
    ofile = open(oname, 'w')

    message = ifile.read()
    message = message[:-1]
    #message = message.encode('utf-8')

    key = kfile.read()
    key = key[:-1]
    ciphertext = ''

    if(isIV == 0):
        rndfile = Random.new()
        IV = rndfile.read(8)
        ran = random.randrange(10**80)
        myhex = "%64x" %ran
        myhex = myhex[:16]
    else:
        myhex = vfile.read()
        myhex = myhex[:-1]
        myhex = myhex[:16]

    ctr = myhex
    myhex = bytes(myhex, 'utf-8')

    IV = ba.hexlify(IV)
    padded = pad(message)

    ciphertext = createCipher(ciphertext, ctr)
    for i in range(len(padded)):
        if(i%blocksize == blocksize-1 and i != 0):
            l.append(padded[i-blocksize+1:i+1])
    
    #for i in range(len(l)):
    #    print("hex is " + str((l[i])))

    ctr = int(myhex, 16)

    output = mp.Queue()
    #myhex is IV
    processes = [mp.Process(target=encrypt, args=(key, ctr+i, l[i], output)) for i in range(len(l))]
    for p in processes:
        p.start()
    for p in processes:
        p.join()

    results = [output.get() for p in processes]
    #print(type(results[0].decode('utf-8')))
    for i in range(len(results)):
        ciphertext = createCipher(ciphertext, results[i].decode('utf-8'))

    ofile.write(ciphertext)

def pad(message):
    
    padamount = 8 - len(message) % 8
    padbyte = chr(padamount)
    padded = (message + padbyte * padamount).encode('utf-8')
    return padded

def encrypt(key, ctr, message, output):
    cipher = AES.AESCipher(key[:32], AES.MODE_ECB)
    aescipher = cipher.encrypt(bytes(hex(ctr)[2:], 'utf-8'))

    c = strxor.strxor(aescipher, ba.hexlify(message))
    #print(ba.hexlify(c))
    output.put(ba.hexlify(c))

def createCipher(ciphertext, message):
    ciphertext += message;
    return ciphertext

main()
