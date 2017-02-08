#!/usr/bin/python3
# -*-coding:Utf-8 -*

"""  
caesarCustom is a small program based on caesar encryption used to encrypt/decrypt files 

Usage : caesarCustom.py path command key

path : path to the file to encrypt/decrypt
command : c -> encryption mode; d -> decryption mode
key : key used to encrypt/decrypt, example : this_is_a_key 
"""

import sys
import re

alphabet = {"a":0, "b":1, "c":2, "d":3, "e":4, "f":5, "g":6, "h":7, "i":8, "j":9, "k":10, "l":11, "m":12, "n":13, "o":14, "p":15, "q":16, "r":17, "s":18, "t":19, "u":20, "v":21, "w":22, "x":23, "y":24, "z":25}

key = ""



def checkArgs():

    global key
    
    if len(sys.argv) == 2 and sys.argv[1] == "--help":
        print (__doc__)
        sys.exit()

    elif len(sys.argv) < 4:
        print ("Arguments missing, see help with caesarCustom.py --help")
        sys.exit()

    elif len(sys.argv) > 4:
        print ("Too much parameters, see help with caesarCustom.py --help")
        sys.exit()
    
    else:
        if sys.argv[2] != "c" and sys.argv[2] != "d":
            print ("Bad command option, see help with caesarCustom.py --help")
            sys.exit()
        
        key = sys.argv[3].lower()
        if not re.match("^([a-z]+)(_[a-z]+)*$", key):
           print ("Bad key, see help with caesarCustom.py --help")
           sys.exit()
        
        key = "".join(key.split("_"))


def keyCalculus():

    keyValue = 0
    for c in key:
        keyValue = ((keyValue + alphabet[c]) % 26) + 1 

    return keyValue
    
def encrypt(shift):
    
    print("****Ecryption mode****")
    try:
        src = open(sys.argv[1], "rb")

    except:
        print("File not found") 
        sys.exit()

    else:
        content = src.read()
        ciphertext = ""
        cmpt = 0
        for c in content:
            if c >= 97 and c <= 122:
                ciphertext += chr(((alphabet[chr(c)] + shift + cmpt) %26 + 97))
            elif c >= 65 and c <= 90:
                ciphertext += chr(((alphabet[chr(c).lower()] + shift + cmpt) %26 + 65))
            else:
                ciphertext += chr(c)

            cmpt = (cmpt + 1)%5

        print("Ciphertext : \n" + ciphertext)
        src.close()
    

def decrypt(shift):
    
    print("****Decryption mode****")
    
    try:
        src = open(sys.argv[1], "rb")

    except:
        print("File not found") 
        sys.exit()

    else:
        content = src.read()
        plaintext = ""
        cmpt = 0
        for c in content:
            if c >= 97 and c <= 122:
                plaintext += chr(((alphabet[chr(c)] - (shift + cmpt) + 26) %26 + 97))
            elif c >= 65 and c <= 90:
                plaintext += chr(((alphabet[chr(c).lower()] - (shift + cmpt) + 26) %26 + 65))
            else:
                plaintext += chr(c)
            
            cmpt = (cmpt + 1)%5

        print("Plaintext :\n" + plaintext)
        src.close()
    

if __name__ == "__main__":
    
    checkArgs()
    shift = keyCalculus()
    if sys.argv[2] == "c":
        encrypt(shift)

    elif sys.argv[2] == "d":
        decrypt(shift)
    
    
