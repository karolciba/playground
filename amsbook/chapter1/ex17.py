#!/usr/bin/env python

import random
import sys

import numpy as np
import matplotlib.pyplot as plt

number = 100
if len(sys.argv) > 1:
    number = int(sys.argv[1])

def asim(_):
    edge = 10000

    from random import choice as c
    dirs = [-1, 1]

    pos = 0
    pos += c(dirs)
    steps = 1
    while pos != 0:
        steps += 1
        pos += c(dirs)
        if pos > edge or pos < -edge:
            print "Fell over world's edge"
            return -1

    return steps

def a(number):

    out = []
    print "Simulation"
    from multiprocessing import Pool

    p = Pool()
    out = p.map(asim, range(number))
    p.close()
    # print out

    # for x in xrange(number):
    #     print '\r', x,
    #     out.append(sim())
    # else:
    #     print ""

    print "Drawing histogram"
    fallen = sum(1 for x in out if x == -1)
    tot = len(out)
    print "Fallen", fallen, "out of", tot, "ratio", float(fallen)/tot
    # hist, _ = np.histogram(out)
    plt.hist(out,100)
    plt.show()

def bsim(_):
    edge = 10000

    from random import choice as c
    dirs = [-1, 1]
    def r():
        return (c(dirs),c(dirs))

    x = 0
    y = 0
    x += c(dirs)
    y += c(dirs)
    # pos = [0,0]
    # pos = [ sum(x) for x in zip(pos,r()) ]
    steps = 1
    while x != 0 or y != 0:
        steps += 1
        # pos = [ sum(x) for x in zip(pos,r()) ]
        x += c(dirs)
        y += c(dirs)
        # print '\r', _, steps, x, y,
        if x > edge or x < -edge or y > edge or y < -edge:
            print "Fell over world's edge", steps, x, y
            return -1

    return steps

def b(number):

    out = []
    from multiprocessing import Pool
    print "Simulation"
    p = Pool()
    out = p.map(bsim, range(number))
    p.close()
    # for x in xrange(number):
    #     print '\r', x,
    #     out.append(sim())
    # else:
    #     print ""

    print "Drawing histogram"
    fallen = sum(1 for x in out if x == -1)
    tot = len(out)
    print "Fallen", fallen, "out of", tot, "ratio", float(fallen)/tot
    # hist, _ = np.histogram(out)
    plt.hist(out,100)
    plt.show()

def csim(_):
    edge = 10000

    from random import choice as c
    dirs = [-1, 1]
    def r():
        return (c(dirs),c(dirs))

    x = 0
    y = 0
    z = 0
    x += c(dirs)
    y += c(dirs)
    z += c(dirs)
    # pos = [0,0]
    # pos = [ sum(x) for x in zip(pos,r()) ]
    steps = 1
    while x != 0 or y != 0 or z != 0:
        steps += 1
        # if steps > 10000000:
        #     return -1
        # pos = [ sum(x) for x in zip(pos,r()) ]
        x += c(dirs)
        y += c(dirs)
        z += c(dirs)
        # print '\r', _, steps, x, y, z,
        if x > edge or x < -edge or y > edge or y < -edge or z > edge or z < -edge:
            print "Fell over world's edge", steps, x, y, z
            return -1

    return steps

def c(number):

    out = []
    from multiprocessing import Pool
    print "Simulation"
    p = Pool()
    out = p.map(csim, range(number))
    p.close()
    # for x in xrange(number):
    #     print '\r', x,
    #     out.append(sim())
    # else:
    #     print ""

    print "Drawing histogram"
    fallen = sum(1 for x in out if x == -1)
    tot = len(out)
    print "Fallen", fallen, "out of", tot, "ratio", float(fallen)/tot
    # hist, _ = np.histogram(out)
    plt.hist(out,1000)
    plt.show()
