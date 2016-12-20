#!/usr/bin/env python

import numpy as np
np.random.seed(1)

def sigmoid(x, deriv=False):
    if (deriv):
        return x*(1-x)
    return 1/(1+np.exp(-x))

def softplus(x, deriv=False):
    if deriv:
        return 1/(1 + np.exp(-x))
    return np.log(1 + np.exp(x))

def tanh(x, deriv=False):
    if deriv:
        return 1.0 - np.tanh(x)**2
    return np.tanh(x)

nonlin = softplus

x = np.array([[0, 0, 1],
              [0, 1, 1],
              [1, 0, 1],
              [1, 1, 1]])

y = np.array([[0,1,1,1]]).T

hid = 2*np.random.random((3,1)) - 1

iterations = 10000
weights = np.zeros((3, iterations))
errors = np.zeros((4, iterations))

debug = False
# import pdb; pdb.set_trace()

for i in xrange(iterations):

    # forward
    l0 = x
    # pass it thru layer
    l1 = np.dot(l0, hid)

    # apply nolinearyti
    nl1 = nonlin(l1)

    # calc error
    l1_error = y - nl1

    # backpropagate
    l1_delta = l1_error * nonlin(nl1, True)

    # apply
    hid += np.dot(l0.T, l1_delta)

    weights[:,i] = hid.copy().flatten()
    errors[:,i] = l1_error.copy().flatten()
    # import pdb; pdb.set_trace()

    if debug:
        print "l0", l0
        print "l1", l1
        print "nl1", nl1
        print "l1_error", l1_error
        print "l1_delta", l1_delta
        print "hid", hid

import matplotlib.pyplot as plt
plt.plot(errors.T)
plt.title("error")
plt.show(block=True)

plt.plot(weights.T)
plt.title("weights")
plt.show()

print ""
print "After learning"
print hid

print "Out"
print nl1
