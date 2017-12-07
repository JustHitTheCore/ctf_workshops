#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
~Gros
'''

import sys
from hashlib import sha256
from binascii import hexlify, unhexlify
import random
import argparse
from Crypto.Cipher import AES
import os

from utils import *


class Unbuffered(object):
   def __init__(self, stream):
       self.stream = stream
   def write(self, data):
       self.stream.write(data)
       self.stream.flush()
   def __getattr__(self, attr):
       return getattr(self.stream, attr)

sys.stdout = Unbuffered(sys.stdout)


def alice(send_data, receive_data, check_parameters=False, check_keys=False):
    # get parameters
    p = 0xffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff
    g = 2

    # send parameters
    send_data(str(p))
    send_data(str(g))

    # get ACK, update p and g, send A
    if receive_data() != 'ACK':
        send_data("No ok")
        sys.exit(1)
    p_bob = int(receive_data())
    g_bob = int(receive_data())

    if check_parameters and (p_bob != p or g_bob != g):
        send_data("No ok")
        sys.exit(1)
    else:
        p, g = p_bob, g_bob

    a = random.randint(0,p-1)
    A = pow(g, a, p)
    send_data(str(A))

    # get B, compute key
    B = int(receive_data())
    if check_keys and (B <= 0 or B >= p):
        send_data("No ok")
        sys.exit(1)

    key = derive_key(pow(B, a, p))

    # send msg to bob
    iv = random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    msg = "Hello Bob, it's good day to die, isn't it?"
    msg = add_padding(msg)
    msg_enc = cipher.encrypt(msg)
    send_data(hexlify(iv+msg_enc))

    #get and print msg from bob
    msg2 = str(receive_data()).strip()
    try:
        msg2 = unhexlify(msg2)
    except TypeError:
        msg2 = unhexlify('0'+msg2)
    iv = msg2[:16]
    msg2 = msg2[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    # print(cipher.decrypt(msg2))


def bob(send_data, receive_data, check_parameters=False, check_keys=False):
    # get parameters
    p = int(receive_data())
    g = int(receive_data())

    # send ACK
    send_data('ACK')
    send_data(str(p))
    send_data(str(g))

    # get Alice public key
    A = int(receive_data())
    if check_keys and (A <= 0 or A >= p):
        send_data("No ok")
        sys.exit(1)

    # generate and send bob keys
    b = random.randint(0, p-1)
    B = pow(g, b, p)
    send_data(str(B))

    # compute shared key
    key = derive_key(pow(A, b, p))

    # get msg from alice
    msg2 = str(receive_data()).strip()
    try:
        msg2 = unhexlify(msg2)
    except TypeError:
        msg2 = unhexlify('0'+msg2)
    iv = msg2[:16]
    msg2 = msg2[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    msg2 = strip_padding(cipher.decrypt(msg2))

    #send msg to alice
    if msg2 == "Hello Bob, it's good day to die, isn't it?":
        msg = "Hello Alice. Yes it is. Flag: jhtc{Remember when we had guns and drums?}"
    else:
        msg = "Meh"

    iv = random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    msg = add_padding(msg)
    msg_enc = cipher.encrypt(msg)
    send_data(hexlify((iv+msg_enc)))


def send_data(data):
    print(data)


def receive_data():
    return raw_input()


# Subgroups confinement start
def xor(a, b):
    return ''.join(chr(ord(x)^ord(y)) for x,y in zip(a,b))

def mac(K, m):
    """Compute HMAC
        K(string): key
        m(string): message
    """
    block_size = sha256().block_size
    if len(K) > block_size:
        K = sha256(K).digest()
    if len(K) < block_size:
        K += '\x00'*(block_size - len(K))

    o_key_pad = '\x5c'*block_size
    i_key_pad = '\x36'*block_size
    o_key_pad = xor(o_key_pad, K)
    i_key_pad = xor(i_key_pad, K)
    return sha256(o_key_pad + sha256(i_key_pad + m).digest()).digest()

def verify(K, m, t):
    """Verify HMAC
        K(string): key
        m(string): message
        t(string): tag
    """
    if t == mac(K, m):
        return True
    return False

def i2b(number):
    """Integer to bytes"""
    number_bytes = ''
    while number:
        number_bytes += chr(number & 0xff)
        number >>= 8
    return number_bytes[::-1]

def bob_non_empheral(send_data, receive_data):
    p = 7199773997391911030609999317773941274322764333428698921736339643928346453700085358802973900485592910475480089726140708102474957429903531369589969318716771
    g = 4565356397095740655436854503483826832136106141639563487732438195343690437606117828318042418238184896212352329118608100083187535033402010599512641674644143

    with open('subgroups_confinement_config.txt', 'r') as f:
        bob_secret_key = int(f.readline().strip())

    public_key = int(receive_data())
    key = pow(public_key, bob_secret_key, p)
    key = derive_key(key)

    m = "Sztuka nie ma żadnego celu"
    t = hexlify(mac(key, m))
    send_data(m)
    send_data(t)

def sc_setup():
    p = 7199773997391911030609999317773941274322764333428698921736339643928346453700085358802973900485592910475480089726140708102474957429903531369589969318716771
    g = 4565356397095740655436854503483826832136106141639563487732438195343690437606117828318042418238184896212352329118608100083187535033402010599512641674644143
    q = 236234353446506858198510045061214171961  # order of g

    flag = 'jhtc{lallala kotki dwa kotki dwa}'
    flag = add_padding(flag)

    bob_secret_key = random.randint(2, q-1)

    alice_secret = random.randint(2, q-1)
    alice_public = pow(g, alice_secret, p)

    key = pow(alice_public, bob_secret_key, p)
    key = derive_key(key)

    iv = random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    flag_enc = cipher.encrypt(flag)

    with open('subgroups_confinement_config.txt', 'w') as f:
        f.write(str(bob_secret_key)+'\n')
        f.write(str(alice_public)+'\n')
        f.write(hexlify(flag_enc)+'\n')
# Subgroups confinement end


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run alice or bob.')
    parser.add_argument('what_run', type=str, nargs=1,
                   help='What to run', choices=['alice', 'bob', 'subgroups_confinement'])

    parser.add_argument('--check_parameters', action='store_const', const=True,
                        default=False, help='check_parameters')

    parser.add_argument('--check_keys', action='store_const', const=True,
                        default=False, help='check_keys')

    args = parser.parse_args()

    try:
        if args.what_run[0] == 'alice':
            alice(send_data, receive_data, args.check_parameters, args.check_keys)
        elif args.what_run[0] == 'bob':
            bob(send_data, receive_data, args.check_parameters, args.check_keys)
        elif args.what_run[0] == 'subgroups_confinement':
            if not os.path.isfile('subgroups_confinement_config.txt'):
                sc_setup()
            bob_non_empheral(send_data, receive_data)
        else:
            print("Nope")
    except Exception as e:
        print("Something wrong!", e)