"""
Phenotype: 0, A, B, AB
Genotype: 00, A0, 0A, AA, B0, 0B, BB, AB

Populacja   0Rh+    ARh+    BRh+    ABRh+   0Rh-    ARh-    BRh-    ABRh-
Polska[9]   31% 32% 15% 7%  6%  6%  2%  1%
P(P, Rh):
    0  +  .31
    A  +  .32
    B  +  .15
    AB +  .07
    O  -  .06
    A  -  .06
    B  -  .02
    AB -  .01

P(P):
    0   .37
    A   .38
    B   .17
    AB  .08

P(P | G):
    0  00  1
    A  A0  1
    A  0A  1
    A  AA  1
    B  B0  1
    B  0B  1
    B  BB  1
    AB AB  1
    .. ..  0

P(P,G) = P(P|G)*P(G)
P(P,G) = P(G|P)*P(P)
"""



