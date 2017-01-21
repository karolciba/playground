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

from enum import Enum

STATES = Enum('Coin', 'fair biased')
EMISSIONS = Enum('Toss', 'H T')

from collections import namedtuple
Parameters = namedtuple('Parameters','transitions emissions initial')

transitions = { STATES.fair: { STATES.fair: 0.3, STATES.biased: 0.7 },
                STATES.biased: { STATES.fair: 0.5, STATES.biased: 0.5 } }
# initial = { STATES.fair: 0.83, STATES.biased: 0.17 }
initial = { STATES.fair: 0.5, STATES.biased: 0.5 }
emissions = { STATES.fair: { EMISSIONS.H: 0.4, EMISSIONS.T: 0.6 },
                STATES.biased: { EMISSIONS.H: 0.8, EMISSIONS.T: 0.2 } }

crooked_casino = Parameters(transitions, emissions, initial)


def strtotoss(string):
    l = { 'H': EMISSIONS.H, 'T': EMISSIONS.T }
    return map(lambda x: l[x], string)

def strtocoins(string):
    l = { 'F': STATES.fair, 'B': STATES.biased }
    return map(lambda x: l[x], string)

def casino(parameters = crooked_casino):
    """Crooked casino generator, generates emissions (Head, Tail) acording to
    provided HMM model of Fair and Biased coin"""
    import random

    from collections import namedtuple
    record = namedtuple('Record', 'emission state')

    # TODO: reimplement as exercise
    from numpy.random import choice

    transitions = parameters.transitions
    emissions = parameters.emissions
    initial = parameters.initial

    state = choice(list(STATES), p=initial.values())

    while True:
        yield record(choice(emissions[state].keys(), p=emissions[state].values()), state)
        state = choice(transitions[state].keys(), p=transitions[state].values())

def mul(elements):
    m = 1
    for el in elements:
        m *= el
    return m

def prob_observation_state(x, pi, parameters = crooked_casino):
    transitions = parameters.transitions
    emissions = parameters.emissions
    initial = parameters.initial

    from itertools import tee, izip

    # pairs PIi and PIi+1
    state_i, state_i_next = tee(pi)
    state_i_next.next()
    # (PI1, PI2), (PI2,PI3), ... (PIn-1,PIn)
    trans = izip(state_i, state_i_next)
    # select transitions probabilities
    trans_coef = [ transitions[i][j] for i,j in trans ]
    # states path probability, initial prob * transitions
    # P(pi)
    state_prob = initial[pi[0]] * mul(trans_coef)

    # list of probabilities for observation i given state_i
    emiss_list = [ emissions[state][obs] for state,obs in zip(pi,x) ]
    # P(x|pi)
    emiss_prob = mul(emiss_list)

    # end probability is multiplication of pass probability
    # and emission probability
    # P(x,pi) = Pi(x|pi)*P(pi)
    return state_prob * emiss_prob

def dynamic_decode(experiment, parameters = crooked_casino):
    transitions = parameters.transitions
    emissions = parameters.emissions
    initial = parameters.initial

    from collections import defaultdict

    def weight(fro, to, emiss):
        """ weight of the edge from strate "fro" to state "to" multiplied
        by emisssion probability "emiss" at the destination state"""
        return transitions[fro][to] * emissions[to][emiss]

    # Forward pass
    scores = defaultdict(lambda: 1.0)
    scores[(-1,STATES.biased)] = initial[STATES.biased], None
    scores[(-1,STATES.fair)] = initial[STATES.fair], None
    # for state in list(STATE):
    #     scores[(state,0)] = 1.0 * emissions[state][experiment[0]]

    for i,o in enumerate(experiment):
        for state in list(STATES):
            # import pdb; pdb.set_trace()
            l = [ (scores[(i-1,s)][0]*weight(s,state,o), s) for s in list(STATES) ]
            print i,o,state,l,max(l, key= lambda x: x[0])
            scores[(i,state)] = max(l, key= lambda x: x[0])

    filtered = [ [ (k[1],v) for k,v in scores.items() if k[0] == index ] for index in xrange(len(experiment)) ]
    maxes = [ max(l, key=lambda x:x[1]) for l in filtered ]
    return maxes, scores

    return scores

