"""
first triangle number to ove over five hundred divisors
28 is first to have over five divisors
"""
from euler import factors, cached

def triangular():
    from itertools import count
    last = 0
    for n in count(1):
        last += n
        yield last

import sys

# def divisors(div):
#     for i,t in enumerate(triangular(),1):
#         print "\r", i, t, len(factors(t)),
#         sys.stdout.flush()
#         # if len(factors(i))+len(factors(i+1)) - 1 >= div:
#         if len(factors(t)) >= div:
#             return t

# @cached
def number_of_factors(n):
    import math
    number_of_factors = 0
    for i in xrange(1, int(math.floor(math.sqrt(n)))+1):
        if n % i == 0:
            number_of_factors +=2
        if i*i==n:
            number_of_factors -=1
    return number_of_factors

def divisors(div):
    for i,t in enumerate(triangular(),1):
        # print "\r", i, t, len(factors(t))
        # sys.stdout.flush()
        if i % 2 == 0:
            if number_of_factors(i/2)*number_of_factors(i+1) >= div:
                return i,t
        else:
            if number_of_factors(i)*number_of_factors((i+1)/2) >= div:
                return i,t
