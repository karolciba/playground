""" Finite State Automaton is described by five elements tuple:
    (S, Sigma, delta, s0, SA) where:
    S - finite set of states in the automata
    Sigma - finite alphabet used by automata (union of transitions)
    delta - tansition function delta(state_i,input) -> state_j
    s0 - initial state
    SA - list of accepting states
"""

import string
from collections import defaultdict

epsilon = ""

class Automata(object):
    def __init__(self, states, sigma, delta, s0, accepting, error_state):
        """
        states - set of states available
        sigma - alfabet
        delta - function mapping state_i, input -> next state
            must follow collections interface, i.e. delta[(state_i,'c')] -> error_state
        s0 - initial state
        accepting - set of accepting states
        """
        self.states = states or set()
        self.sigma = sigma or set()
        self.delta = delta or set()
        self.s0 = s0
        self.accepting = accepting or set()
        self.error_state = error_state

        self.fringe = [ s0 ]

    def transit(self, input):
        # if input not in self.sigma:
        #     raise Exception("Input not in alphabet")
        next_fringe = []
        for state in self.fringe:
            next_state = self.delta[state,input]
            if next_state:
                next_fringe.append(next_state)
            else:
                raise Exception("Unknown transition")
                next_fringe.append(self.error_state)
            if (next_state,"") in self.delta:
                next_fringe.extend(self.delta[next_state,""])

        self.fringe = set(next_fringe)

    def match(self, string):
        self.reset()
        for char in string:
            self.transit(char)
        return self.accepted()

    def reset(self):
        self.fringe = [ self.s0 ]

    def accepted(self):
        return any(st for st in self.fringe if st in self.accepting)

    def concat(self, other):
        new_start = self.s0
        new_delta = defaultdict(lambda: self.error_state)
        print 'copying left'
        for key,value in self.delta.iteritems():
            print key,value
            new_delta[key] = value

        second_start = max(self.states) + 1
        print "epsilon transition from accepitn"
        for acc in self.accepting:
            print (acc,""), second_start
            new_delta[acc,""] = [second_start]

        print "appending right"
        for key,value in other.delta.iteritems():
            new_key = key[0]+second_start,key[1]
            new_value = value + second_start
            print "old:",key,value, "new:", new_key, new_value
            new_delta[new_key] = new_value

        new_accepting = [ oth_acc+second_start for oth_acc in  other.accepting]
        new_sigma = self.sigma + other.sigma

        print new_delta
        new_states = set(key[0] for key in new_delta)
        return Automata(new_states, new_sigma, new_delta, new_start, new_accepting, self.error_state)

    def alternate(self, other):
        new_start = 0
        new_delta = defaultdict(lambda: self.error_state)
        for key,value in self.delta.iteritems():
            new_key = key[0]+1,key[1]
            new_value = value + 1
            new_delta[new_key] = new_value

        second_start = max(self.states) + 1
        new_delta[0,""] = [ self.s0 + 1, other.s0 + 2]
        for key,value in other.delta.iteritems():
            new_key = key[0]+second_start,key[1]
            new_value = value + second_start
            print "old:",key,value, "new:", new_key, new_value
            new_delta[new_key] = new_value

        new_sigma = self.sigma + other.sigma

        print new_delta
        new_states = set(key[0] for key in new_delta)
        new_accepting = len(new_states) + 1

        acc_eps = [s_acc + 1 for s_acc in self.accepting]
        acc_eps += [o_acc + second_start for o_acc in other.accepting ]

        for s in acc_eps:
            delta[s,""] = [new_accepting]
        return Automata(new_states, new_sigma, new_delta, new_start, new_accepting, self.error_state)

    def __str__(self):
        return super(Automata,self).__str__() + " In state {}, accepting {}"\
            .format(self.fringe, [st for st in self.fringe if st in self.accepting])



# INTEGER
# Integer 0|[1-9][0-9]*
delta = defaultdict(lambda: -1)
delta[0,'0'] = 1
for x in range(1,10):
    delta[0,str(x)] = 2
    delta[2,str(x)] = 2
delta[2,'0'] = 2

INTEGER = Automata(set([-1,0,1,2]),string.digits, delta, 0, [1,2], -1)

# FLOAT
# Float (0|[1-9][0-9]*)+.[0-9]*
delta = defaultdict(lambda: -1)
delta[0,'0'] = 1
delta[0,'.'] = 4
for x in range(1,10):
    delta[0,str(x)] = 2

delta[1,'.'] = 3

for x in range(0,10):
    delta[2,str(x)] = 2
delta[2,'.'] = 3

for x in range(0,10):
    delta[3,str(x)] = 3

for x in range(0,10):
    delta[4,str(x)] = 5
    delta[5,str(x)] = 5


FLOAT = Automata(set([-1,0,1,2]),string.digits+".", delta, 0, [3, 5], -1)

PLUS = Automata(set([-1,0,1]),"+",defaultdict(lambda: -1, [ ((0,"+"),1)]), 0, [1], -1)
MINUS = Automata(set([-1,0,1]),"-",defaultdict(lambda: -1, [ ((0,"-"),1)]), 0, [1], -1)
MUL = Automata(set([-1,0,1]),"*",defaultdict(lambda: -1, [ ((0,"*"),1)]), 0, [1], -1)
DIV = Automata(set([-1,0,1]),"/",defaultdict(lambda: -1, [ ((0,"/"),1)]), 0, [1], -1)

if __name__ == "__main__":
    from collections import defaultdict

    print "Test automata"
    states = set(xrange(-1,5))
    sigma = 'abcdef'

    delta = defaultdict(lambda: -1)
    delta[0, 'a'] = 1
    delta[1, 'b'] = 2
    delta[2, 'c'] = 3
    accepting = set([3])

    auto = Automata(states, sigma, delta, 0, accepting, -1)

    print "Transition a-b-c"
    auto.transit('a')
    print auto
    auto.transit('b')
    print auto
    auto.transit('c')
    print auto


    print "INTEGER"
    integer = INTEGER
    print "Transition 01"
    for c in '01':
        print "transition", c
        integer.transit(c)
        print integer

    integer.reset()
    print "Transition 1012"
    for c in '1012':
        print "transition", c
        integer.transit(c)
        print integer


    delta = defaultdict(lambda: -1)
    delta[0,'n'] = 1
    delta[1,'e'] = 2
    delta[2,'w'] = 3
    delta[1,'o'] = 4
    delta[4,'t'] = 5

    states = [x for x in range(6)]
    newnot = Automata(states, set('newnot'), delta, 0, [3,5],-1)

    newnot.reset()
    print "Transition not"
    for c in 'not':
        print "transition", c
        newnot.transit(c)
        print newnot

    print "FLOAT"
    float = FLOAT
    transitions = ['123.123', '1.9', '0.434', '0.', '.0', '.123', '.', '123foobar.23']
    for trans in transitions:
        float.reset()
        # print "transition", trans
        for c in trans:
            # print "transition", c
            float.transit(c)
            # print float
        print "transition", trans, "accepted", float.accepted()

    # print "PLUS"
    # transitions = ['+', '-', '123+123', '123.23+foobar']
    # plus = PLUS
    # for trans in transitions:
    #     plus.reset()
    #     for c in trans:
    #         # print "transition", c
    #         plus.transit(c)
    #         # print plus
    #     print "transition", trans, "accepted", plus.accepted()
