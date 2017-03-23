#!/usr/bin/env python
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
"""

from prob import P
from enum import Enum

class Phenotype(Enum):
    O = 0
    A = 1
    B = 2
    AB = 3

class Genotype(Enum):
    OO = 1
    OA = 2
    AO = 3
    AA = 4
    OB = 5
    BO = 6
    BB = 7
    AB = 8

p_Phenotype = P(Phenotype)
p_Phenotype.table([ [Phenotype.O, 0.37],
                    [Phenotype.A, 0.38],
                    [Phenotype.B, 0.17],
                    [Phenotype.AB,0.08]])

p_Genotype = P(Genotype)
p_Genotype.table([ [Genotype.OO, 1.0],
                   [Genotype.OA, 1.0],
                   [Genotype.AO, 1.0],
                   [Genotype.AA, 1.0],
                   [Genotype.OB, 1.0],
                   [Genotype.BO, 1.0],
                   [Genotype.BB, 1.0],
                   [Genotype.AB, 1.0]])
p_Genotype.normalize()

p_Phenotype_Genotype = P(Phenotype).given(Genotype)
p_Phenotype_Genotype.table([ [Phenotype.O, Genotype.OO, 1.0],
                             [Phenotype.A, Genotype.OA, 1.0],
                             [Phenotype.A, Genotype.AO, 1.0],
                             [Phenotype.A, Genotype.AA, 1.0],
                             [Phenotype.B, Genotype.OB, 1.0],
                             [Phenotype.B, Genotype.BO, 1.0],
                             [Phenotype.B, Genotype.BB, 1.0],
                             [Phenotype.AB, Genotype.AB, 1.0]])

p_Genotype_Phenotype = P(Genotype).given(Phenotype)
p_Genotype_Phenotype.table([ [Genotype.OO, Phenotype.O, 1.0],
                             [Genotype.OA, Phenotype.A, 0.33],
                             [Genotype.AO, Phenotype.A, 0.33],
                             [Genotype.AA, Phenotype.A, 0.34],
                             [Genotype.OB, Phenotype.B, 0.33],
                             [Genotype.BO, Phenotype.B, 0.33],
                             [Genotype.BB, Phenotype.B, 0.34],
                             [Genotype.AB, Phenotype.AB, 1.0]])

p_PhenotypeGenotype = p_Genotype_Phenotype * p_Phenotype

# p_Genotype_Phenotype = p_PhenotypeGenotype / p_Phenotype
"""
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

