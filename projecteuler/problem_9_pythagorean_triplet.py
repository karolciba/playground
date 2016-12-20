"""
a < b < c

a + b + c = 1000
a**2 + b**2 = c**2

c = 1000 - a - b
"""

def triplet():
    for c in xrange(1,1001):
        for b in xrange (1,c):
            for a in xrange(1,b):
                if a + b + c == 1000 and a**2 + b**2 == c**2:
                    return a*b*c

def otriplet():
    for a in xrange(0,1000):
        for b in xrange (0,1000):
            if b > a:
                break
            if a**2+b**2 == (1000 - a - b)**2:
                return a*b*(1000-a-b)



def oftriplet():
    g = ( (a,b,c) for c in xrange(1,1001) for b in xrange(1,c) for a in xrange(1,b) if a + b + c == 1000 and a**2 + b**2 == c**2)
    a,b,c = next(g)
    return a*b*c

def ftriplet():
    g = ( (a,b,c) for a in xrange(1,1001) for b in xrange(1,1001) for c in xrange(1,1001) if a < b < c and a + b + c == 1000 and a**2 + b**2 == c**2)
    a,b,c = next(g)
    return a*b*c