def forward(observations, parameters = crooked_casino):
    transitions = parameters.transitions
    emissions = parameters.emissions
    initial = parameters.initial

    # P(state_i, observation_1:i)
    # for P(state_i | observation_1:i) normalize by sum of P(state_i, observation_1:i)
    scores = [ {} for x in range(len(observations)) ]

    scores[0] = { state: initial[state]*emissions[state][observations[0]] for state in list(STATES) }
    # nomalize border case
    # s = sum(v for v in scores[0].values())
    # scores[0] = { k: v/s for k,v in scores[0].items() }

    # P(state_i, observation_1:i) = SIGMA(state_i-1) P(o_i|state_i) * P(state_i
    # | state_i-1) * P(state_i-1, observation_1:i-1)
    for i,o in enumerate(observations[1:],1):
        for state in list(STATES):
            prev = 0.0
            for prev_state in list(STATES):
                prev += transitions[prev_state][state] * scores[i-1][prev_state]
            scores[i][state] = emissions[state][o] * prev
        # scale = sum(v for v in scores[i].values())
        # for state in list(STATES):
        #     scores[i][state] /= scale

    # f = scores
    # sums = [ sum (v for v in ff.values()) for ff in f ]
    # norm = [ { k:v/s for k,v in ff.items() } for ff,s in zip(f,sums) ]

    return scores

def backward(observations, parameters = crooked_casino):
    transitions = parameters.transitions
    emissions = parameters.emissions
    initial = parameters.initial

    scores = [ {} for x in range(len(observations)+1) ]

    # scores[-1] = { state: emission[state][observation[-1]] * transition[state
    scores[-1] = { state: 1.0 for state in list(STATES) }

    # P(observation_i+1 | state_i) = SIGMA(state_i+1) P(o_i+2:n | state_i+1) *
    # P(o_i+1 | state_i+1) * P(state_i+1 | state_i)
    for i,o in reversed(list(enumerate(observations))):
        for state in list(STATES):
            nxt = 0.0
            # print i,o,scores
            # import pdb; pdb.set_trace()
            for next_state in list(STATES):
                nxt += scores[i+1][next_state] * transitions[state][next_state]
            scores[i][state] = nxt * emissions[state][o]

    return scores

def forward_backward(observations, parameters = crooked_casino):
    f = forward(observations, parameters)
    b = backward(observations, parameters)

    fb = [ {} for x in f ]
    for i,row in enumerate(f):
        # import pdb; pdb.set_trace()
        s = 0.0
        for k,v in row.items():
            fb[i][k] = v * b[i][k]
            # if fb[i][k] == 0:
            #     print "!!forward backward!! epsilon"
            #     fb[i][k] = 0.01
            s += fb[i][k]
        # normalize
        for k,v in row.items():
            fb[i][k] /= s

    return fb

def max_forward_backward(observations, parameters = crooked_casino):
    fb = forward_backward(observations, parameters)

    return [ max(row.items(), key = lambda x: x[1]) for row in fb ]


from random import random

x = random(); y = 1 - x;
a = random(); b = 1 - a;
model_transitions = { STATES.fair: { STATES.fair: a, STATES.biased: b },
                STATES.biased: { STATES.fair: x, STATES.biased: y } }
# initial = { STATES.fair: 0.83, STATES.biased: 0.17 }
x = random(); y = 1 - x;
model_initial = { STATES.fair: x, STATES.biased: y }
x = random(); y = 1 - x;
a = random(); b = 1 - a;
model_emissions = { STATES.fair: { EMISSIONS.H: a, EMISSIONS.T: b },
                STATES.biased: { EMISSIONS.H: x, EMISSIONS.T: y } }

casino_model = Parameters(model_transitions, model_emissions, model_initial)

