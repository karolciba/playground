class Specimen:

    _alleles = ( 'AA', 'AB', 'BA', 'A0', 'BB', 'B0', '00', '0A', '0B' )

    _phenotypes = ( 'A', 'B', 'AB', '0' )

    _phenotype_probability = { 'A' : 0.43,
                   'B' : 0.11,
                   'AB': 0.04,
                   '0' : 0.42 }

    _allele_given_phenotype = {
            'AB' : { 'AA': 0, 'A0': 0, '0A': 0,
                    'BB': 0, 'B0': 0, '0B': 0,
                    'AB': .5, 'BA': .5,
                    '00': 0 },
            'A' : { 'AA': 1./3, 'A0': 1./3, '0A': 1./3,
                    'BB': 0, 'B0': 0, '0B': 0,
                    'AB': 0, 'BA': 0,
                    '00': 0 },
            'B' : { 'AA': 0, 'A0': 0, '0A': 0,
                    'BB': 1./3, 'B0': 1./3, '0B': 1./3,
                    'AB': 0, 'BA': 0,
                    '00': 0 },
            '0' : { 'AA': 0, 'A0': 0, '0A': 0,
                    'BB': 0, 'B0': 0, '0B': 0,
                    'AB': 0, 'BA': 0,
                    '00': 1 }
            }

    def __init__(self, name):
        self._name = name
        self._alleles = Specimen._alleles
        self._phenotypes = Specimen._phenotypes
        self._phenotype_probability = Specimen._phenotype_probability
        self._allele_probability = { key: 0 for key in self._alleles }
        self._parents = []
        self._children = []
        self._calculate_allele_probability()

    def set_phenotype(self, phenotype):
        for key in self._phenotype_probability.keys():
            if key == phenotype:
                self._phenotype_probability[key] = 1
            else:
                self._phenotype_probability[key] = 0

    def add_parent(self, parent):
        self._parents.append(parent)
        parent._children.append(self)

    def add_child(self, child):
        self._children.append(child)
        child._parents.append(self)

    def _calculate_allele_probability(self):
        self._allele_probability = { key: 0 for key in self._alleles }
        for phenotype, phenotype_probability in self._phenotype_probability.items():
            print phenotype, phenotype_probability
            bayes = self._allele_given_phenotype[phenotype]
            print bayes
            for allele, probability in bayes.items():
                print "allele %s = probability %s * phenotype_p %s" % (allele, probability, phenotype_probability)
                self._allele_probability[allele] += probability * phenotype_probability
        print
        print self._allele_probability
        return self._allele_probability


class Matrix:
    def __init__(self):
        pass
