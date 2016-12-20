def primes():
    def sixkplusminusone():
        from itertools import count
        for n in count(1):
            yield 6*n-1
            yield 6*n+1
    primes = []
    yield 2
    yield 3
    for n in sixkplusminusone():
        div = False
        if any(n % p == 0 for p in primes if p ** 2 <= n):
            div = True
        if not div:
            primes.append(n)
            yield n

def genlen(gen):
    """ Returns len(list(gen)) without temporary list creation"""
    counter = 0
    for _ in gen:
        counter += 1
    return counter

def cached(func):
    cache = { }
    def wrapped(*args):
        if args in cache:
            return cache[args]
        ret = func(*args)
        cache[args] = ret
        return ret
    return wrapped

@cached
def sieve(max):
    p = range(0,max)
    p[0] = 0
    p[1] = 0
    for i in xrange(2,max):
        r = i
        if r == 0:
            continue
        for x in xrange(r+r, max, r):
            p[x] = 0
    return [ p for p in p if p != 0 ]

@cached
def factors(number):
    # l = [ x for x in xrange(1,int(number**0.5)) if number % x == 0 ]
    l = [ x for x in xrange(1,number) if number % x == 0 ]
    l.append(number)
    return l

@cached
def propfactors(number):
    # l = [ x for x in xrange(1,int(number**0.5)) if number % x == 0 ]
    l = [ x for x in xrange(1,number) if number % x == 0 ]
    # l.append(number)
    return l

def permutations(alpha):
    # abcd
    perm = []
    if len(alpha) == 1:
        return alpha

    for el in alpha:
        sub = list(alpha)
        sub.remove(el)
        subperm = permutations(sub)
        for p in subperm:
            l = [el]
            l.extend(p)
            perm.append(l)

    return perm


def pengen(alpha, prefix = []):
    if len(alpha) == 1:
        yield prefix + alpha

    for el in alpha:
        temp = list(alpha)
        temp.remove(el)
        for n in pengen(temp, prefix + [el]):
            yield n

def mul(list):
    acc = 1
    for el in list:
        acc *= el
    return acc

def binominal(n, k):
    import fractions
    acc = 1
    for i in range(1,k+1):
        acc *= fractions.Fraction(n - i + 1,i)
    return int(acc)
