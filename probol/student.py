#!/usr/bin/env python

from prob import P
from enum import Enum
from decimal import Decimal

class Difficulty(Enum):
    d0 = 0
    d1 = 1

class Intelligence(Enum):
    i0 = 0
    i1 = 1

class Grade(Enum):
    g1 = 1
    g2 = 2
    g3 = 3

class Sat(Enum):
    s0 = 0
    s1 = 1

class Letter(Enum):
    l0 = 0
    l1 = 1

p_Intelligence = P(Intelligence)
p_Intelligence.table([[Intelligence.i0, 0.7],
                      [Intelligence.i1, 0.3]])

p_Difficulty = P(Difficulty)
p_Difficulty.table([[Difficulty.d0, 0.6],
                    [Difficulty.d1, 0.4]])

p_Sat_Intelligence = P(Sat).given(Intelligence)
p_Sat_Intelligence.table([[Intelligence.i0, Sat.s0, 0.95],
                          [Intelligence.i0, Sat.s1, 0.05],
                          [Intelligence.i1, Sat.s0, 0.2],
                          [Intelligence.i1, Sat.s1, 0.8]])

p_Grade_DifficultyIntelligence = P(Grade).given(Difficulty, Intelligence)
p_Grade_DifficultyIntelligence.table([[Intelligence.i0, Difficulty.d0, Grade.g1, 0.3],
                                      [Intelligence.i0, Difficulty.d0, Grade.g2, 0.4],
                                      [Intelligence.i0, Difficulty.d0, Grade.g3, 0.3],
                                      [Intelligence.i0, Difficulty.d1, Grade.g1, 0.05],
                                      [Intelligence.i0, Difficulty.d1, Grade.g2, 0.25],
                                      [Intelligence.i0, Difficulty.d1, Grade.g3, 0.7],
                                      [Intelligence.i1, Difficulty.d0, Grade.g1, 0.9],
                                      [Intelligence.i1, Difficulty.d0, Grade.g2, 0.08],
                                      [Intelligence.i1, Difficulty.d0, Grade.g3, 0.02],
                                      [Intelligence.i1, Difficulty.d1, Grade.g1, 0.5],
                                      [Intelligence.i1, Difficulty.d1, Grade.g2, 0.3],
                                      [Intelligence.i1, Difficulty.d1, Grade.g3, 0.2]])

p_Letter_Grade = P(Letter).given(Grade)
p_Letter_Grade.table([[Grade.g1, Letter.l0, 0.1],
                      [Grade.g1, Letter.l1, 0.9],
                      [Grade.g2, Letter.l0, 0.4],
                      [Grade.g2, Letter.l1, 0.6],
                      [Grade.g3, Letter.l0, 0.99],
                      [Grade.g3, Letter.l1, 0.01]])

p_Joint = p_Letter_Grade * p_Grade_DifficultyIntelligence * p_Difficulty * p_Intelligence * p_Sat_Intelligence
p_Joint_no_Sat = p_Letter_Grade * p_Grade_DifficultyIntelligence * p_Difficulty * p_Intelligence

# d0        , g2   , i1          , l0    , s1  = 0.004608
assert p_Joint.query(Difficulty.d0, Grade.g2, Intelligence.i1, Letter.l0, Sat.s1) == Decimal('0.004608')
w_s1 = p_Joint.query(Difficulty.d0, Grade.g2, Intelligence.i1, Letter.l0, Sat.s1)
w_s0 = p_Joint.query(Difficulty.d0, Grade.g2, Intelligence.i1, Letter.l0, Sat.s0)
w = p_Joint_no_Sat.query(Difficulty.d0, Grade.g2, Intelligence.i1, Letter.l0) # == 0.00576
assert w == w_s1+w_s0, (w, w_s1 + w_s0)

print "Test"
# import pdb; pdb.set_trace()
assert p_Joint.query(Difficulty.d0, Grade.g2, Intelligence.i1, Letter.l0) == Decimal('0.00576')
