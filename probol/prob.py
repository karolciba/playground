"""Probabylity model:

Creating new model:
    p_ab = P('A,B')        # non-conditional
    p_xyz_ab = P('X,Y,Z|A,B')  # conditional

    or?

    p_ab = P(traffic=['yes','no'],weather=['rainy','sunny'])
    p_x_ab = P(late=['yes','no']).given(traffic=['yes','no'],weather=['rainy','sunny'])

    or?
    class Traffic(Enum):
        yes = auto(),
        no = auto()

    class Weather(Enum):
        rainy = auto(),
        cloudy = auto(),
        sunny = auto()

    class Late(Enum):
        yes = auto(),
        no = auto()

    p_TrafficWeather = P(Traffic,Weather)
    p_Late_TrafficWeather = P(Late).given(Traffic,Weather)


Defining:
    p_TrafficWeather.row(Traffic.yes,Weather.rainy, 0.5)
    p_TrafficWeather.table(
        [Traffic.yes, Weather.rainy, 0.5],
        [Traffic.yes, Weather.cloudy, 0.1],
        ...
        [Traffic.no, Weather.sunny, 0.01])


Operations:
    # Multiply conditional
    p_xab = p_x_ab * p_ab

    # Partial conditional
    p_xa = p_x_ab * p_a

    # Marginalize
    p_a = p_ab.sum(Weather)

    # set
    p_Traffic_cloudy = p_TrafficWheather(Weather.Cloudy)

    # renormalize
    p_Traffic_cloudy.normalize()

    # querying
    p_TrafficWeather[Traffic] -> table of p_Weather
    p_TrafficWeather[Traffic.yes] -> table of p_Weather | Traffic.yes
    p_TrafficWeather[Traffic.yes,Wather.sunny] -> probability

All operations should be possibly lazy ;)
"""

class P(object):
    from collections import namedtuple
    Row = namedtuple('row',['columns','conditions'])
    def __init__(self,*columns):
        self.columns = frozenset(columns)
        self.conditions = frozenset()
        self.rows = dict()
    def given(self,*conditions):
        self.conditions = frozenset(conditions)
        return self
    def row(self, *args):
        if len(args) == 1:
            args = args[0]
        probability = args[-1]
        args = args[:-1]
        # columns = set(a for a in args if type(a) in self.columns)
        # conditions = set(a for a in args if type(a) in self.conditions)
        # row = P.Row(frozenset(columns + conditions))
        key = frozenset(a for a in args)
        # import pdb; pdb.set_trace()
        self.rows[key] = probability
    def table(self, rows):
        for row in rows:
            self.row(row)
    def __getitem__(self, *keys):
        # import pdb; pdb.set_trace()
        if len(keys) == 1:
            keys = list(keys)
            pass
        else:
            # more keys
            pass
        return self._sum_over(keys)
    def normalize(self):
        whole = sum(v for v in self.rows.values())
        for k in self.rows:
            self.rows[k] /= whole
    def _sum_over(self, columns):
        from itertools import product, chain
        set_columns = self.columns - frozenset(columns)
        summed = []
        for s in set_columns:
            summed.extend(s)
        summed = set(summed)

        table = {}
        idx = list(product(*chain(columns,self.conditions)))
        for i in idx:
            table[frozenset(i)] = 0
        for k,v in self.rows.iteritems():
            i = k - summed
            table[i] += v

        p = P(set_columns).given(self.conditions)
        p.rows = table

        return p


if __name__ == "__main__":
    from enum import Enum

    class Traffic(Enum):
        yes = 1
        no = 2

    class Weather(Enum):
        rainy = 1
        cloudy = 2
        sunny = 3

    class Late(Enum):
        yes = 1
        no = 2


    class Failed(Enum):
        true = 1
        false = 2

    p_TrafficWeather = P(Traffic, Weather)
    p_TrafficWeather.table([ [Traffic.yes, Weather.rainy,  0.1],
                             [Traffic.yes, Weather.cloudy, 0.1],
                             [Traffic.yes, Weather.sunny,  0.2],
                             [Traffic.no,  Weather.rainy,  0.2],
                             [Traffic.no,  Weather.cloudy, 0.3],
                             [Traffic.no,  Weather.sunny,  0.1]])

    p_FailedLate_TrafficWeather = P(Late).given(Traffic, Weather)
    p_FailedLate_TrafficWeather.table([
            [Failed.true, Late.yes, Traffic.yes, Weather.rainy,  0.1],
            [Failed.true, Late.yes, Traffic.yes, Weather.cloudy, 0.1],
            [Failed.true, Late.yes, Traffic.yes, Weather.sunny,  0.2],
            [Failed.true, Late.yes, Traffic.no,  Weather.rainy,  0.2],
            [Failed.true, Late.yes, Traffic.no,  Weather.cloudy, 0.3],
            [Failed.true, Late.yes, Traffic.no,  Weather.sunny,  0.1],
            [Failed.true, Late.no,  Traffic.yes, Weather.rainy,  0.1],
            [Failed.true, Late.no,  Traffic.yes, Weather.cloudy, 0.1],
            [Failed.true, Late.no,  Traffic.yes, Weather.sunny,  0.2],
            [Failed.true, Late.no,  Traffic.no,  Weather.rainy,  0.2],
            [Failed.true, Late.no,  Traffic.no,  Weather.cloudy, 0.3],
            [Failed.true, Late.no,  Traffic.no,  Weather.sunny,  0.1],
            [Failed.false, Late.yes, Traffic.yes, Weather.rainy,  0.1],
            [Failed.false, Late.yes, Traffic.yes, Weather.cloudy, 0.1],
            [Failed.false, Late.yes, Traffic.yes, Weather.sunny,  0.2],
            [Failed.false, Late.yes, Traffic.no,  Weather.rainy,  0.2],
            [Failed.false, Late.yes, Traffic.no,  Weather.cloudy, 0.3],
            [Failed.false, Late.yes, Traffic.no,  Weather.sunny,  0.1],
            [Failed.false, Late.no,  Traffic.yes, Weather.rainy,  0.1],
            [Failed.false, Late.no,  Traffic.yes, Weather.cloudy, 0.1],
            [Failed.false, Late.no,  Traffic.yes, Weather.sunny,  0.2],
            [Failed.false, Late.no,  Traffic.no,  Weather.rainy,  0.2],
            [Failed.false, Late.no,  Traffic.no,  Weather.cloudy, 0.3],
            [Failed.false, Late.no,  Traffic.no,  Weather.sunny,  0.1]
    ])
    p_FailedLate_TrafficWeather.normalize()

    # print p_TrafficWeather[Weather]
    p_Failed_TrafficWeather = p_FailedLate_TrafficWeather[Failed]
