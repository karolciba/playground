#!/usr/bin/env python

import random
import sys
import string
from itertools import count

number = 40
if len(sys.argv) > 1:
    number = int(sys.argv[1])

def simulate():
    plays = 40
    tosses = (random.choice('HT') for x in xrange(plays))

    def toss():
        for x in count():
            yield random.choice('HT')

    score = 0
    lead = "peter"
    leading = []

    for i,x in enumerate(tosses,1):
        if x == "H":
            score += 1
        else:
            score -= 1

        if lead == "peter" and score < 0:
            lead = "paul"
        elif lead == "paul" and score > 0:
            lead = "peter"

        # print i,x, score, lead
        leading.append(lead)

    return score,sum( 1 for x in leading if x == 'peter')


# from numpy import histogram

def crappyhist(a, bins):
    '''Draws a crappy text-mode histogram of an array'''
    import numpy as np
    import string
    from math import log10

    h,b = np.histogram(a, bins)

    for i in range (0, bins-1):
        print string.rjust(`b[i]`, 7)[:int(log10(
                   np.amax(b)))+5], '| ', '#'*int(70*h[i-1]/np.amax(h))

    print string.rjust(`b[bins]`, 7)[:int(log10(np.amax(b)))+5]


def display():
    import os
    os.system('clear')
    print "Scores hist",max(scores),min(scores)
    scores_hist = crappyhist(scores,21)

    print "Leads hist",max(leads),min(leads)
    leads_hist = crappyhist(leads,21)

scores = []
leads = []
for x in xrange(number):
    score, lead = simulate()
    scores.append(score)
    leads.append(lead)
    # if x % 10000 == 0:
    #     display()
    #     print "Iteration %d" % (x)

# print scores,leads
