#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
~Gros
'''


from bob_alice import bob, alice
import argparse
import string
from pwn import *

from config import config


def np():
    print("MITM (negotiated groups)...")

    alice = remote(config["host"], config["task3"]["port_alice"])
    bob = remote(config["host"], config["task3"]["port_bob"])

    # to implement
    pass


if __name__ == "__main__":
    np()