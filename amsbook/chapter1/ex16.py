#!/usr/bin/env python

import random
import sys

number = 100
if len(sys.argv) > 1:
    number = int(sys.argv[1])

def boygen():
    genders = ['B', 'G']
    g = random.choice(genders)
    yield g
    while g != 'B':
        g = random.choice(genders)
        yield g
    raise StopIteration

def pairgen():
    genders = ['B', 'G']
    boy = False
    girl = False
    while not boy or not girl:
        g = random.choice(genders)
        if g == 'B':
            boy = True
        if g == 'G':
            girl = True
        yield g
    raise StopIteration

def orderedpairgen():
    genders = ['B', 'G']
    boy = False
    girl = False
    while not boy or not girl:
        g = random.choice(genders)
        if g == 'B':
            boy = True
        if boy == True and g == 'G':
            girl = True
        yield g
    raise StopIteration

def anypairgen():
    genders = ['B', 'G']
    boys = 0
    girls = 0
    while boys < 2 and girls < 2:
        g = random.choice(genders)
        if g == 'B':
            boys += 1
        if g == 'G':
            girls += 1
        yield g
    raise StopIteration

def twoboysgen():
    genders = ['B', 'G']
    boys = 0
    while boys < 2:
        g = random.choice(genders)
        if g == 'B':
            boys += 1
        yield g
    raise StopIteration

def stats(gen = boygen, number = 1000):
    lengths = []
    for x in xrange(number):
        s = sum(1 for x in gen())
        lengths.append(s)


    import matplotlib.pyplot as plt

    m = max(lengths)
    plt.hist(lengths, bins = m)
    plt.show()

    return sum(lengths)/float(len(lengths)), max(lengths)
