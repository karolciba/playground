#!/usr/bin/env python

import pycuda.driver as drv
import pycuda.tools
import pycuda.autoinit
from pycuda.compiler import SourceModule
import numpy as np
import hmm

mod = SourceModule(open('hmm.cu','r').read())

alpha_norm = mod.get_function('alpha_norm')
beta_norm = mod.get_function('beta_norm')

transitions = np.array([ [ 0.5, 0.5, 0.1 ],
                         [ 0.2, 0.8, 0.1 ],
                         [ 0.3, 0.3, 0.4 ]]).astype(np.float32)
emissions = np.array([ [ 0.8, 0.2, 0.1 ],
                       [ 0.6, 0.4, 0.1 ],
                       [ 0.1, 0.2, 0.7 ]]).astype(np.float32)
initial = np.array([ 0.33, 0.5, 0.2 ]).astype(np.float32)

transitions = np.array([ [ 0.5, 0.5 ],
                         [ 0.2, 0.8 ] ]).astype(np.float32)
emissions = np.array([ [ 0.5, 0.5 ],
                       [ 0.8, 0.2 ] ]).astype(np.float32)
initial = np.array([ 0.5, 0.5 ]).astype(np.float32)

states = 2;
symbols = 2;
observations = 10
obs = np.random.randint(symbols,size=10).astype(np.int32)

# dest = np.zeros((states,observations),order='F').astype(np.float32)
alpha = np.zeros((observations,states)).astype(np.float32)
beta = np.zeros((observations,states)).astype(np.float32)
#
#
shared_len = 4;

alpha_norm(drv.Out(alpha), np.int32(states), np.int32(symbols), np.int32(observations), drv.In(transitions), drv.In(emissions), drv.In(initial), drv.In(obs), block=(10,1,1), grid=(1,1), shared=shared_len)
#
print("Alpha Cuda calc");
print(alpha)

print("Alpha Python calc");
print(hmm.alpha(obs,hmm.crooked_casino,True).T)

print("Observations",obs)

beta_norm(drv.Out(beta), np.int32(states), np.int32(symbols), np.int32(observations), drv.In(transitions), drv.In(emissions), drv.In(initial), drv.In(obs), block=(10,1,1), grid=(1,1), shared=shared_len)
#
print("Beta Cuda calc");
print(beta)
print("Beta Python calc");
print(hmm.beta(obs,hmm.crooked_casino, False).T)
print("Observations",obs)