def train(no = 10, l = 10):
    print "Before"
    print "Trans", casino_model.transitions
    print "Emis", casino_model.emissions
    print "Init", casino_model.initial
    import sys
    for t in xrange(no):
        g = casino()
        obs = [ g.next().emission for x in xrange(l) ]
        print "\r","Train", t,
        sys.stdout.flush()
        # print "Observations", obs
        m = baum_welch(obs)
    print ""
    print "After"
    print "Trans", m.transitions
    print "Emis", m.emissions
    print "Init", m.initial
    print ""
    print "Orig"
    print "Trans", crooked_casino.transitions
    print "Emis", crooked_casino.emissions
    print "Init", crooked_casino.initial

def batch_train(batch_size = 10, obs_length = 10):
    print "Before"
    print "Trans", casino_model.transitions
    print "Emis", casino_model.emissions
    print "Init", casino_model.initial
    import sys
    observations_list = []
    for t in xrange(batch_size):
        g = casino()
        obs = [ g.next().emission for x in xrange(obs_length) ]
        observations_list.append(obs)

    m = batch_baum_welch(observations_list)

    print ""
    print "After"
    print "Trans", m.transitions
    print "Emis", m.emissions
    print "Init", m.initial
    print ""
    print "Orig"
    print "Trans", crooked_casino.transitions
    print "Emis", crooked_casino.emissions
    print "Init", crooked_casino.initial

def alpha(observations, model = crooked_casino):
    transitions = model.transitions
    emissions = model.emissions
    initial = model.initial

    f = [ { state: 1.0 for state in list(STATES) } for o in observations ]

    f[0] = { state: (initial[state] * emissions[state][observations[0]]) for state in list(STATES) }

    for i,o in enumerate(observations[1:],1):
        for state in list(STATES):
            s = sum(f[i-1][prev_state] * transitions[prev_state][state] for prev_state in list(STATES))
            f[i][state] = s * emissions[state][o]
        # normalize
        row_sum = sum(f[i][state] for state in list(STATES))
        for state in list(STATES):
            f[i][state] /= float(row_sum)

    return f

def beta(observations, model = crooked_casino):
    transitions = model.transitions
    emissions = model.emissions
    initial = model.initial

    b = [ { state: 1.0 for state in list(STATES) } for o in observations ]

    # alredy initialized border case
    # b[-1] = { state: 1.0 for state in list(STATES) }

    for i,o in reversed(list(enumerate(observations[1:]))):
        for state in list(STATES):
            b[i][state] = sum( transitions[state][next_state]
                              * emissions[next_state][o]
                              * b[i+1][next_state] for next_state in list(STATES) )
        row_sum = sum(b[i][state] for state in list(STATES))
        for state in list(STATES):
            b[i][state] /= float(row_sum)

    return b

def baum_welch(observations, model = casino_model):
    transitions = model.transitions
    emissions = model.emissions
    initial = model.initial

    # f = forward(observations, model)
    # b = backward(observations, model)
    f = alpha(observations, model)
    b = beta(observations, model)

    # print "forward", f
    # print "backward", b

    ksi = [ { fro: { to: 1.0 for to in list(STATES) } for fro in list(STATES) } for x in observations[:-1] ]
    for i,o in enumerate(observations[1:] ,0):
        s = 0.0
        for fro in list(STATES):
            for to in list(STATES):
                ksi[i][fro][to] = f[i][fro]*transitions[fro][to]*b[i+1][to]*emissions[to][o]
                # if ksi[i][fro][to] == 0:
                #     print "!!baum welch!! epsilon"
                #     ksi[i][fro][to] = 0.01
                #     # import pdb; pdb.set_trace()
                s += ksi[i][fro][to]
        # normalize
        # if s != 0:
        if True:
            for fro in list(STATES):
                for to in list(STATES):
                    ksi[i][fro][to] /= s

    # gamma = forward_backward(observations, model)
    # print "old gamma", len(gamma), gamma

    gamma = [ { state: 1.0 for state in list(STATES) } for x in observations[:-1] ]
    for i,row in enumerate(gamma):
        for state in list(STATES):
            s = sum(ksi[i][state][to] for to in list(STATES))
            row[state] = s

    # print "new gamma", len(gamma), gamma
    # print ksi

    for row in gamma:
        for state in list(STATES):
            initial[state] = row[state]
    s = sum(v for v in initial.values())
    for state in initial:
        initial[state]/=s

    for fro in list(STATES):
        for to in list(STATES):
            transitions[fro][to] = sum( row[fro][to] for row in ksi[:-1] )/sum( row[fro] for row in gamma[:-1])
            if transitions[fro][to] == 0:
                transitions[fro][to] = 0.01

    for state in list(STATES):
        for em in list(EMISSIONS):
            nom = 0.0
            for i in xrange(len(observations[:-1])):
                if observations[i] == em:
                    nom += gamma[i][state]
            emissions[state][em] = nom/sum( row[state] for row in gamma)
            if emissions[state][em] == 0:
                emissions[state][em] = 0.01

    return model

