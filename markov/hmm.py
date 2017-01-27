#!/usr/bin/env python
""" Exercices on HMM, inference and learning

    References:
    [1] http://bozeman.genome.washington.edu/compbio/mbt599_2006/rabiner.pdf
    [2] http://bozeman.genome.washington.edu/compbio/mbt599_2006/hmm_scaling_revised.pdf
    [3] http://alumni.media.mit.edu/~rahimi/rabiner/rabiner-errata/
    [4] http://crsouza.com/2010/03/23/hidden-markov-models-in-c/
    [5] http://crsouza.com/2010/03/24/hidden-markov-model-based-sequence-classifiers-in-c/
    [6] https://www.youtube.com/watch?v=7KGdE2AK_MQ&list=PLD0F06AA0D2E8FFBA&index=95
    [7] https://www.youtube.com/playlist?list=PLQ-85lQlPqFPnk31Uut2ajVkBvlFmMtdx
"""

from __future__ import division

from collections import namedtuple
import numpy as np

Model = namedtuple('Model', 'transitions emissions initial')
transitions = np.array([ [ 0.7, 0.1, 0.1, 0.1 ],
                [ 0.1, 0.7, 0.1, 0.1 ],
                [ 0.1, 0.1, 0.7, 0.1 ],
                [ 0.1, 0.1, 0.1, 0.7 ] ])
emissions = np.array([ [ 0.495, 0.495, 0.01 ],
              [ 0.795, 0.195, 0.01 ],
              [ 0, 0, 1],
              [ 0.33, 0.33, 0.34 ]])
initial = np.array([ 0.25, 0.25, 0.25, 0.25 ])
# transitions = np.array([ [ 0.8, 0.2 ],
#                          [ 0.2, 0.8 ] ])
# emissions = np.array([ [ 0.5, 0.5 ],
#                        [ 0.8, 0.2 ] ])
# initial = np.array([ 0.5, 0.5 ])

crooked_casino = Model(transitions, emissions, initial)

def random_model(states_count, symbols_count):
    """ Return randomly initialized model with states_count number of states and symbols_count number of emissed symbols"""
    # random arrays
    transitions = np.random.random((states_count,states_count))
    emissions = np.random.random((states_count,symbols_count))
    initial = np.random.random(states_count)

    # normalize arrays row wise
    transitions_sums = np.sum(transitions, axis=1)
    transitions /= transitions_sums[:,None]

    emissions_sums = np.sum(emissions, axis=1)
    emissions /= emissions_sums[:,None]

    initial_sums = np.sum(initial)
    initial /= initial_sums

    return Model(transitions, emissions, initial)

def random_model_like(model):
    return random_model( len(model.initial), len(model.emissions[0]))

train_model = random_model_like(crooked_casino)

def synthetic(model = crooked_casino, verbose = False):
    import random
    from numpy.random import choice

    states = xrange(len(model.initial))
    observations = xrange(len(model.emissions[0]))

    state = choice(states, p=model.initial)

    VerboseRecord = namedtuple('VerboseRecord', 'emissions state')

    while True:
        emis = choice(observations, p=model.emissions[state])
        if verbose:
            yield VerboseRecord(emis, state)
        else:
            yield emis
        state = choice(states, p=model.transitions[state])

def denumerate(iter, start=-1):
    """denumerate(iterable[, start]) -> iterator for index, value for iterable"

    Reversed enumerator yelding elements from iterator along with index couting down"""
    from itertools import count, izip

    return izip(count(start, -1), iter)

def alpha(observations, model, normalized = True):
    transitions = model.transitions
    emissions = model.emissions
    initial = model.initial

    # ensure numpy array
    observations = np.array(observations)

    states_no = len(initial)

    # egde case for dynamic algorithm,
    a = np.empty((states_no, len(observations)))
    for state in xrange(states_no):
        a[state,0] = emissions[state,observations[0]] * initial[state]
    # normalize this step to obtain pseudo-probability
    if normalized:
        a[:,0] /= np.sum(a[:,0])

    for i,o in enumerate(observations[1:],1):
        # TODO: numpy'ize this?
        for state in xrange(states_no):
            a[state,i] = sum(a[prev_state,i-1] * transitions[prev_state,state] for prev_state in xrange(states_no)) * emissions[state,o]

        # normalize this step to obtain pseudo-probability
        if normalized:
            a[:,i] /= np.sum(a[:,i])

    return a

