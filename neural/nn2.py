#!/usr/bin/env python

import numpy as np

def sigmoid(x):
    return 1/(1+np.exp(-x))

def d_sigmoid(x):
    y = sigmoid(x)
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

Y = f_xor

def bias(x):
    return np.append(x.flatten(),1)

hid0 = 2*np.random.random((3,4)) - 2
hid1 = 2*np.random.random((4,)) - 2

iterations = 100000

import pdb

for i in xrange(iterations):
    # pdb.set_trace()

    x = X(i)

    l0 = bias(x)

    l1 = l0.dot(hid0)

    a1 = nonlin(l1)

    # l2 = np.dot(l1,hid1)
    l2 = a1.dot(hid1)

    a2 = nonlin(l2)


    l2_error = Y(x) - a2

    l2_delta = l2_error * d_nonlin(a2)

    l1_error = l2_delta * hid1

    l1_delta = l1_error * d_nonlin(a1)


    hid1 += a1 * l2_delta

    hid0 += np.array([l0, l0, l0, l0]).T * l1_delta

    # l1_error = Y(x) - a1
    #
    # l1_delta = l1_error * d_nonlin(a1)
    #
    # hid0 += l0 * l1_delta

    if i%10000 == 0:
        print "l0", l0, "l1", l1, "a1", a1, "l1_error", l1_error, "l1_delta", l1_delta, "hid0", hid0
        print "l2", l2, "a2", a2, "l2_error", l2_error, "l2_delta", l2_delta, "hid1", hid1
    # pdb.set_trace()


print "After training"
x = np.array([[0, 0, 1],
              [0, 1, 1],
              [1, 0, 1],
              [1, 1, 1]])

l1 = np.dot(x,hid0)

a1 = nonlin(l1)

l2 = np.dot(a1, hid1)

a2 = nonlin(l2)

print x, a1, a2, [Y(x[0]), Y(x[1]), Y(x[2]), Y(x[3])]
