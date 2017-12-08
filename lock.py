#rsa_keygen = __import__('rsa-keygen')
import subprocess
import argparse
import math
import sys, getopt
import hashlib
from paddingfunc import paddingFunc

#def readInputs(commandl):

def main():
    print(1)
    #dname, pname, rname, vkname = readInputs(sys.argv[1:])
    parser = argparse.ArgumentParser(description='take in input args')
    parser.add_argument('-d', help ='directory file',action ="store", dest="dname", type=str)
    parser.add_argument('-p', help ='action public key file',action ="store", dest="pname", type=str)
    parser.add_argument('-r', help ='private action key file',action ="store", dest="rname", type=str)
    parser.add_argument('-vk', help ='validation key file',action ="store", dest="vkname", type=str)
    args = parser.parse_args()
    print("dname is "+ args.dname)
    print("pname is "+ args.pname)
    print("rname is "+ args.rname)
    print("vkname is "+ args.vkname)

    subprocess.run(["python", "rsa-keygen.py", "-p", arg.pname, "-s", args.vkname, "-n", "256"])
    print("back from subprocess")
main()
