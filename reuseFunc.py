#this funciton will include the reused functs
import sys, getopt
import binascii as ba
from Crypto.Cipher import AES

def readInputs(commandl):
    print("in reuse") 
    #call with: kname, iname, oname, vname = readInputs(sys.argv[1:])

    iname = ''
    oname = ''
    kname = ''
    vname = ''
    try:
        opts, args = getopt.getopt(commandl,"hm:t:k:v:",["kfile=", "vfile=","mfile=","tfile="])
    except getopt.GetoptError:
#	print ('test.py -k <keyfile> -v <IVfile> -i <inputfile> -o <outputfile>"')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('test.py -k <key> -v <IVfile> -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-m", "--mfile"):
            iname = arg
        elif opt in ("-t", "--tfile"):
            oname = arg
        elif opt in ("-k", "--kfile"):
            kname = arg
        elif opt in ("-v", "--vfile"):
            vname = arg
    print ('Input file is "', iname)
#    print ('key is "', kname)	
#    print ('Output file is "', oname)	
#    print ('IV file is "', vname)	

    if(kname ==''):
        print("you have to inlude a key file")
        exit(1)
    if(iname ==''):
        print("you have to include a message file")
        exit(1)
    if(oname==''):
        print("you have to include a tag file")
        exit(1)	
    return kname, iname, oname, vname


