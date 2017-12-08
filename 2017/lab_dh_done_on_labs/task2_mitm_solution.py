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
from pwn import *

from utils import *
from config import config


def mitm():
    print("MITM (key-fixing attack)...")

    alice = remote(config["host"], config["task2"]["port_alice"])
    bob = remote(config["host"], config["task2"]["port_bob"])

    # alice p,g--> bob
    p = int(alice.recvline().strip())
    g = int(alice.recvline().strip())
    print "p = {}".format(p)
    print "g = {}".format(g)

    key = derive_key("0")
    evil_AB = p

    bob.sendline(str(p))
    bob.sendline(str(g))

    # alice <--ACK,p,g bob
    bob.recvline().strip()
    bob.recvline().strip()
    bob.recvline().strip()

    alice.sendline('ACK')
    alice.sendline(str(p))
    alice.sendline(str(g))

    # alice A--> bob
    A = int(alice.recvline().strip())
    print "A = {}".format(A)
    print "set A = evil_AB"
    bob.sendline(str(evil_AB))

    # alice <--B bob
    B = int(bob.recvline().strip())
    print "B = {}".format(B)

    print "set B = evil_AB"
    alice.sendline(str(evil_AB))

    # get msg from alice
    msg_from_alice = unhexlify(alice.recvline().strip())
    iv = msg_from_alice[:16]
    msg_from_alice = msg_from_alice[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    msg = strip_padding(cipher.decrypt(msg_from_alice))
    print "Msg from alice: {}".format(msg)

    # send bob evil msg
    fake_msg_from_alice = msg
    fake_msg_from_alice = add_padding(fake_msg_from_alice)
    iv = random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    msg_enc = cipher.encrypt(fake_msg_from_alice)
    bob.sendline(hexlify(iv+msg_enc))

    # get msg from bob
    msg_from_bob = unhexlify(bob.recvline().strip())
    iv = msg_from_bob[:16]
    msg_from_bob = msg_from_bob[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    msg = strip_padding(cipher.decrypt(msg_from_bob))
    print "Msg from bob: {}".format(msg)

    # send alice evil msg
    fake_msg_from_bob = 'I am so evil!'
    fake_msg_from_bob = add_padding(fake_msg_from_bob)
    iv = random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    msg_enc = cipher.encrypt(fake_msg_from_bob)
    alice.sendline(hexlify(iv+msg_enc))


if __name__ == "__main__":
    mitm()