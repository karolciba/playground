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
    """Nondeterministic Finite Automata"""
    def __init__(self, states, delta, accepting):
        """
        states - count of states (including start state, excluding error state)
        delta - function mapping state_i, input -> next state
            must follow collections interface, i.e. delta[(state_i,'c')] -> error_state
        accepting - set of accepting states

        error_state = implicit -1
        s0 - initial state, implicit 0
        sigma - implicit alphabet of all chars
        """
        self.states = states

        # self.delta = defaultdict(lambda: set([-1]))
        new_delta = dict()
        # tranlate new_stastes to set's
        for key,value in delta.iteritems():
            listed_value = list()
            try:
                listed_value.extend(value)
            except:
                listed_value.append(value)
            new_delta[key] = frozenset(listed_value)

        # compress input - if many edges from state to state condense them in
        # one with a list, default list with one item.
        # NOTE: poor complexity o(len(delta)**2)
        # self.delta = new_delta
        # new_delta = dict()
        # transitions = set((k[0],v) for k,v in self.delta.iteritems())
        # for fro,to in transitions:
        #     inputs = frozenset(k[1] for k,v in self.delta.iteritems() if k[0] == fro and v == to)
        #     new_delta[fro,inputs] = to

        self.delta = new_delta

        self.s0 = 0
        self.accepting = set()
        try:
            self.accepting.update(accepting)
        except:
            self.accepting.add(accepting)

        self.error_state = -1

        self.fringe = set([ self.s0 ])
        adt = self.delta.get((self.s0,""),None)
        if adt:
            self.fringe.update(adt)
        self._unroll_fringe()

    def _unroll_fringe(self):
        while True:
            new_fringe = set()
            for state in self.fringe:
                new_fringe.add(state)
                adt = self.delta.get((state,""),None)
                if adt:
                    new_fringe.update(adt)
            if new_fringe == self.fringe:
                break
            self.fringe = new_fringe

    def transit(self, input):
        next_fringe = set()
        for state in self.fringe:
            next_state = self.delta.get((state,input),set([-1]))
            if next_state:
                next_fringe.update(next_state)
            else:
                next_fringe.add(-1)
            # epsilon transitions
            for n in next_state:
                if (n,"") in self.delta:
                    next_fringe.update(self.delta[n,""])

        self.fringe = next_fringe
        self._unroll_fringe()

    def match(self, string):
        self.reset()
        for char in string:
            self.transit(char)
        return self.accepted()

    def reset(self):
        self.fringe = set([ self.s0 ])
        if (self.s0,"") in self.delta:
            self.fringe.update(self.delta[self.s0,""])

    def accepted(self):
        return any(st for st in self.fringe if st in self.accepting)

    def concat(self, other):
        new_states = self.states + other.states
        new_delta = defaultdict(lambda: set([-1]))
        max_state = 0
        # renumbering old states shifting them +1
        for key,value in self.delta.iteritems():
            # (state, input) => new_state
            new_key = key[0], key[1]
            max_state = max(max_state, max(value))
            new_delta[new_key] = set(value)

        # transitions from old accepting to other start
        other_start = max_state + 1
        for acc in self.accepting:
            new_delta[acc,""] = other_start

        # renumbering other states shiting them whast already is
        for key,value in other.delta.iteritems():
            new_key = key[0] + other_start, key[1]
            new_delta[new_key] = set(v + other_start for v in value)

        new_accepting = [ o_acc + other_start for o_acc in other.accepting ]

        return Automata(new_states, new_delta, new_accepting)


    def alternate(self, other):
        new_states = self.states + other.states
        new_delta = defaultdict(lambda: set([-1]))

        max_state = 1
        # renumbering old states shifting them +1
        for key,value in self.delta.iteritems():
            # (state, input) => new_state
            new_key = key[0]+1, key[1]
            max_state = max(max_state, max(value) + 1)
            new_delta[new_key] = set(v + 1 for v in value)

        other_start = max_state + 1
        # renumbering other states shiting them whast already is
        for key,value in other.delta.iteritems():
            new_key = key[0] + other_start, key[1]
            new_delta[new_key] = set(v + other_start for v in value)

        # epsilon transitions to both start_states
        new_delta[0,""] = [ 1, other_start ]

        new_accepting = [ s_acc + 1 for s_acc in self.accepting ]
        new_accepting += [ o_acc + other_start for o_acc in other.accepting ]

        return Automata(new_states, new_delta, new_accepting)

    def __and__(self, other):
        return self.concat(other)

    def __or__(self, other):
        return self.alternate(other)

    def __str__(self):
        return super(Automata,self).__str__() + " In state {}, accepting {}"\
            .format(self.fringe, [st for st in self.fringe if st in self.accepting])

    def __repr__(self):
        return super(Automata,self).__repr__() + " In state {}, accepting {}"\
            .format(self.fringe, [st for st in self.fringe if st in self.accepting])



# INTEGER
# Integer 0|[1-9][0-9]*
delta = defaultdict(lambda: -1)
delta[0,'0'] = 1
for x in range(1,10):
    delta[0,str(x)] = 2
    delta[2,str(x)] = 2
delta[2,'0'] = 2

INTEGER = Automata(3, delta, [1,2])

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


FLOAT = Automata(3, delta, [3, 5])

