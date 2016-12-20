from itertools import count

def factorial(number):
    from itertools import count
    fact = []
    for i in count(2):
        if number < i:
            break
        if number % i == 0:
            fact += [i]
            number /= i
    return fact

def multiple(max):
    r = range(2,max+1)
    for i in count(max,max):
        rem = [ i % x for x in r ]
        s = sum(rem)
        if not s:
            return i

def fmultiple(max):
    r = range(2,max+1)
    for i in count(max,max):
        if any(i % x for x in r):
            continue
        return i

def fastmult(max):
    r = range(2,max+1)
    for i in count(1):
        found = True
        for x in r:
            if i % x:
                found = False
                break


def fact_mul(max):
    s = range(2,max)
    f = [factorial(x) for x in s]
    return f


def lcm(r):
    s = set(r)

