#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
~Gros
'''

import sys
from hashlib import sha256
from binascii import hexlify, unhexlify
from utils import *


def alice(send_data, receive_data, stage):
    # get parameters
    p = 0xffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff
    g = 2

    # send parameters
    with stage[0]:
        send_data(str(p))
        send_data(str(g))
        stage[0].notify_all()

    # get ACK, update p and g, send A
    with stage[1]:
        stage[1].wait()
        if receive_data() != 'ACK':
            send_data("No ok")
            sys.exit(1)
        p = int(receive_data())
        g = int(receive_data())

    # send alice public key
    with stage[2]:
        a = random.randint(0,p-1)
        A = pow(g, a, p)
        send_data(str(A))
        stage[2].notify_all()

    # get B, compute key
    with stage[3]:
        stage[3].wait()
        B = int(receive_data())
        key = derive_key(pow(B, a, p))

    # send msg to bob
    with stage[4]:
        iv = random_bytes(16)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        msg = "Hello Bob, it's good day to die, isn't it?"
        msg = add_padding(msg)
        msg_enc = cipher.encrypt(msg)
        send_data(hexlify(iv+msg_enc))
        stage[4].notify_all()

    #get and print msg from bob
    with stage[5]:
        stage[5].wait()
        msg2 = unhexlify(str(receive_data()).strip())
        iv = msg2[:16]
        msg2 = msg2[16:]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        print(cipher.decrypt(msg2))


def bob(send_data, receive_data, stage):
    # get parameters
    with stage[0]:
        stage[0].wait()
        p = int(receive_data())
        g = int(receive_data())

    # send ACK
    with stage[1]:
        send_data('ACK')
        send_data(str(p))
        send_data(str(g))
        stage[1].notify_all()

    # get Alice public key
    with stage[2]:
        stage[2].wait()
        A = int(receive_data())

    # generate and send bob keys
    with stage[3]:
        b = random.randint(0, p-1)
        B = pow(g, b, p)
        send_data(str(B))
        stage[3].notify_all()

    # compute shared key
    key = derive_key(pow(A, b, p))

    # get msg from alice
    with stage[4]:
        stage[4].wait()
        msg2 = unhexlify(str(receive_data()).strip())
        iv = msg2[:16]
        msg2 = msg2[16:]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        msg2 = strip_padding(cipher.decrypt(msg2))

    #send msg to alice
    if msg2 == "Hello Bob, it's good day to die, isn't it?":
        msg = "Hello Alice. Flag: jhtc{Remember when we had guns and drums?}"
    else:
        msg = "Hello Alice. How do you do?"

    with stage[5]:
        iv = random_bytes(16)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        msg = add_padding(msg)
        msg_enc = cipher.encrypt(msg)
        send_data(hexlify((iv+msg_enc)))
        stage[5].notify_all()