def beta(observations, model):
    transitions = model.transitions
    emissions = model.emissions
    initial = model.initial

    # ensure numpy array
    observations = np.array(observations)

    states_no = len(initial)

    b = np.empty((states_no, len(observations)))

    # edge case for dynamic algorithm
    b[:,-1] = 1.0/states_no

    for i,o in denumerate(reversed(observations[1:]),len(observations)-2):
        # TODO: numpy'ize this?
        for state in xrange(states_no):
            b[state,i] = sum(transitions[state,next_state] * emissions[next_state,o] * b[next_state,i+1] for next_state in xrange(states_no))

        # normalize this step to obtain pseudo-probability
        b[:,i] /= np.sum(b[:,i])

    return b


def observation_probability(observation, model):
    """Calculates probability of observation given model"""
    a = alpha(observation, model, normalized = False)
    return np.sum(a[:,-1])

def probabilities(model, order = 3):
    from itertools import product
    symbols_no = len(model.emissions[0])
    obs = list(product(range(symbols_no), repeat=order))
    return [ (o,observation_probability(o,model)) for o in obs ]

def model_similarity(first, second, order = 3):
    from itertools import product
    symbols_no = len(first.emissions[0])
    obs = list(product(range(symbols_no), repeat=order))
    first_scores = [ observation_probability(o,first) for o in obs ]
    second_scores = [ observation_probability(o,second) for o in obs ]
    deltas = [ abs(x - y) for x,y in zip(first_scores,second_scores) ]
    # deltas = [ x - y for x,y in zip(first_scores,second_scores) ]

    return list(zip(first_scores, second_scores, deltas)), sum(deltas)

def ksi_gamma(observations, model):
    transitions = model.transitions
    emissions = model.emissions
    initial = model.initial

    a = alpha(observations, model)
    b = beta(observations, model)

    states_no = len(initial)

    k = np.empty((states_no,states_no,len(observations)-1))
    g = np.empty((states_no,len(observations)-1))

    for i,o in enumerate(observations[1:],0):
        s = 0.0
        for fro in xrange(states_no):
            ss = 0.0
            for to in xrange(states_no):
                k[fro,to,i] = a[fro,i]*transitions[fro,to]*b[to,i+1]*emissions[to,o]
                s += k[fro,to,i]
                ss += k[fro,to,i]
            g[fro,i] = ss
        for fro in xrange(states_no):
            for to in xrange(states_no):
                k[fro,to,i] /= s
        g[:,i] /= np.sum(g[:,i])

    return k, g

def baum_welch(observations, model):
    k, g = ksi_gamma(observations, model)

    import copy
    new_model = copy.deepcopy(model)
    eta = 0.001

    transitions = new_model.transitions
    emissions = new_model.emissions
    initial = new_model.initial

    states_no = len(initial)

    # sum probabilies being in each state
    initial = np.sum(g, axis=1)
    # normalize
    # initial = g[:,0]

    initial[ initial == 0 ] = eta
    initial /= np.sum(initial)
    new_model.initial[:] = initial[:]

    for fro in xrange(states_no):
        for to in xrange(states_no):
            transitions[fro,to] = sum(k[fro,to,:-1])/sum(g[fro,:-1])

    for state in xrange(states_no):
        for e in xrange(len(emissions[0])):
            nom = 0.0
            for i in xrange(len(observations)-1):
                if observations[i] == e:
                    nom += g[state,i]
            emissions[state,e] = nom/sum(g[state,:])

    # smooth
    # normalize arrays row wise
    transitions[ transitions == 0 ] = eta
    transitions_sums = np.sum(transitions, axis=1)
    transitions /= transitions_sums[:,None]

    emissions[ emissions == 0] = eta
    emissions_sums = np.sum(emissions, axis=1)
    emissions /= emissions_sums[:,None]

    return new_model
    import pdb; pdb.set_trace()

