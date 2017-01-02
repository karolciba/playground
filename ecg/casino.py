
from enum import Enum

STATES = Enum('Coin', 'fair biased')
EMISSIONS = Enum('Toss', 'H T')

from collections import namedtuple
Parameters = namedtuple('Parameters','transitions emissions initial')

transitions = { STATES.fair: { STATES.fair: 0.9, STATES.biased: 0.1 },
                STATES.biased: { STATES.fair: 0.5, STATES.biased: 0.5 } }
initial = { STATES.fair: 0.83, STATES.biased: 0.17 }
emissions = { STATES.fair: { EMISSIONS.H: 0.5, EMISSIONS.T: 0.5 },
                STATES.biased: { EMISSIONS.H: 0.75, EMISSIONS.T: 0.25 } }

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
    trans = izip(state_i, state_i_next)
    # select transitions probabilities
    trans_coef = [ transitions[i][j] for i,j in trans ]
    # states path probability, initial prob * transitions
    state_prob = initial[pi[0]] * mul(trans_coef)

    # import pdb; pdb.set_trace()
    emiss_list = [ emissions[state][obs] for state,obs in zip(pi,x) ]
    print emiss_list
    emiss_prob = mul(emiss_list)

    return state_prob * emiss_prob

def decode(experiment, parameters = crooked_casino):
    transitions = parameters.transitions
    emissions = parameters.emissions

    from itertools import product
    paths = product(list(STATES), repeat=len(experiment))
    paths_prob = {}
    for path in paths:
        prob = 1./len(STATES)
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
    print prettyprint(arg_max[0],arg_max[1])
    print "------------"
    for k,v in sorted(paths_emiss_prob.items(), key=lambda l: l[1]):
        print prettyprint(k,v)

    return arg_max

def pass_prob(experiment, parameters = crooked_casino):
    transitions = parameters.transitions
    emissions = parameters.emissions

    from itertools import product
    paths = product(list(STATES), repeat=len(experiment))
    paths_prob = {}
    for path in paths:
        prob = 1./len(STATES)
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