PLUS = Automata(2,defaultdict(lambda: -1, [ ((0,"+"),1)]),[1])
MINUS = Automata(2,defaultdict(lambda: -1, [ ((0,"-"),1)]),[1])
MUL = Automata(2,defaultdict(lambda: -1, [ ((0,"*"),1)]),[1])
DIV = Automata(2,defaultdict(lambda: -1, [ ((0,"/"),1)]),[1])

SIGNED_INTEGER = MINUS & INTEGER

if __name__ == "__main__":

    print "Test automata"

    print "INTEGER"
    integer = INTEGER
    transitions = ['123123', '19', '0.434', '0.', '.0', '0', '.1', '123foobar.23']
    for trans in transitions:
        integer.reset()
        # print "transition", trans
        for c in trans:
            # print "transition", c
            integer.transit(c)
            # print float
        print "transition", trans, "accepted", integer.accepted()

    print "SIGNED INTEGER"
    signed_integer = SIGNED_INTEGER
    transitions = ['123123', '-19', '0.434', '0.', '.0', '0', '.1', '123foobar.23']
    for trans in transitions:
        signed_integer.reset()
        # print "transition", trans
        for c in trans:
            # print "transition", c
            signed_integer.transit(c)
            # print float
        print "transition", trans, "accepted", signed_integer.accepted()

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

    print "PLUS"
    transitions = ['+', '-', '123+123', '123.23+foobar']
    plus = PLUS
    for trans in transitions:
        plus.reset()
        for c in trans:
            # print "transition", c
            plus.transit(c)
            # print plus
        print "transition", trans, "accepted", plus.accepted()

    print "PLUS AND MINUS"
    transitions = ['+-', '-+', '+', '-',  '123+123', '123.23+foobar']
    plus_and_minus = PLUS & MINUS
    for trans in transitions:
        plus_and_minus.reset()
        for c in trans:
            # print "transition", c
            plus_and_minus.transit(c)
            # print plus
        print "transition", trans, "accepted", plus_and_minus.accepted()

    print "PLUS OR MINUS"
    transitions = ['+-', '-+', '+', '-', '123+123', '123.23+foobar']
    plus_or_minus = PLUS | MINUS
    for trans in transitions:
        plus_or_minus.reset()
        for c in trans:
            # print "transition", c
            plus_or_minus.transit(c)
            # print plus
        print "transition", trans, "accepted", plus_or_minus.accepted()

    print "SIGNED INTEGER"
    sint = MINUS.concat(INTEGER)
    transitions = ['-123', '123', '-123.2']
    for trans in transitions:
        sint.reset()
        for c in trans:
            # print "transition", c
            sint.transit(c)
            # print plus
        print "transition", trans, "accepted", sint.accepted()

    print "ANYINT"
    anyint = (MINUS & INTEGER) | INTEGER
    transitions = ['-123', '123', '-123.2']
    for trans in transitions:
        anyint.reset()
        for c in trans:
            # print "transition", c
            anyint.transit(c)
            # print anyint
        print "transition", trans, "accepted", anyint.accepted()

    print "ANYFLOAT"
    anyfloat = FLOAT | (MINUS & FLOAT)
    transitions = ['-123.', '123.', '-.2', '.3', '34']
    for trans in transitions:
        anyfloat.reset()
        for c in trans:
            # print "transition", c
            anyfloat.transit(c)
            # print anyint
        print "transition", trans, "accepted", anyfloat.accepted()

    print "NUMBER"
    number = FLOAT | INTEGER
    transitions = ['123.', '123', '-.2', '.3', '34', '-5']
    for trans in transitions:
        number.reset()
        for c in trans:
            # print "transition", c
            number.transit(c)
            # print anyint
        print "transition", trans, "accepted", number.accepted()

    print "ANYNUMBER"
    anynumber = INTEGER | (MINUS&INTEGER) | FLOAT
    transitions = ['123.', '123', '-.2', '.3', '34', '-5']
    for trans in transitions:
        anynumber.reset()
        for c in trans:
            # print "transition", c
            anynumber.transit(c)
            # print anyint
        print "transition", trans, "accepted", anynumber.accepted()

    print "INT OP INT"

    anyint = INTEGER | (MINUS & INTEGER)
    anyfloat = FLOAT | (MINUS & FLOAT)
    number = anyint | anyfloat
    binop = PLUS | MINUS | MUL | DIV
    expr = (anyfloat | anyint) & binop & anyint
    expr = anyint & binop & anyint
    expr = (INTEGER | FLOAT | (MINUS&INTEGER)) & binop & number

    transitions = ['12+23', '-12*7', '12./4', '11-23.0']
    for trans in transitions:
        expr.reset()
        for c in trans:
            # print "transition", c
            expr.transit(c)
            # print anyint
        print "transition", trans, "accepted", expr.accepted()

    print "(FLOAT | INT | -FLOAT | -INT) & (+ | - | * | / ) & (FLOAT | INT | -FLOAT | -INT)"

    anyint = INTEGER | (MINUS & INTEGER)
    anyfloat = FLOAT | (MINUS & FLOAT)
    number = anyint | anyfloat
    binop = PLUS | MINUS | MUL | DIV
    expr = number & binop & number

    transitions = ['12+23', '12*.7', '12./4', '11-23.']
    for trans in transitions:
        expr.reset()
        for c in trans:
            # print "transition", c
            expr.transit(c)
            # print anyint
        print "transition", trans, "accepted", expr.accepted()
