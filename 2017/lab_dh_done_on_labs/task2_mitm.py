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


def mitm():
    print("MITM (key-fixing attack)...")

    alice = remote(config["host"], config["task2"]["port_alice"])
    bob = remote(config["host"], config["task2"]["port_bob"])

    p = int(alice.recvline())
    g = int(alice.recvline())

    bob.sendline(str(p))
    bob.sendline(str(g))

    # Bob will send ACK, p, g
    alice.send(bob.recvline())
    alice.send(bob.recvline())
    alice.send(bob.recvline())

    print "Alice =", alice.recvline()
    print "Bob =", bob.recvline()

    """
    Schemat Diffie-Helman

    Alice                             Bob:
    a = rand 2..n                     b = rand 2..n
    A = g^a % p                       B = g^b % p
     ( strony wymieniają klucze publiczne )
    <dostaje B>   <--------------->   <dostaje A>

    Wspólny sekret:
    B^a % p = g^(ab) % p              A^b % p = g^(ab) % p

    Opcje ataków:
    1) zmienić klucze publiczne A i B na p lub na 0
    2) zwykły mitm (szyfrować osobno z każdą ze stron)
    3) można zmienić g:
     * na p, klucz wyjdzie 0
     * na p-1, klucz wyjdzie 1 albo p-1
       (zależnie czy potęga jest parzysta czy nieparzysta)
    (bo Alice nie sprawdza czy jest poprawne i używa zmienionego)
    """




if __name__ == "__main__":
    mitm()
