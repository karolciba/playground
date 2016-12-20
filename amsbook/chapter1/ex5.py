#!/usr/bin/env python

import random
import sys


number = 1000
if len(sys.argv) > 1:
    number = int(sys.argv[1])

def throwthree():
    dice = [1,2,3,4,5,6]
    return [random.choice(dice) for x in xrange(3)]

def any(list,test):
    for el in list:
        if el == test:
            return True
    return False

no_tests = 20000
probs = []

tests = [[throwthree() for x in xrange(2*number)] for y in xrange(no_tests)]

def lists():
    probs = []
    for no_of_throws in xrange(1,number+1):
        experiment = [ x[0:no_of_throws] for x in tests ]
        sixes = [ x for x in experiment if [6,6,6] in x ]
        occurences = len(sixes)
        ratio = float(occurences)/no_tests
        probs.append(ratio)
    return probs

def genlen(gen):
    l = 0
    for _ in gen:
        l += 1
    return l

def gens():
    probs = []
    for no_of_throws in xrange(1,number+1):
        experiment = (x[no_of_throws:2*no_of_throws] for x in tests)
        sixes = (1 for x in experiment if [6,6,6] in x)
        occurences = sum(sixes)
        ratio = float(occurences)/no_tests
        probs.append(ratio)
    return probs

# def regens():
#     probs = []
#     for no_of_throws in xrange(1,number+1):
#         experiment = ((throwthree() for x in xrange(no_of_throws)) for y in xrange(no_tests))
#         sixes = (1 for x in experiment if [6,6,6] in x)
#         occurences = sum(sixes)
#         ratio = float(occurences)/no_tests
#         probs.append(ratio)
#     return probs

# for no_of_throws in xrange(1,number+1):
#     occurences = 0
#     for x in xrange(tests):
#         throws = [throwthree() for x in xrange(no_of_throws)]
#         sixes = [x for x in throws if [6,6,6] == x]
#         if len(sixes) > 0:
#             # import pdb; pdb.set_trace()
#             occurences += 1
#     probs.append(float(occurences)/tests)

# probs = gens()
# print list(enumerate(probs,1))
#
# from matplotlib import pyplot as plt
# plt.plot(probs)
# plt.show()

