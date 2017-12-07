#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
~Gros
'''

import sys
from hashlib import sha256
from binascii import hexlify, unhexlify
from utils import *
import random
import argparse
from Crypto.Cipher import AES


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
        iv = random_bytes(16)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        msg = "Hello Alice. Flag: jhtc{Remember when we had guns and drums?}"
        msg = add_padding(msg)
        msg_enc = cipher.encrypt(msg)
        send_data(hexlify((iv+msg_enc)))


def send_data(data):
    print(data)


def receive_data():
    return raw_input()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run alice or bob.')
    parser.add_argument('what_run', type=str, nargs=1,
                   help='What to run', choices=['alice', 'bob'])

    parser.add_argument('--check_parameters', action='store_const', const=True,
                        default=False, help='check_parameters')

    parser.add_argument('--check_keys', action='store_const', const=True,
                        default=False, help='check_keys')

    args = parser.parse_args()

    try:
        if args.what_run[0] == 'alice':
            alice(send_data, receive_data, args.check_parameters, args.check_keys)
        else:
            bob(send_data, receive_data, args.check_parameters, args.check_keys)
    except Exception as e:
        print("Something wrong!", e)