def train(cycles, obs_len, train_model = None):
    if not train_model:
        train_model = random_model(4,3)
    # train_model = random_model(2,3)
    if cycles > 0:
        it = xrange(cycles)
    else:
        from itertools import count
        it = count()
    for cycle in it:
        print ""
        print "cycle", cycle
        g = synthetic()
        o = [ g.next() for x in xrange(obs_len) ]
        model = baum_welch(o, train_model)
        print ""
        print "before"
        print "trainsitions\n", train_model.transitions
        print "emissions\n", train_model.emissions
        print "initial\n", train_model.initial
        print ""
        print "after"
        print "trainsitions\n", model.transitions
        print "emissions\n", model.emissions
        print "initial\n", model.initial
        # import pdb; pdb.set_trace()
        t_delta = np.sum(train_model.transitions.flatten() * model.transitions.flatten())
        t_delta /= np.linalg.norm(train_model.transitions.flatten())
        t_delta /= np.linalg.norm(model.transitions.flatten())
        e_delta = np.sum(train_model.emissions.flatten() * model.emissions.flatten())
        e_delta /= np.linalg.norm(train_model.emissions.flatten())
        e_delta /= np.linalg.norm(model.emissions.flatten())
        i_delta = np.sum(train_model.initial.flatten() * model.initial.flatten())
        i_delta /= np.linalg.norm(train_model.initial.flatten())
        i_delta /= np.linalg.norm(model.initial.flatten())
        print ""
        print "deltas"
        print "transitions\n", t_delta
        print "emissions\n", e_delta
        print "initial\n", i_delta
        # delta = np.hstack( (t_delta.flatten(), e_delta.flatten(), i_delta))
        train_model = model
        # print "norm", np.linalg.norm(delta)
    print ""
    print "target"
    print "trainsitions", crooked_casino.transitions
    print "emissions", crooked_casino.emissions
    print "initial", crooked_casino.initial

    return train_model

def ksi_gamma_wrapper(params):
    obs, model = params
    return ksi_gamma(obs, model)

from multiprocessing import Pool
pool = None

def batch_baum_welch(observations_list, model):

    ksis_gammas = pool.map(ksi_gamma_wrapper, [ [obs, model] for obs in observations_list ])
    ksis = [ x[0] for x in ksis_gammas ]
    gammas = [ x[1] for x in ksis_gammas ]

    import copy
    new_model = copy.deepcopy(model)

    transitions = new_model.transitions
    emissions = new_model.emissions
    initial = new_model.initial

    states_no = len(initial)

    # sum probabilies being in each state
    initial = np.sum(gammas[0], axis=1)
    # normalize
    # initial = g[:,0]

    initial /= np.sum(initial)
    new_model.initial[:] = initial[:]

    for fro in xrange(states_no):
        for to in xrange(states_no):
            noms = [ sum(k[fro,to,:-1]) for k in ksis ]
            denoms = [ sum(g[fro,:-1]) for g in gammas ]
            transitions[fro,to] = sum(noms)/sum(denoms)

    for state in xrange(states_no):
        for e in xrange(len(emissions[0])):
            nom = 0.0
            for observations,g in zip(observations_list, gammas):
                for i in xrange(len(observations)-1):
                    if observations[i] == e:
                        nom += g[state,i]
            denoms = [ sum(g[state,:]) for g in gammas ]
            emissions[state,e] = nom/sum(denoms)
    return new_model

def batch_train(cycles, obs_len, batch_size):
    global pool
    pool = Pool()
    for cycle in xrange(cycles):
        print ""
        print "cycle", cycle
        g = synthetic()
        o = [ [ g.next() for x in xrange(obs_len) ] for y in range(batch_size) ]
        global train_model
        model = batch_baum_welch(o, train_model)
        print ""
        print "before"
        print "trainsitions", train_model.transitions
        print "emissions", train_model.emissions
        print "initial", train_model.initial
        print ""
        print "after"
        print "trainsitions", model.transitions
        print "emissions", model.emissions
        print "initial", model.initial
        # import pdb; pdb.set_trace()
        t_delta = train_model.transitions - model.transitions
        e_delta = train_model.emissions - model.emissions
        i_delta = train_model.initial - model.initial
        print ""
        print "deltas"
        print "transitions", t_delta
        print "emissions", e_delta
        print "initial", i_delta
        delta = np.hstack( (t_delta.flatten(), e_delta.flatten(), i_delta))
        train_model = model
        print "norm", np.linalg.norm(delta)

    return train_model
    pool.close()
    print ""
    print "target"
    print "trainsitions", crooked_casino.transitions
    print "emissions", crooked_casino.emissions
    print "initial", crooked_casino.initial
