#this is the encryption padding function
import os

def paddingFunc(message, length):
    #should return 00 02 Rand 00 message

    padded = b''
    mlength = len(message)
    length = int(length/8)
    ##if mlength > (length-11):
     ##   print("not enough space for padding")
      ##  return 1
    
    padded = b''

    while(len(padded) < length):
        left = length - len(padded)
        
        #newpad = os.urandom(left +20)
        newpad = b'01'
        newpad = newpad.replace(b'00', b'')
        padded = padded + newpad[:left]


    if(len(padded) != length):
        print("padded is the wrong size")
        return 1

  #  message = (bytearray(message.encode('utf-8')))
    pad = b''.join([b'\x00\x02', padded, b'\x00'])
    while(len(message)+len(pad) < (length*2)/8):
        pad = b''.join([pad, b'\x00'])

    pad = b''.join([pad, message])
    return pad.rstrip()

if __name__ == "__main__":
    message = str(9234532)
    padded = paddingFunc(message, 256)
    print(padded)
    
