## Diffie-Hellman

### Tasks

* implementation
* mitm
    + key-fixing attack
    + negotiated groups, malicious "g" parameters
    + subgroup-confinement attack


### Classical Diffie-Hellman
```
p - 
g - 
a
b
A
B

Alice  -->  p, g       -->  Bob
Alice  <--  ACK, p, g  <--  Bob
Alice  -->  A          -->  Bob
Alice  <--  B          <--  Bob
Alice  -->  E(msg1)    -->  Bob
Alice  <--  E(msg2)    <--  Bob    <-- flag in msg2, if msg1 is correct
```

### Setup
On remote server run: `bash ./setup.sh`
In config.py setup host properly

Sniffing only:
`nc host 10003`

MITM with checks on parameters
`nc host 10001  # alice`
`nc host 10002  # bob`

MITM with checks on keys
`nc host 30001  # alice`
`nc host 30002  # bob`

Subgroups Confinement
Private key is generated at server start
`nc host 40001`


### Overwiew

##### Task1.
Just to check if you can break dh only sniffing ;)
`python ./task1_sniffing.py`

##### Task2.
Man in the middle (key-fixing attack)
`python ./task2_mitm.py`
DH without authentication can be broken with simple MITM attack. Just negotiate keys separately with alice and bob.
Somehow more funny method is to set public keys to, for example, p.

##### Task3
Man in the middle (negotiated groups, malicious "g" parameters)
`python ./task3_negotiated_parameters.py`
Simmilar to above, but we are playing with group parameters.

##### Task4
Subgroups Confinement
`python ./task4_subgroup_confinement.py`
This attack can be used with non-empheral dh (when bob's private key doesn't change), when order of group generator is small enough and groups order is somehow smooth. It's about forcing shared key to be in small subgroup, so it's possible to bruteforce it.

### Links
[Cryptopals](https://cryptopals.com/sets/5)
