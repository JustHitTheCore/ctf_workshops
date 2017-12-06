#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
~Gros
'''


from bob_alice import bob, alice
import multiprocessing


def send_data(data):
    print(data)


def receive_data():
    return raw_input()


if __name__ == "__main__":
    stage = [multiprocessing.Condition() for _ in xrange(6)]
    alice = multiprocessing.Process(target=alice, args=(send_data, receive_data, stage[:]))
    bob = multiprocessing.Process(target=bob, args=(send_data, receive_data, stage[:]))

    alice.start()
    bob.start()

    alice.join()
    bob.join()