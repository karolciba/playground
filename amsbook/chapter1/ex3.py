#!/usr/bin/env python

import random
import sys


number = 1000
if len(sys.argv) > 1:
    number = int(sys.argv[1])

def throwthree():
    dice = [1,2,3,4,5,6]
    return [random.choice(dice) for x in xrange(3)]

throws = [throwthree() for x in xrange(number)]

sumsto9 = [x for x in throws if sum(x) == 9]
sumsto10 = [x for x in throws if sum(x) == 10]

print "Sum to 9 %d sum to 10 %d" % (len(sumsto9), len(sumsto10))


combs = [ (x,y,z) for x in range(1,7) for y in range(1,7) for z in range(1,7) ]
