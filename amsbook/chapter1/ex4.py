#!/usr/bin/env python

import random
import sys


number = 100
if len(sys.argv) > 1:
    number = int(sys.argv[1])

def raquet(prob_win_serving = 0.6, prob_win_defend = 0.5, volley = False):
    player = 0
    opponent = 0
    serving = 'player'
    while player < 21 and opponent < 21:
        # print "Player", player, "opponent", opponent
        if serving == 'player':
            won = random.random() <= prob_win_serving
            if won:
                # print "Serving", serving, "won"
                player += 1
            else:
                # print "Serving", serving, "lost"
                if volley: opponent += 1
                serving = 'opponent'
        else:
            won = random.random() <= prob_win_defend
            if won:
                # print "Serving", serving, "won"
                if volley: player += 1
                serving = 'player'
            else:
                # print "Serving", serving, "lost"
                opponent += 1

    return 1 if player == 21 else 0

wons = [ raquet(0.6,0.4,True) for x in xrange(number) ]

print "Player won %d times, ratio %f" % (sum(wons), sum(wons)/float(number))
