#!/usr/bin/env python

import random
import sys
import string

number = int(sys.argv[1])

tosses = string.join([random.choice('HT') for x in xrange(number)], '')

heads = sum([ 1 for x in tosses if x == 'H'])
tails = sum([ 1 for x in tosses if x == 'T'])


print "Heads %d Tails %d ratio %f" % (heads, tails, float(heads)/(heads + tails))

