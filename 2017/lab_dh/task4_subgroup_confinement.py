#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
~Gros
'''


from bob_alice import bob, alice
import argparse
import string
from pwn import *
from binascii import unhexlify, hexlify

from config import config


def sc():
    print("Subgroup-Confinement...")

    with open('subgroups_confinement_config.txt', 'r') as f:
        bob_secret_key = int(f.readline().strip())
        alice_public = int(f.readline().strip())
        flag_enc = unhexlify(f.readline().strip())

    print("Alice public key: {}".format(alice_public))
    print("Encrypted flag: {}".format(hexlify(flag_enc)))
    
    bob = remote(config["host"], config["task4"]["port_bob"])

    # to implement
    pass


if __name__ == "__main__":
    sc()