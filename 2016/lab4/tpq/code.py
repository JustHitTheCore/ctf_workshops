import gmpy2
import random

FLAG = int(open('flag.txt','r').read().encode('hex'), 16)

def encrypt(m, e, p, q):
    return pow(m, e, p*q)

def main():
    print "Generate primes..."
    primes = [gmpy2.next_prime(random.randint(1<<511, (1<<512)-1)) for x in xrange(10)]
    while True:
        print "Index of p: "
        p = int(raw_input())
        print "Index of q: "
        q = int(raw_input())
        if p < 0 or p > 9 or q < 0 or q > 9:
            print "index not in [0,9]"
            sys.exit(1)
        print encrypt(FLAG, 0x10001, primes[p], primes[q])

if __name__ == "__main__":
    main()
