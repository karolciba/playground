#!/usr/bin/env python

import random
import sys
import string

number = int(sys.argv[1])

die = [1,2,3,4,5,6]

tosses = [ [(random.choice(die),random.choice(die)) for x in xrange(25)]  for x in xrange(number)]

# print tosses[0]

pairsixoccured = sum([ 1 for x in tosses if (6,6) in x ])

# print sixoccured
ratio = float(pairsixoccured)/len(tosses)

print "For %d tosses pair of six occured %d times with ratio %f" % (number,pairsixoccured,ratio)