def batch_baum_welch(observations_list, model = casino_model):
    transitions = model.transitions
    emissions = model.emissions
    initial = model.initial

    def gamma_ksi(observations):
        f = alpha(observations, model)
        b = beta(observations, model)

        ksi = [ { fro: { to: 1.0 for to in list(STATES) } for fro in list(STATES) } for x in observations[:-1] ]
        for i,o in enumerate(observations[1:] ,0):
            s = 0.0
            for fro in list(STATES):
                for to in list(STATES):
                    ksi[i][fro][to] = f[i][fro]*transitions[fro][to]*b[i+1][to]*emissions[to][o]
                    # if ksi[i][fro][to] == 0:
                    #     print "!!baum welch!! epsilon"
                    #     ksi[i][fro][to] = 0.01
                    #     # import pdb; pdb.set_trace()
                    s += ksi[i][fro][to]
            # normalize
            # if s != 0:
            if True:
                for fro in list(STATES):
                    for to in list(STATES):
                        ksi[i][fro][to] /= s

        # gamma = forward_backward(observations, model)
        # print "old gamma", len(gamma), gamma

        gamma = [ { state: 1.0 for state in list(STATES) } for x in observations[:-1] ]
        for i,row in enumerate(gamma):
            for state in list(STATES):
                s = sum(ksi[i][state][to] for to in list(STATES))
                row[state] = s
        return gamma, ksi

    gamma_ksi_list = [ gamma_ksi(observations) for observations in observations_list ]

    gammas = [ x[0] for x in gamma_ksi_list ]
    ksis = [ x[1] for x in gamma_ksi_list ]


    # sum state probability for all steps in gamma for all gammas
    # for gamma in gammas:
    #     for row in gamma:
    #         for state in list(STATES):
    #             initial[state] += row[state]

    for state in list(STATES):
        initial[state] = 0.0

    for gamma in gammas:
        for state in list(STATES):
            initial[state] += gamma[0][state]
    # normalize
    s = sum(v for v in initial.values())
    for state in initial:
        initial[state] /= s

    from itertools import chain
    for fro in list(STATES):
        for to in list(STATES):
            noms = [ [ row[fro][to] for row in ksi[:-1] ] for ksi in ksis ]
            denoms = [ [ row[fro] for row in gamma[:-1] ] for gamma in gammas ]
            transitions[fro][to] = sum( chain(*noms) ) / sum( chain(*denoms) )
            if transitions[fro][to] == 0:
                transitions[fro][to] = 0.01

    for state in list(STATES):
        for em in list(EMISSIONS):
            nom = 0.0
            for observations in observations_list:
                for i in xrange(len(observations[:-1])):
                    if observations[i] == em:
                        nom += gamma[i][state]
            emissions[state][em] = nom/sum( row[state] for row in gamma for gamma in gammas)
            if emissions[state][em] == 0:
                emissions[state][em] = 0.01

    return model

