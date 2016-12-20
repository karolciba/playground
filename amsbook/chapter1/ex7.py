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

def simulate(number):
    redblack = [ 1 if random.choice(wheel).color == COLORS.red else -1 for x in xrange(number) ]

    field = [ 36 if int(random.choice(wheel).number) == 17 else -1 for x in xrange(number) ]

    acc_redblack = accumulate(redblack)

    acc_field = accumulate(field)
    return acc_redblack, acc_field

import matplotlib.pyplot as plt

acc_redblack, acc_field = simulate(number)

plt.ioff()
plt.clf()
# plt.plot(redblack)
plt.plot(acc_redblack)
# plt.plot(field)
plt.plot(acc_field)

plt.draw()

plt.show()


