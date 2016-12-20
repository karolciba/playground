
def prime_gen():
    from itertools import count
    primes = []
    yield 2
    for n in count(3,2):
        div = False
        if any(n % p == 0 for p in primes):
            div = True
        # print "testing", n, primes
        if not div:
            primes.append(n)
            yield n

def prime_gen_f():
    from itertools import count
    primes = []
    yield 2
    for n in count(3,2):
        div = False
        if any(n % p == 0 for p in primes if p ** 2 <= n):
            div = True
        # print "testing", n, primes
        if not div:
            primes.append(n)
            yield n

def prime_no(no):
    g = prime_gen()
    p = 0
    for i in xrange(1,no+1):
        p = g.next()
        if i == no:
            return p

def prime_no_f(no):
    g = prime_gen_f()
    p = 0
    for i in xrange(1,no+1):
        p = g.next()
        if i == no:
            return p

def prime_no_ff(no):
    from prime import primes
    g = primes()
    p = 0
    for i in xrange(1,no+1):
        p = g.next()
        if i == no:
            return p

