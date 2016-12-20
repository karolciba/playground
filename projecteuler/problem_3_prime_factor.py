"""
The prime factors of 13195 are 5, 7, 13 and 29.

What is the largest prime factor of the number 600851475143 ?
"""

def prime_gen():
    from itertools import count
    primes = []
    yield 2
    for n in count(3,2):
        comp = False
        for p in primes:
            if not n % p:
                comp = True
                break
            elif p ** 2 > n:
                break
        if not comp:
            primes.append(n)
            yield n

def prime_factorial(number):
    fact = []
    while number >= 2:
        # print number
        g = prime_gen()
        for i in g:
            # print i
            if not number % i:
                fact.append(i)
                number = number / i
                # print "after", number
                break
    return fact

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

# print "factorials", prime_factorial(13195)
