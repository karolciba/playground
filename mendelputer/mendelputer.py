"""
Phenotype: 0, A, B, AB
Genotype: 00, 0A, A0, AA, 0B, B0, BB, AB


P(P):
 0      .37
 A      .38
 B      .17
 AB     .08

P(P|G)
 0 | 00     1
 A | 0A     1
 A | A0     1
 A | AA     1
 B | 0B     1
 B | B0     1
 B | BB     1
 AB | AB    1

 otherwise  0

P(P,G) = P(P|G)*P(G)
P(P,G) = P(G|P)*P(P)
P(G|P) = P(P|G)*P(G)/P(P)

P(P|Pp): sum( P|PmPd, Pd)

                       Grand Mom Pheno     Uknown Parent Pheno
                        |   |                     |
               +--------+   |  +------------------+
               v            |  |
         Grand Mom Blood    |  |
                            v  v
   Mom Pheno              Dad Pheno                  Step Mom Pheno
     |  |                   |  |  |                     |     |
     |  |                   |  |  +-------------+       |     |
     |  |                   |  |                |       |     +-------+
   +-+  +------+  +------+--+  +-+              +---+   |             v
   v           |  |      |       v                  |   |      Step Mom Blood
Mom Blood      |  |      |    Dad Blood             v   v
               |  |      |                    Step Sister Pheno
               v  v      +-----------+                |
            Child Pheno              v                v
                 |            Sibiling Pheno   Step Sister Blood
                 v                   |
            Child Blood              v
                              Sibiling Blood

"""

"""
Possible Node instances:
 blood : value
 0     : .37
 A     : .38
 B     : .17
 AB    : .08

 child_blood, parent_blood : value
 A            A            : .3
 0            A            : .2
 0            AB           : 0

 child_blood, parent_blood | grand_blood : value
 A            A            | A           : .3
 0            A            | 0           : .2
 0            AB           | 0           : 0
"""

class Node():

    def __init__(self, name, columns, conditions = [], table = []):
        """ variables names list
        conditions list which of the variables are conditions, empty for joint
        """
        from collections import namedtuple
        # tuple ("a","b","c", 0.314)
        self.factors = dict()

        self.conditions = list(conditions)
        self.columns = list(columns)

        self.name = name
        self.parents = {}
        self.children = {}

    def add_row(self, variables, value):
        key = tuple(variables)
        self.factors[key] = value

    def set_parent(self, parent):
        self.parents.add(parent)
        parent.children.add(self)

    def add_child(self, child):
        child.add_parent(self)

    def marginalize(self, name):
        if name in self.columns and name not in self.conditions:
            factors = {}
            column = next(pos for pos,val in enumerate(self.columns) if val == name)
            column_space = set( v for v in self.factor.keys()[column] )
            new_columns = list(self.columns).remove(name)


        """ Sum over variable name reducing size table """

    def join(self, parent):
        """ Joins with parent, remove parent and takes its precedessors """


def test():
    pass