def decode(experiment, parameters = crooked_casino, verbose = True):
    """ Calculates most probable path which gives observed emissions => argmax(P(x,PI))
    x - observed emissions
    PI - path throught hidden states

    Exponential decode, iterates over all paths calculating it's probabilities
    O(len(experiment),states) = states**len(experiments)
    """
    transitions = parameters.transitions
    emissions = parameters.emissions
    initial = parameters.initial

    from itertools import product
    paths = product(list(STATES), repeat=len(experiment))
    paths_prob = {}
    for path in paths:
        prob = initial[path[0]]
        prev = path[0]
        for state in path[1:]:
            prob *= transitions[prev][state]
            prev = state
        paths_prob[path] = prob

    paths_emiss_prob = {}
    for path,prob in paths_prob.items():
        emiss_prob = prob
        for state,emiss in zip(path, experiment):
            emiss_prob *= emissions[state][emiss]
        paths_emiss_prob[path] = emiss_prob

    arg_max = max(paths_emiss_prob.items(), key=lambda x: x[1])
    if verbose:
        print prettyprint(arg_max[0],arg_max[1])
        print "------------"
        for k,v in sorted(paths_emiss_prob.items(), key=lambda l: l[1]):
            print prettyprint(k,v)

    return arg_max

def pass_prob(experiment, parameters = crooked_casino):
    transitions = parameters.transitions
    emissions = parameters.emissions
    initial = parameters.initial

    from itertools import product
    paths = product(list(STATES), repeat=len(experiment))
    paths_prob = {}
    for path in paths:
        prob = initial[path[0]]
        prev = path[0]
        for state in path[1:]:
            prob *= transitions[prev][state]
            prev = state
        paths_prob[path] = prob

    paths_emiss_prob = {}
    for path,prob in paths_prob.items():
        emiss_prob = prob
        for state,emiss in zip(path, experiment):
            emiss_prob *= emissions[state][emiss]
        paths_emiss_prob[path] = emiss_prob

    return sum(paths_emiss_prob.values())

def max_prob(length, patameters = crooked_casino):
    from itertools import product
    passes = product(list(EMISSIONS), repeat=length)

    probs = { pas: pass_prob(pas) for pas in passes }

    arg_max =  max(probs.items(), key=lambda x: x[1])
    print emprettyprint(arg_max[0],arg_max[1])
    print "------------"
    for k,v in sorted(probs.items(), key=lambda l: l[1]):
        print emprettyprint(k,v)

    return arg_max

def prettyprint(states, prob):
    from string import join
    s = [ 'F' if state.name == 'fair' else 'B' for state in states ]
    return join(s), "{0:.5f}".format(prob)

def emprettyprint(states, prob):
    from string import join
    s = [ 'H' if state.name == 'H' else 'T' for state in states ]
    return join(s), "{0:.5f}".format(prob)

def estimation(gen = casino(), samples=1000):
    from collections import defaultdict
    from collections import Counter
    # counting = lambda: defaultdict(lambda: 0.0)
    transitions = defaultdict(lambda: Counter())
    emissions = defaultdict(lambda: Counter())

    # count data
    initial = gen.next()
    state = initial.state
    for x in xrange(samples):
        record = gen.next()
        new_state = record.state
        emission = record.emission
        transitions[state][new_state] += 1
        emissions[new_state][emission] += 1
        state = new_state

    # normalize
    normalized_transitions = {}
    for state,row in transitions.items():
        occurences = float(sum(v for k,v in row.items()))
        normalized_row = { k: v/occurences for k,v in row.items() }
        normalized_transitions[state] = normalized_row

    normalized_emissions = {}
    for state,row in emissions.items():
        occurences = float(sum(v for k,v in row.items()))
        normalized_row = { k: v/occurences for k,v in row.items() }
        normalized_emissions[state] = normalized_row

    return Parameters(normalized_transitions, normalized_emissions)

# if __name__ == '__main__':
#     for i in range(100):
#         print "Batch no", i
#         train(100,300)
#         print ""
