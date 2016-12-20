#!/usr/bin/env python

import random
import sys


number = 100
if len(sys.argv) > 1:
    number = int(sys.argv[1])


larger = 45
smaller = 15


sims = []

for x in xrange(number):
    boys_larger = []
    boys_smaller = []

    for x in xrange(365):
        l = [ 1 for x in xrange(larger) if random.random() > 0.5 ]
        s = [ 1 for x in xrange(smaller) if random.random() > 0.5 ]

        boys_larger.append(sum(l))
        boys_smaller.append(sum(s))

    # print sum(1 for x in boys_larger if x >= 0.6 * larger), sum(1 for x in boys_smaller if x >= 0.6 * smaller)
    ratio_larger = [ float(x)/larger for x in boys_larger ]
    ratio_smaller = [ float(x)/smaller for x in boys_smaller ]

    test_larger = [ 1 for x in ratio_larger if x >= 0.6 ]
    test_smaller = [ 1 for x in ratio_smaller if x >= 0.6 ]

    # import pdb; pdb.set_trace()

    sims.append( (sum(test_larger), sum(test_smaller) ) )

    print "larger", sum(test_larger), "smaller", sum(test_smaller)
