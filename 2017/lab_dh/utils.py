#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
~Gros
'''

from hashlib import sha256


def add_padding(data, block_size=16):
    """add PKCS#7 padding"""
    size = block_size - (len(data)%block_size)
    return data+chr(size)*size


def strip_padding(data, block_size=16):
    """strip PKCS#7 padding"""
    padding = ord(data[-1])
    if padding == 0 or padding > block_size or data[-padding:] != chr(padding)*padding:
        raise Exception("Invalid padding")
    return data[:-padding]


def derive_key(key_int, block_size=16):
    return sha256(str(key_int)).digest()[:16]