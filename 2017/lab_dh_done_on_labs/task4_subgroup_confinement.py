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
    """
    Założenie: klucz prywatny Boba jest stały (czyli 'b')
    
    Wysyłamy do Boba jakąś liczbę 'h' i on nam odpowiada
    h^b % p

    #g to 'rząd g'
    #g = x

    (...)

    Finalnie będziemy mieć zbiór rownań:
    b % p1 = 37 % p1
    b % p2 = 29 % p2
    b % p3 = .. % p3

    Które można rozwiązać przez Chineese Remainder Theorem

    Z uwagi że gdzieś po drodze będziemy mieć dzielenie, trzeba pamiętać,
    że w arytmetyce modulo nie może nam wyjść ułamek więc:
        x / y % p
    
    Zapisujemy jako:
        x * y^(-1) % p

    Gdzie y^(-1) to ,,odwrotność liczby y'', do którego policzenia wykorzystuje się
    rozszerzony algorytm Euklidesa: http://eduinf.waw.pl/inf/alg/001_search/0009.php
    """
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

    """

    """

if __name__ == "__main__":
    sc()
