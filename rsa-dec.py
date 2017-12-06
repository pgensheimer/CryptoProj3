#this file decrypts an encryption of an integer using RSA


import sys, getopt


def readInputs(commandl):
    kname = ''
    iname = ''
    onmae = ""
    try:
        opts, args = getopt.getopt(commandl, "k:i:o:", ["kfile=", "ifile =", "ofile="])
    except getopt.GetoptError:
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-k", "--kfile"):
            kname = arg
        elif opt in ("-i", "--ifile"):
            iname = arg
        elif opt in ("-o", "--ofile"):
            oname = arg
    if(oname == ''):
        print("you have to include an output file")
        exit(1)
    if(iname == ''):
        print("you have to include an input file")
        exit(1)
    if(kname == ''):
        print("must include fiel with RSA key in correct format")
        exit(1)
    
    return kname, iname, oname

def modexp(cipher, d, n):
    count = 1
    while d:
        if d & 1:
            count = count * cipher % n
        d >>= 1
        cipher = cipher * cipher % n
    return count
    #print(count)

def getMess(int_mess):
    padded_mess = int(int_mess).to_bytes(len(str(int_mess)), byteorder='big')
    reverse_mess = padded_mess[::-1]
    plaintext = ''
    for i in range(len(reverse_mess)):
        cur_char = chr(reverse_mess[i])
        plaintext += cur_char
        if(cur_char == '\x00'):
            break
    return(plaintext)

def main():
    kname, iname, oname = readInputs(sys.argv[1:])

    k = open(kname, 'r')
    i = open(iname, 'r')
    o = open(oname, 'w')

    numbits = int(k.readline().rstrip())
    n = int(k.readline().rstrip())
    d = int(k.readline().rstrip())
    cipher = int(i.read().rstrip())

    int_mess = modexp(cipher, d, n)
    plaintext = getMess(int_mess)[::-1]
    #print(plaintext[1:])

    o.write(plaintext[1:])

main()
