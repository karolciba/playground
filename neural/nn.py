#!/usr/bin/env python

import numpy as np

def sigmoid(x):
    return 1/(1+np.exp(-x))

def d_sigmoid(x):
    return x*(1-x)

def tanh(x):
    return np.tanh(x)

def d_tanh(x):
    return 1.0 - np.tanh(x)**2

nonlin = sigmoid
d_nonlin =d_sigmoid

# nonlin = tanh
# d_nonlin = d_tanh

def X(i):
    return np.random.randint(2, size=2)

def f_or(x):
    return 1 if x[0] == 1 or x[1] == 1 else 0

def f_nor(x):
    return 1 if x[0] == 0 and x[1] == 0 else 0

def f_and(x):
    return 1 if x[0] == 1 and x[1] == 1 else 0

def f_nand(x):
    return 1 if x[0] == 0 or x[1] == 0 else 0

def f_xor(x):
    return 1 if (x[0] == 1 and x[1] == 0) or (x[0] == 0 and x[1] == 1) else 0

def f_xnor(x):
    return 0 if (x[0] == 1 and x[1] == 0) or (x[0] == 0 and x[1] == 1) else 1

Y = f_nand

def bias(x):
    return np.append(x.flatten(),1)

hid0 = 2*np.random.random((3,)) - 2

iterations = 10000

import pdb

for i in xrange(iterations):

    x = X(i)

    l0 = bias(x)

    l1 = np.dot(l0,hid0)

    a1 = nonlin(l1)

    l1_error = Y(x) - a1

    l1_delta = l1_error * d_nonlin(a1)

    hid0 += l0 * l1_delta

    if i%100 == 0:
        print l0, l1, a1, l1_error, l1_delta, hid0
    # pdb.set_trace()


print "After training"
x = np.array([[0, 0, 1],
              [0, 1, 1],
              [1, 0, 1],
              [1, 1, 1]])

l1 = np.dot(x,hid0)

a1 = nonlin(l1)

print x, a1
