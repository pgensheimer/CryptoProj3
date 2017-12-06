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

    blocksize = 32
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

    key = kfile.read()
    key = key[:-1]
    plaintext = ''

    #myhex = bytes(myhex, 'utf-8')
    IV = message[:16]
    message = message[16:]
    message = message.encode('utf-8')
    #IV = ba.hexlify(IV)

    for i in range(len(message)):
        if(i%blocksize == blocksize-1 and i != 0):
            l.append(message[i-blocksize+1:i+1])
    
    ctr = int(IV, 16)
    print(ctr)

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
        plaintext = createCipher(plaintext, results[i].decode('utf-8'))

    ofile.write(plaintext)

def encrypt(key, ctr, message, output):
    cipher = AES.AESCipher(key[:32], AES.MODE_ECB)
    aescipher = cipher.decrypt(bytes(hex(ctr)[2:], 'utf-8'))

    c = strxor.strxor(aescipher, ba.unhexlify(message))
    #print(ba.hexlify(c))
    output.put(ba.hexlify(c))

def createCipher(ciphertext, message):
    ciphertext += message;
    return ciphertext

main()

