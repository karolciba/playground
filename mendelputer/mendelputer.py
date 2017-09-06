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

def genPhenotypeSet(name):
    return Enum("Phenotype_"+name,"0 A B AB", module=__name__)

def genPhenotypeGivenGenotypeProb(name,genotype):
    pset = genPhenotypeSet(name)
    return "p_NAME(TOP_Parent)_Phenotype_Genotype"

def genGenotypeGivenParentsGenotype(name,mother,father):
    return "p_"


class Genotype(Enum):
    OO = 1
    OA = 2
    AO = 3
    AA = 4
    OB = 5
    BO = 6
    BB = 7
    AB = 8
    BA = 9

def genGenotypeSet(name):
    return Enum("Genotype_"+name, "OO OA AO AA OB BO BB AB BA", module=__name__)

"""
# wikipedia - eu
p_Phenotype = P(Phenotype)
p_Phenotype.table([ [Phenotype.O, 0.37],
                    [Phenotype.A, 0.38],
                    [Phenotype.B, 0.17],
                    [Phenotype.AB,0.08]])

# http://anthro.palomar.edu/blood/table_of_ABO_and_Rh_blood_type_frequencies_in_US.htmw
p_Phenotype = P(Phenotype)
p_Phenotype.table([ [Phenotype.O, 0.44],
                    [Phenotype.A, 0.44],
                    [Phenotype.B, 0.10],
                    [Phenotype.AB,0.04]])

p_Genotype = P(Genotype)
p_Genotype.table([ [Genotype.OO, 1.0],
                   [Genotype.OA, 1.0],
                   [Genotype.AO, 1.0],
                   [Genotype.AA, 1.0],
                   [Genotype.OB, 1.0],
                   [Genotype.BO, 1.0],
                   [Genotype.BB, 1.0],
                   [Genotype.AB, 1.0],
                   [Genotype.BA, 1.0])
p_Genotype.normalize()

# https://en.wikipedia.org/wiki/Blood_type_distribution_by_country
# http://www.sciencedirect.com/science/article/pii/S1110863011000796
# https://www.hindawi.com/journals/bmri/2014/286810/
p_Phenotype_Genotype = P(Phenotype).given(Genotype)
p_Phenotype_Genotype.table([ [Phenotype.O, Genotype.OO, 1.0],
                             [Phenotype.A, Genotype.OA, 1.0],
                             [Phenotype.A, Genotype.AO, 1.0],
                             [Phenotype.A, Genotype.AA, 1.0],
                             [Phenotype.B, Genotype.OB, 1.0],
                             [Phenotype.B, Genotype.BO, 1.0],
                             [Phenotype.B, Genotype.BB, 1.0],
                             [Phenotype.AB, Genotype.AB, 1.0],
                             [Phenotype.AB, Genotype.BA, 1.0]])

p_Genotype_Phenotype = P(Genotype).given(Phenotype)
p_Genotype_Phenotype.table([ [Genotype.OO, Phenotype.O, 1.0],
                             [Genotype.OA, Phenotype.A, 0.33],
                             [Genotype.AO, Phenotype.A, 0.33],
                             [Genotype.AA, Phenotype.A, 0.34],
                             [Genotype.OB, Phenotype.B, 0.33],
                             [Genotype.BO, Phenotype.B, 0.33],
                             [Genotype.BB, Phenotype.B, 0.34],
                             [Genotype.AB, Phenotype.AB, 1.0],
                             [Genotype.BA, Phenotype.AB, 1.0]])

p_PhenotypeGenotype = p_Genotype_Phenotype * p_Phenotype

p_Genotype_ParentLeft = P(Genotype).given(Genotype)
p_Genotype_ParentLeft.table([ [Genotype.OO, L_Genotype.OO, 1.],
                              [Genotype.OO, L_Genotype.OA, 1.],
                              [Genotype.OO, L_Genotype.OB, 1.],
                              [Genotype.AO, L_Genotype.AO, 1.],
                              [Genotype.AO, L_Genotype.AA, 1.],
                              [Genotype.AO, L_Genotype.AB, 1.],
                              [Genotype.AB, L_Genotype.AO, 1.],
                              [Genotype.AB, L_Genotype.AA, 1.],
                              [Genotype.AB, L_Genotype.AB, 1.],
                              [Genotype.BO, L_Genotype.BO, 1.],
                              [Genotype.BO, L_Genotype.BB, 1.],
                              [Genotype.BO, L_Genotype.BA, 1.],
                              [Genotype.BA, L_Genotype.BO, 1.],
                              [Genotype.BA, L_Genotype.BB, 1.],
                              [Genotype.BA, L_Genotype.BA, 1.]])

p_Genotype_ParentRight = P(Genotype).given(Genotype)
p_Genotype_ParentRight.table([ [Genotype.OO, R_Genotype.OO, 1.],
                              [Genotype.OO, R_Genotype.AO, 1.],
                              [Genotype.OO, R_Genotype.BO, 1.],
                              [Genotype.OA, R_Genotype.OA, 1.],
                              [Genotype.OA, R_Genotype.AA, 1.],
                              [Genotype.OA, R_Genotype.BA, 1.],
                              [Genotype.BA, R_Genotype.OA, 1.],
                              [Genotype.BA, R_Genotype.AA, 1.],
                              [Genotype.BA, R_Genotype.BA, 1.],
                              [Genotype.OB, R_Genotype.OB, 1.],
                              [Genotype.OB, R_Genotype.BB, 1.],
                              [Genotype.OB, R_Genotype.AB, 1.],
                              [Genotype.AB, R_Genotype.OB, 1.],
                              [Genotype.AB, R_Genotype.BB, 1.],
                              [Genotype.AB, R_Genotype.AB, 1.]])

p_Genotype_Parent = P(Genotype).given(L_Genotype,R_Genotype)
p_Genotype_Parent.table([
    [Genotype.OO, L_Genotype.OO, R.Genotype.OO, 1],
    [Genotype.OO, L_Genotype.AO, R.Genotype.OO, 1],
    [Genotype.OO, L_Genotype.OO, R.Genotype.OO, 1],
    [Genotype.OO, L_Genotype.OO, R.Genotype.OO, 1],
    [Genotype.OO, L_Genotype.OO, R.Genotype.OO, 1],
    [Genotype.OO, L_Genotype.OO, R.Genotype.OO, 1]])


# p_Genotype_Phenotype = p_PhenotypeGenotype / p_Phenotype
"""

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

