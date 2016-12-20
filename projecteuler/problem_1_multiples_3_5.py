def loop():
    s = 0
    for i in range(1000):
        if i % 3 == 0 or i % 5 == 0:
            s += i
    return s

def setgen():
    s3 = set(x for x in xrange(1000) if x % 3 == 0)
    s5 = set(x for x in xrange(1000) if x % 5 == 0)
    s = s3 | s5
    return sum(s)

def func():
    return sum(x for x in xrange(1000) if x % 3 == 0 or x % 5 == 0)
