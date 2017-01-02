
from enum import Enum

STATES = Enum('Coin', 'fair biased')
EMISSIONS = Enum('Toss', 'H T')

from collections import namedtuple
Parameters = namedtuple('Parameters','transitions emissions')

transitions = { STATES.fair: { STATES.fair: 0.9, STATES.biased: 0.1 },
                STATES.biased: { STATES.fair: 0.5, STATES.biased: 0.5 } }
emissions = { STATES.fair: { EMISSIONS.H: 0.5, EMISSIONS.T: 0.5 },
                STATES.biased: { EMISSIONS.H: 0.75, EMISSIONS.T: 0.25 } }

crooked_casino = Parameters(transitions, emissions)

def strtotoss(string):
    toss = []
    l = list(EMISSIONS)
    for c in string:
        toss += [ x for x in l if x.name == c ]
    return toss

def casino(parameters = crooked_casino):
    import random

    from collections import namedtuple
    record = namedtuple('Record', 'emission state')

    # TODO: exercise reimplemnt
    from numpy.random import choice

    state = random.choice(list(STATES))

    transitions = parameters.transitions
    emissions = parameters.emissions

    while True:
        yield record(choice(emissions[state].keys(), p=emissions[state].values()), state)
        state = choice(transitions[state].keys(), p=transitions[state].values())

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
