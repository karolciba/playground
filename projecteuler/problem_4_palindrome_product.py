from itertools import *

digit3 = xrange(999, 100, -1)


multip = (x*y for x,y in product(digit3,digit3))

pal = (x for x in multip if str(x) == str(x)[::-1])

maxpal = max(pal)

print maxpal
