import prime
from itertools import count

upto = 2000000

def gsum():
    s = 0
    g = prime.primes()
    for x in count():
        p = g.next()
        if p > upto:
            break
        s += g.next()
    return s

def ssum():
    p = prime.sieve(upto)
    return sum(p)
