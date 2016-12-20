"""
Collatz sequence:
    n/2 if n is even
    3*n + 1 if n is odd

collatz(13): [13, 40, 20, 10, 5, 16, 8, 4, 2, 1]
len(collatz(13)): 10

Longest chain uner one million?
"""

def collatz(n):
    if n < 1:
        raise ValueError("Values to be greater than 0")
    yield n
    while n != 1:
        n = (n / 2) if n % 2 == 0 else (3 * n + 1)
        yield n

print(list(collatz(13)))


def under_x(max_v):
    return (collatz(x) for x in xrange(1,max_v+1))

from euler import genlen

# gens = under_x(13)
gens = under_x(1000000)
lens = (genlen(x) for x in gens)

from operator import itemgetter

m = max(enumerate(lens,1), key=itemgetter(1))

print m
