#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
~Gros
'''


from bob_alice import bob, alice
import argparse
import string
from pwn import *

context.log_level = 'error'
from config import config
config = config["task1"]


def sniffing():
    print("Sniffing...")

    alice = remote('localhost', config["port_alice"])
    # bob = remote('localhost', config["port_bob"])

    def send_data(data):
        print("Bob sends: {}".format(data))
        alice.sendline(data)

    def receive_data():
        data = alice.recvline().strip()
        print("Bob recvs: {}".format(data))
        return data

    bob(send_data, receive_data)


if __name__ == "__main__":
    sniffing()