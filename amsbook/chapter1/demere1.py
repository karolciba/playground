#!/usr/bin/env python

import random
import sys
import string

number = int(sys.argv[1])

die = [1,2,3,4,5,6]

tosses = [ [random.choice(die) for x in xrange(4)]  for x in xrange(number)]

# print tosses

sixoccured = sum([ 1 for x in tosses if 6 in x ])

# print sixoccured
ratio = float(sixoccured)/len(tosses)

print "For %d tosses six occured %d times with ratio %f" % (number,sixoccured,ratio)
