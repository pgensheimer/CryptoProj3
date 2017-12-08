#rsa_keygen = __import__('rsa-keygen')
import subprocess
import argparse
import math
import sys, getopt
import hashlib
import os
from paddingfunc import paddingFunc

#def readInputs(commandl):

def main():
    #print(1)
    #dname, pname, rname, vkname = readInputs(sys.argv[1:])
    parser = argparse.ArgumentParser(description='take in input args')
    parser.add_argument('-d', help ='directory file',action ="store", dest="dname", type=str)
    parser.add_argument('-p', help ='action public key file',action ="store", dest="pname", type=str)
    parser.add_argument('-r', help ='private action key file',action ="store", dest="rname", type=str)
    parser.add_argument('-vk', help ='validation key file',action ="store", dest="vkname", type=str)
    args = parser.parse_args()
    #print("dname is "+ args.dname)
    #print("pname is "+ args.pname)
    #print("rname is "+ args.rname)
    #print("vkname is "+ args.vkname)

    ret = subprocess.check_output(["python", "rsa-validate.py", "-k", args.rname, "-m", args.pname, "-s", args.vkname])
    #ret = subprocess.check_output(["python", "rsa-validate.py", "-k", args.rname, "-m", args.pname, "-s", args.vkname], stdout = subprocess.PIPE)
    #stdout=ret.communicate()
    #print(ret)
    if ret == b'True\r\n':
        val = 0
        #print("accept")
    else:
        print("failure: problem verifying public key information")
        exit(1)
    randkey = os.urandom(32)
    aesfilename = "randAESkey"
    aeskey = open(aesfilename, 'w')
    aeskey.write(str(randkey))
    aeskey.close()
    aeskey = open(aesfilename, 'r')
    symkeyfile = "symkeyman"
    keymanifest = open(symkeyfile, 'w')
    
    print(randkey)
    #make randkeyfile

    keymanifest.close()
    aeskey.close()
    ret = subprocess.check_output(["python", "rsa-enc.py", "-k", args.pname, "-i", aesfilename, "-o", symkeyfile])
    
  #  subprocess.run(["python", "rsa-keygen.py", "-p", args.pname, "-s", args.vkname, "-n", "256"])
    #print("back from subprocess")
main()
