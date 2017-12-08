## DH


#### Schemat Diffie-Helman

```
Alice                             Bob:
a = rand 2..n                     b = rand 2..n
A = g^a % p                       B = g^b % p
 ( strony wymieniają klucze publiczne )
<dostaje B>   <--------------->   <dostaje A>

Wspólny sekret:
B^a % p = g^(ab) % p              A^b % p = g^(ab) % p
```


#### Task2 / Task3

Man in the middle kontra diffie-hellman

Opcje ataków:
1. zmienić klucze publiczne A i B na p lub na 0
2. zwykły mitm (szyfrować osobno z każdą ze stron)
3. można zmienić g:
    * na 0, klucz wyjdzie 0
    * na p, klucz wyjdzie 0
    * na p-1, klucz wyjdzie 1 albo p-1

   (zależnie czy potęga jest parzysta czy nieparzysta)

* Atak 1 działa, jeśli Alice i Bob nie sprawdzają, czy otrzymane klucze publiczne są poprawne
* Atak 3 działa, jeśli Alice i Bob nie sprawdzają, czy g jest poprawne
* Atak 2 działa zawsze :)

Rozwiązania w task2_mitm_solution.py oraz task3_negotiated_parameters_solution.py


#### Liczenie logarytmów dyskretnych

Problem: mając dane g, p, A = g^a % p, znaleźć a
Pięć głównych metod:

* Number field sieve ~ O(exp(log(p)^1/3))
* Pollard's rho ~ O(sqrt(p)), niedeterministyczny, da się zrównoleglać
* Baby step giant step ~ O(sqrt(p)), deterministyczny, time-memory tradeoff
* Pollard's kangaroo ~ O(sqrt(t-s)), jeśli wiemy że a należy do przedziału <s,t>, niedeterministyczny, da się zrównoleglać
* Pohlig–Hellman ~ O(sum(ei * sqrt(pi))), jeśli p-1 = product(pi^ei)

Ostatni sposób jest dla nas interesujący. Działa on dobrze, jeśli rząd grupy (czyli p-1) to iloczyn małych liczb pierwszych.
Nasz ostatni atak (subgroup confinement) to, można powiedzieć, wersja "online" algorytmu Pohlig-Hellmana.


### Task4 - Subgroup confinement

Zanim zaczniemy, będziemy potrzebować następumących algorytmów:
* gcd (największy wspólny dzielnik / algorytm euklidesa)
* egcd (rozszerzony algorytm euklidesa)
* invmod (odwrotności modulo, ponieważ nie możemy dzielić "normalnie".
  * Na wzorach to wygląda tak: b = invmod(a, p) <=> b = a^(-1) % p <=> a\*a^(-1) = 1 % p <=> a*b = 1 % p )
* crt (chińskie twierdzenie o resztach)

Teraz trochę matematyki:

* Rząd grupy to ilość elementów w grupie. Jeśli p to liczba pierwsza, to ord(p) = p-1 (pomijamy zero)
* Rząd elementu g (należącego do grupy) to najmniejsza liczba q, taka że g^q = 1 mod p
* Jeśli rząd g = p-1, to g nazywamy generatorem (bo g do kolejnych potęg wygeneruje nam całą grupę)
* Jeśli q dzieli p-1, to istnieje element g rzędu q (dokładniej, istnieje q-1 takich elementów)
* Jeśli g jest rzędu q, to podnosząc g do kolejnych potęg dostaniemy q różnych liczb (potęgowanie od pewnego momentu zacznie dawać nam te same liczby). Czyli g^x mod p = g^(x + k*q) mod p
* Jeśli chcemy znaleźć element rzędu r, to liczmy h = rand(1, p)^((p-1)/r) mod p
* Mniejsze twierdzenie Fermata: jeśli p to liczba pierwsza, to dla dowolnego elementu a mamy a^(p-1) = 1 mod p


Dla zobrazowania kod w pythonie:
```python
from random import randint
from collections import defaultdict


def order(g, p):
    for i in xrange(1, p):
        if pow(g, i, p) == 1:
            return i
    return float('inf')


def find_element_of_order_r(r, p):
    h = 1
    while h == 1:
        h = pow(randint(1, p), (p-1)//r, p)
    return h


p = (2*13*71) + 1
g = 5
assert order(g, p) == p-1

r = 13
h = find_element_of_order_r(r, p)
assert pow(h, r, p) == 1

# może zająć trochę czasu...
elements_with_same_order = defaultdict(int)
elements_with_order_r = set()
generators = set()
for h in xrange(1, p):
    o = order(h, p)
    elements_with_same_order[o] += 1
    if o == r:
        elements_with_order_r.add(h)
    elif o == p-1:
        generators.add(h)

print "Elements with order {} ({}): {}".format(r, len(elements_with_order_r), elements_with_order_r)
print "(order:number_of_elements_with_that_order): {}".format(dict(elements_with_same_order))
print "Is our g a generator: {}".format(g in generators)
```

Jak widać mamy 12 elementów rzędu 13, 70 elementów rzędu 71 oraz 840 elementów rzędu 1846 (czyli 1846 generatorów).
To 840 jest związane z funkcją phi eulera (zwana też tocjent), tj. euler_phi(p-1) = 840

Do ataku "subgroup confinement" wykorzystamy trzy rzeczy:
* prywatny klucz Boba jest stały
* rząd g jest dość niski
* rząd grupy (p-1) składa się z [dużej ilości liczb pierwszych](http://factordb.com/index.php?query=30477252323177606811760882179058908038824640750610513771646768011063128035873508507547741559514324673960576895059570)

To, że rząd g jest niski daje nam tyle, że b (klucz prywatny Boba) jest mniejsze od tego rzędu.
Większe nie może być, bo g^b mod p = g^(b + k*q) mod p


Robimy tak:
* wybieramy małą liczbę dzielącą p-1 (r)
* liczymy element rzędu r (h = rand(1, p)^((p-1)/r) mod p)
* Bob policzy klucz symetryczny (key = h^b mod p). b to klucz sekretny Boba
* Bob wyśle nam parę {"jakaś wiadomość", mac(key, "jakaś wiadomość")}, gdzie mac to message-authentication-code
* My wiemy, że key ma r możliwych wartości. Wiemy to stąd, że Bob podniósł do potęgi nasze h, a h jest rzędu r
* Ponieważ r jest małe, możemy sprawdzać wszystkie wartości od 1 do r, dopóki nie znajdziemy takiego x, że h^x = key mod p
* Teraz wiemy, że x = b mod r
* Zbieramy dużo równań jak powyżej (tj. xi = b mod ri), zbieramy dopóki iloczyn ri <= q
* Używamy chińskiego twierdzenia o resztach do obliczenia b
* BOM. Mamy klucz prywatny Boba