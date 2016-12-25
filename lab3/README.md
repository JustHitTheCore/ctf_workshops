## [RSA](https://pl.wikipedia.org/wiki/RSA_(kryptografia))

RSA bazuje na problemie faktoryzacji liczb. Najszybszy znany algorytm (dla ogólnego przypadku) to General Number Field Sieve, inne [tutaj](http://stackoverflow.com/a/2274520).

Pierwszy przedstawiony na warsztatach atak dotyczy użycia zbyt małego klucza (zadanie male_jest_piekne z pwning ctf autorstwa p4). Ponieważ n jest małe (263 bity, przy zalecanej wielkości >=2048 bitów) możemy je łatwo sfaktoryzować, korzystając na przykłaz z tej strony: <http://factordb.com/index.php?query=13513545201780754751363061730973412461964840798555163524204230289623875027547891>

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import gmpy2
from Crypto.PublicKey import RSA
from pwn import *


n = 13513545201780754751363061730973412461964840798555163524204230289623875027547891
p = 2425967623052370772757633156976982469681
q = 5570373270183181665098052481109678989411
e = 65537

# obliczamy `d` bo jest potrzebne do deszyfrowania
# d * e = phi(n) == ( (p-1) * (q-1) ) % n
#
# dwrotność modulo liczy się z rozszerzonego algorytmu Euklidesa
# my skorzystamy z biblioteki gmpy2

d = long(gmpy2.invert(e, (p-1)*(q-1)))

key = RSA.construct((n, long(e)))

# szyfrowanie  : pow(m, e, n)    --> 3ci arg to (mod n)
# deszyfrowanie: pow(c, d, n)    --> 3ci arg to (mod n)

ciphertext = int(open('flag.txt').read(), 16)
plaintext = pow(ciphertext, d, n)

pt_str = pack(plaintext, 160, 'big')
print "Decoded: ", pt_str
```

Kolejny atak wykorzystuje mały publiczny wykładnik (małe e).

```python
message = 7106412  # "lol" - tego nie znamy, to jest szukane

# Te rzeczy znamy (n,e) - klucz publiczny
n = pierdolnie duża liczba
e = 3
ciphertext = pow(message, e, n)
plaintext_decrypted = gmpy2.iroot(ciphertext, e)[0]  # pierwiastek 3 stopnia
```
Ponieważ moduł (n) jest duży, a wykładnik (e) oraz plaintext są małe, zaszyfrowana wiadomość jest mniejsza od n i wystarczy obliczyć odpowiedni pierwiastek z szyfrogramu. W praktyce raczej nie spotykane, istnieją jednak inne ataki działające tylko dla małego e, np:

* [Håstad's broadcast attack](https://en.wikipedia.org/wiki/Coppersmith's_attack) - pozwala odszyfrować wiadomość, jeśli została zaszyfrowana e razy różnymi kluczami
* Franklin-Reiter related-message attack - podobnie jak wyżej, tylko wiadomości powiązane są znanym wielomianem

Kolejne zadanie z warsztatów dotyczy wykorzystania tej samej liczby pierwszej w dwóch kluczach.

Ktoś generuje klucze i wygenerował:

```
#!/usr/bin/env python
n1 = p1 * q
n2 = p2 * q
```
Zadanie `common_prime` - jest 100 kluczy publicznych, dwa z nich mają to samo `q`.

```python
# coding: utf-8

from itertools import combinations
from Crypto.PublicKey import RSA
import gmpy2
import base64


keys = {}

for i in range(1, 101):
    # importujemy klucze publiczne
    key = RSA.importKey(open('./common_prime/%d.pem' % i).read())
    keys[i] = key

# n1 = p1 * q
# n2 = p2 * q
# liczymy dla wszystkich kombinacji kluczy gcd(n1, n2) jeżeli wynik jest różny od 1 to znaczy że dostaliśmy q!
for (idx1, key1), (idx2, key2) in combinations(keys.items(), 2):
    n1, n2 = key1.n, key2.n

    gcd = gmpy2.gcd(n1, n2)

    if gcd != 1:
        print("Found n1, n2 collision")
        q = gcd

        p1 = n1 / q
        p2 = n2 / q
        print "p1 =", p1
        print "p2 =", p2
        print "Found in files:", idx1, idx2

        e1, e2 = key1.e, key2.e
        break

# musimy zdeszyfrowac flage
# szyfrowanie rsa: c = pow(m, e, n)
# deszyfrowanie  : m = pow(c, d, n)

with open('./common_prime/flag.enc') as f:
    flag = base64.b64decode(f.read())

# Tworzymy klucze prywatne - zeby zdeszyfrowac flage

# d = odwrotnosc e (mod fi(n))
# fi(n) = (p-1)*(q-1)
d1 = long(gmpy2.invert(e1, (p1-1)*(q-1)))
privkey1 = RSA.construct((n1, e1, d1))

d2 = long(gmpy2.invert(e2, (p2-1)*(q-1)))
privkey2 = RSA.construct((n2, e2, d2))

# deszyfrujemy
#print "Decrypted flag with privkey1:", privkey1.decrypt(flag)
#print "Decrypted flag with privkey2:", privkey2.decrypt(flag)

open('privkey1.pem', 'w').write(privkey1.exportKey())
open('privkey2.pem', 'w').write(privkey2.exportKey())

# $ openssl rsautl -inkey privkey2.pem -decrypt -in ./common_prime/flag_raw.enc -oaep
# the_flag_is_b767b9d1fe02eb1825de32c6dacf4c2ef78c738ab0c498013347f4ea1e95e8fa
```

Flaga ```-oaep``` informuje o użytym "paddingu", w tym przypadku [Optimal Asymmetric Encryption Padding](https://pl.wikipedia.org/wiki/Optimal_Asymmetric_Encryption_Padding), lub PKCS#1 v2.0.

Dwa główne zadania paddingu to:

* zapewnienie losowości
    + bo wszystkie deterministyczne schematy szyfrowania nie są [semantycznie bezpiecznie](https://en.wikipedia.org/wiki/Semantic_security))
    + bo czyste ("textbook") RSA jest [deformowalne](https://en.wikipedia.org/wiki/Malleability_(cryptography))
* sprawienie, że wiadomość jest "długa"

Innym popularnym paddingiem jest PKCS#1v1.5. Jest on jednak mniej bezpieczny od wcześniejszego (zalecany jest OAEP), np. może być podatny na padding oracle attack.

Lista ataków (niezupełna), jakby ktoś chciał się przygotować na ctfy ;)

* Mały publiczny wykładnik (low public exponent):
    + szyfrogram mniejszy od modułu n
    + [Håstad's broadcast attack](https://en.wikipedia.org/wiki/Coppersmith's_attack) - pozwala odszyfrować wiadomość, jeśli została zaszyfrowana e razy różnymi kluczami
    + Franklin-Reiter related-message attack - podobnie jak wyżej, tylko wiadomości powiązane są znanym wielomianem liniowym
    + Coppersmith’s short-pad attack - jak wyżej, tylko użyty jest krótki losowy padding (zamiast stałego wielomianu). len(padding) < (1/e^2) * len(message)
* Mały prywatny wykładnik (low private exponent):
    + [Wiener's attack](https://en.wikipedia.org/wiki/Wiener's_attack) - złamanie klucza, jeśli d < 1/3 * N^(1/4)
    + [Boneh-Durfee](https://crypto.stanford.edu/~dabo/papers/lowRSAexp.ps) - kiedy d < N^0.292
* Część klucza lub wiadomości znana (partial key/message exposure):
    + [znana część d lub p](https://www.iacr.org/archive/crypto2003/27290027/27290027.pdf) - dla małych e wystarczy znać 1/4 MSB lub LSB d lub p, dla większych e ilość wymaganych znanych bitów rośnie
    + [znana jest część wiadomości](https://github.com/mimoo/RSA-and-LLL-attacks) - szukamy N^(1/e) wiadomości (m=m0+x0, |x0|<=N^(1/e))
* Błędy implementacji (side-channel attacks):
    + [ataki czasowe, SPA, DPA](http://www.nicolascourtois.com/papers/sc/sidech_attacks.pdf)
    + [wyrocznia wypełnienia/parzystości (Bleichenbacher's padding oracle / parity oracle)](http://secgroup.dais.unive.it/wp-content/uploads/2012/11/Practical-Padding-Oracle-Attacks-on-RSA.html) - jeśli serwer (lub inna wyrocznia) informuje nas o błędzie paddingu, możemy na tej podstawie zdeszyfrować dowolną wiadomość
    + [błędy obliczeń (faulty attacks)](https://www.iacr.org/workshops/ches/ches2011/presentations/Session%204/CHES2011_Session4_3.pdf) - jeśli serwer pomyli się w trakcie deszyfrowania/podpisywania wiadomości, jest szansa na złamanie klucza
    + [podrabianie sygnatur (bleichenbacher'06 signature forgery)](https://blog.filippo.io/bleichenbacher-06-signature-forgery-in-python-rsa) -  mały publiczny wykładnik + zła implementacja funkcji weryfikującej podpisy umożliwia podrabianie sygnatur
* Inne:
    + [oślepianie sygnatur (blinding)](https://en.wikipedia.org/wiki/Blind_signature#Dangers_of_blind_signing) - podrabianie podpisów wykrzystujące deformowalność RSA
    + Wspólna liczba pierwsza (common prime) - jeśli dwa klucze współdzielą liczbę pierwszą, możemy je złamać
* Faktoryzacja:
    + [Fermata](https://en.wikipedia.org/wiki/Fermat's_factorization_method) - czynnik blisko pierwiastka z n
    + bazy liczb: <https://factordb.com>
    + [Shora](https://en.wikipedia.org/wiki/Shor's_algorithm) - kwantowe czary-mary. Szybko faktoryzujemy liczby, więszkość obecnie używanych systemów (klucza publicznego) umiera (np. RSA, Diffie-Hellman, ElGamal, ECC, DSA). Przechodzimy na inne (np. McEliece, NTRU, HFE). Potem i tak zabijają nas zombie... A serio, to niektórzy podejżewają wejście komputerów kwantowych w tym półwieczu, więc "be ready" (niepotwierdzone info, nie mogę znaleźć linków). Źródła [tutaj](http://www.math.unicaen.fr/~nitaj/postquant.pdf) i [tutaj](https://pqcrypto.org)

Do poczytania (oprócz linków w tekście):
* [Twenty Years of Attacks on the RSA Cryptosystem](https://crypto.stanford.edu/~dabo/papers/RSA-survey.pdf) - Dana Boneha, klasyka
* [Kurs tegoż pana na coursera.org](https://www.coursera.org/learn/crypto)
* [Jeden z ciekawych blogów](https://www.cryptologie.net)
* [więcej o SPA i DPA](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.567.4078&rep=rep1&type=pdf)

Do ćwiczeń i kodzenia (oprócz ctfów):
* [zadania z Crypto Village DEFCON 2016](https://id0-rsa.pub)
* [Wechall crypto](https://www.wechall.net/challs/Crypto/by/chall_score/ASC/page-1)
* [CHARM](http://charm-crypto.com/index.html)
* [SageMath](http://www.sagemath.org) - majca w pythonie :]