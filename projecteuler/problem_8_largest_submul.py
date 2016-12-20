s = "7316717653133062491922511967442657474235534919493496983520312774506326239578318016984801869478851843858615607891129494954595017379583319528532088055111254069874715852386305071569329096329522744304355766896648950445244523161731856403098711121722383113622298934233803081353362766142828064444866452387493035890729629049156044077239071381051585930796086670172427121883998797908792274921901699720888093776657273330010533678812202354218097512545405947522435258490771167055601360483958644670632441572215539753697817977846174064955149290862569321978468622482839722413756570560574902614079729686524145351004748216637048440319989000889524345065854122758866688116427171479924442928230863465674813919123162824586178664583591245665294765456828489128831426076900422421902267105562632111110937054421750694165896040807198403850962455444362981230987879927244284909188845801561660979191338754992005240636899125607176060588611646710940507754100225698315520005593572972571636269561882670428252483600823257530420752963450"
l = [ int(c) for c in s ]

from operator import mul
from itertools import count
from itertools import chain
from functools import partial
from itertools import imap
import random
import string

# ss = ''.join(random.choice(string.digits) for _ in range(10000))
ll = [ random.choice([1,2,3,4,5,6,7,8,9]) for _ in range(10000) ]

def brute(ints, length):
    muls = []
    for i in xrange(len(ints)-length):
        ll = ints[i:i+length]
        m = reduce(mul, ll)
        muls.append(m)

    return max(muls)

def func(ints, length):
    parts = (ints[x:x+length] for x in xrange(len(ints) - length))
    fil = [ part for part in parts if 0 not in part ]
    mulred = partial(reduce, mul)
    muls = imap( mulred, fil )

    return max( chain(muls,[0]) )


prod_cache = {}
def prod(ints):
    # ints.sort()
    # import pdb; pdb.set_trace()
    # actually, sorting slowes this a lot
    # orig = list(ints)
    # ints.sort()
    # speeds up 4 times
    if 0 in ints:
        return 0
    t = tuple(ints)
    if t in prod_cache:
        return prod_cache[t]
    size = len(t)
    if size == 1:
        prod_cache[t] = t[0]
        return t[0]
    # left = ints[:size/2]
    # right = ints[size/2:]
    # m = prod(left) * prod(right)
    last = ints.pop()
    m = prod(ints) * last
    prod_cache[t] = m
    return m

def dyn(ints, length):
    prod_cache = {}
    parts = (ints[x:x+length] for x in xrange(len(ints) - length))
    muls = [ prod(part) for part in parts ]
    return max(muls)


# print func(l,13)

