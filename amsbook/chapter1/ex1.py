#!/usr/bin/env python

import sys
import string

number = 1000
if len(sys.argv) > 1:
    number = int(sys.argv[1])

def coingen(max = None):
    from itertools import count
    import random
    for x in count():
        yield random.choice('HT')
        if max and x == max:
            raise StopIteration

heads = 0
for i,x in enumerate(coingen(number),1):
    if x == 'H':
        heads += 1
    if i % 1000 == 0:
        # print heads, i
        print '\r', i, (float(heads)/i - 0.5), (heads - i/2),


print ""
print i, (float(heads)/i - 0.5), (heads - i/2)
