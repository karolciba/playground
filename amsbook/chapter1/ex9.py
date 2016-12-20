#!/usr/bin/env python

import random
import sys


number = 100
if len(sys.argv) > 1:
    number = int(sys.argv[1])

def accumulate(list):
    acu = 0
    out = []
    for el in list:
        acu += el
        out.append(acu)
    return out

numbers = [ '00' ]
numbers += [ str(x) for x in xrange(0,37) ]

from enum import Enum
COLORS = Enum('COLORS', 'green red black')

colors = [ COLORS.green, COLORS.green ]
# colors = [ COLORS.red, COLORS.black ]
colors += [ COLORS.red if x % 2 == 0 else COLORS.black for x in xrange(1,37) ]

from collections import namedtuple
pair = namedtuple('pair', 'number color')
wheel = [ pair(*x) for x in zip(numbers,colors) ]

def simulate():
    return random.choice(wheel)

sims = []
for x in xrange(number):
    labouchere = [1,2,3,4]
    wins = []
    bets = 0
    wons = 0
    for x in xrange(1000):
        # print "labouchere", labouchere
        s = simulate()
        first = labouchere.pop(0)
        last = labouchere.pop()
        bet = first + last
        bets += bet
        if s.color == COLORS.red:
            # print "won", bet
            wins.append(bet)
            wons += bet
        else:
            # print "lost", bet
            wins.append(-1*bet)
            wons -= bet
            labouchere.insert(0,first)
            labouchere.append(last)
            labouchere.append(bet)
        if len(labouchere) < 2:
            # print "wons", wons, "bets", bets
            sims.append(wons)
            if len(labouchere) == 1:
                print "only one left"
                # sims.append(labouchere.pop())
                pass
            else:
                print "take last win"
                pass
            break
    else:
        print "Never ended"
        # sims.append(sum(wins))

print sims
print sum(sims)
