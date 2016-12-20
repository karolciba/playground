cache = {}

def cache_fib(n):
    if n == 0:
        return 0
    if n == 1:
        return 1;
    if n in cache:
        return cache[n]
    f = cache_fib(n-1) + cache_fib(n-2)
    cache[n] = f
    return f

def plain_fib(n):
    if n == 0:
        return 0
    if n == 1:
        return 1;
    f = plain_fib(n-1) + plain_fib(n-2)
    return f

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
def fib(n):
    if n == 0:
        return 0
    if n == 1:
        return 1;
    f = fib(n-1) + fib(n-2)
    return f

from itertools import count

def even_valued(func):
    s = 0
    for i in count(1):
        f = func(i)
        if f > 4000000:
            break
        if f % 2 == 0:
            print "adding", f, "to", s
            s += f

    return s



