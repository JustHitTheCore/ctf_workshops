from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from Crypto.Hash import SHA
import sys

key = RSA.importKey(open('priv_key.pem','r').read())
FLAG = open('flag.txt', 'r').read()

def encrypt(message):
    h = SHA.new(message)
    cipher = PKCS1_v1_5.new(key)
    ciphertext = cipher.encrypt(message + h.digest())
    return ciphertext

def parity_oracle(ciphertext):
    message = key.decrypt(ciphertext)
    message = int(message.encode('hex'), 16)
    if message % 2 == 0:
        return '0'
    return '1'

if len(sys.argv) != 2 or sys.argv[1] not in ['encrypt', 'decrypt']:
    print "Usage: {} encrypt|decrypt".format(sys.argv[0])
    sys.exit(1)

if sys.argv[1] == 'encrypt':
    print encrypt(FLAG).encode('hex')
else:
    while True:
        print "Gimme ciphertext as int (-1 to exit)"
        c = raw_input()
        try:
            c = int(c)
            if c < 0:
                break
            c = hex(c)[2:].strip('L')
            c = ('0'*(len(c)&1) + c).decode('hex')
        except:
            print "incorrect"
            continue
        print parity_oracle(c)
