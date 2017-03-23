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
    p_x_b = p_x_ab * p_a

    # Marginalize
    # p_a = p_ab.sum(Weather)

    # set
    # p_Traffic_cloudy = p_TrafficWheather(Weather.Cloudy)

    # renormalize
    p_Traffic_cloudy.normalize()

    # querying
    p_TrafficWeather[Traffic] -> marginalize, table of p_Weather
    p_TrafficWeather[Traffic.yes] -> table of Traffic.yes | rest
    p_TrafficWeather[Traffic.yes,Wather.sunny] -> probability

All operations should be possibly lazy ;)
"""

class P(object):
    from collections import namedtuple
    Row = namedtuple('row',['columns','conditions'])
    def __init__(self,*columns):
        self.columns = frozenset(columns)
        self.conditions = frozenset()
        self.variables = self.columns
        self.rows = dict()
        self.default = 0.0
    def given(self,*conditions):
        self.conditions = frozenset(conditions)
        self.variables = self.columns.union(self.conditions)
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
        if any(c for c in key if type(c) not in self.variables):
            raise Exception("Column {} not in defined set {}".format(key,self.columns))
        # import pdb; pdb.set_trace()
        self.rows[key] = probability
    def table(self, rows):
        for row in rows:
            self.row(row)

    def normalize(self):
        if self.conditions:
            from itertools import product, chain
            cond = product(*self.conditions)
            for c in cond:
                print c
                whole = sum(v for k,v in self.rows.iteritems() if set(c).issubset(k))
                if whole == 0:
                    continue
                for k in self.rows:
                    if set(c).issubset(k):
                        self.rows[k] /= whole
        else:
            whole = sum(v for v in self.rows.values())
            for k in self.rows:
                self.rows[k] /= whole
        return self

    def __str__(self):
        columns = sorted(list(self.columns), key=lambda x: x.__name__)
        s = ", ".join(c.__name__ for c in columns)
        conditions = sorted(list(self.conditions), key=lambda x: x.__name__)
        if conditions:
            s += " | "
            s += ", ".join(c.__name__ for c in conditions)

        col_sizes = [len(c.__name__) for c in columns]
        con_sizes = [len(c.__name__) for c in conditions]
        pipe_pos = len(columns)

        s += "\n"

        from itertools import product, chain
        for k in product(*chain(columns,conditions)):
            prob = self[frozenset(k)]
            if prob == 0.0:
                continue
            for i,x in enumerate(k):
                if i < pipe_pos:
                    s += "{0: <{1}}".format(x.name,col_sizes[i])
                elif i == pipe_pos:
                    s = s[:-2]
                    s += " | "
                    s += "{0: <{1}}".format(x.name,con_sizes[i-pipe_pos])
                else:
                    s += "{0: <{1}}".format(x.name,con_sizes[i-pipe_pos])
                s += ", "
            s = s[:-2]
            s += " = " + str(prob)
            s += "\n"
            # vals = [x.name for x in k]
            # s += ", ".join(vals)
            # # prob = self.rows[frozenset(k)]
            # prob = self[frozenset(k)]
            # s += " = " + str(prob)
            # s += "\n"

        return s

    def __mul__(self, other):
        """Solves P(A|B) * p(B) or vice versa"""
        from itertools import product, chain
        columns = self.columns.union(other.columns)
        conditions = self.conditions.union(other.conditions)
        conditions = conditions - columns

        p = P(*list(columns)).given(*list(conditions))

        for k in product(*p.variables):
            prob = self._query(k) * other._query(k)
            args = list(k)
            args.append(prob)
            p.row(*args)

        return p

        if any(c for c in other.conditions if c in self.columns):
            return other.__mul__(self)
        elif any(c for c in self.conditions if c in other.columns):
            from itertools import product, chain
            columns = self.columns.union(other.columns)
            conditions = self.conditions.union(other.conditions)
            conditions = conditions - columns

            p = P(*list(columns)).given(*list(conditions))

            for k in product(*p.variables):
                prob = self._query(k) * other._query(k)
                args = list(k)
                args.append(prob)
                p.row(*args)

            return p
        else:
            raise Exception("Parameters {} and conditions {} mismatch"\
                            .format(self.columns,other.conditions))

    def __div__(self, other):
        from itertools import product, chain
        p = P(*list(self.columns - other.columns)).given(*chain(list(other.columns),list(self.conditions),list(other.conditions)))
        for k in self.rows:
            num = self._query(k)
            den = other._query(k)
            print k, num, "/", den
            p.rows[k] = self._query(k) / other._query(k)
        return p

    def __getitem__(self, keys):
        # Query for maginalization
        if any(c for c in keys if c not in self.variables):
            return self._query(keys)
        else:
            return self._sum_over(keys)

    def _query(self,keys):
        filtered_keys = frozenset(k for k in keys if type(k) in self.variables)
        ret = self.rows.get(filtered_keys)
        return ret or self.default

    def _marginalize(self, columns):
        from itertools import product, chain

        table = {}
        for k in product(*columns):
            print k

    def _sum_over(self, columns):
        from itertools import product, chain
        rest_columns = self.columns - frozenset(columns)
        summed = []
        for s in rest_columns:
            summed.extend(s)
        summed = set(summed)

        table = {}
        idx = list(product(*chain(columns,self.conditions)))
        for i in idx:
            table[frozenset(i)] = 0
        for k,v in self.rows.iteritems():
            i = k - summed
            table[i] += v

        p = P(rest_columns).given(self.conditions)
        p.rows = table


        return p


if __name__ == "__main__":
    from enum import Enum

    class Test(Enum):
        A = 1
        B = 2

    class Cond(Enum):
        T = 1
        F = 2

    p_Test = P(Test)
    p_Test.table( [[Test.A, 0.3],
                   [Test.B, 0.7]])

    p_Cond = P(Cond)
    p_Cond.table( [[Cond.T, 0.4],
                   [Cond.F, 0.6]])

    p_CondTest = P(Test,Cond)
    p_CondTest.table( [[Test.A, Cond.T, 0.1],
                       [Test.A, Cond.F, 0.2],
                       [Test.B, Cond.T, 0.3],
                       [Test.B, Cond.F, 0.4]])

    p_Test_Cond = P(Test).given(Cond)
    p_Test_Cond.table( [[Test.A, Cond.T, 0.50],
                        [Test.B, Cond.T, 1.5],
                        [Test.A, Cond.F, 0.33],
                        [Test.B, Cond.F, 0.67]])

    p_Cond_Test = P(Cond).given(Test)
    p_Cond_Test.table( [[Cond.T, Test.A, 0.33],
                        [Cond.F, Test.A, 0.67],
                        [Cond.T, Test.B, 0.3/0.7],
                        [Cond.F, Test.B, 0.4/0.7]])
    # from enum import Enum
    #
    # import vimpdb; vimpdb.hookPdb()
    # class Traffic(Enum):
    #     yes = 1
    #     no = 2
    #
    # class Weather(Enum):
    #     rainy = 1
    #     cloudy = 2
    #     sunny = 3
    #
    # class Late(Enum):
    #     yes = 1
    #     no = 2
    #
    #
    # class Failed(Enum):
    #     true = 1
    #     false = 2
    #
    # p_Late = P(Late)
    # p_Late.table( [[Late.yes, 0.1],
    #                [Late.no,  0.9]])
    #
    # p_Failed = P(Failed)
    # p_Failed.table( [[Failed.true, 0.4],
    #                  [Failed.false,  0.6]])
    #
    # print "Declare p_Weather"
    # p_Weather = P(Weather)
    # p_Weather.table( [[Weather.rainy, 0.2],
    #                   [Weather.cloudy, 0.3],
    #                   [Weather.sunny, 0.5]])
    #
    # print "Declare p_Traffic_Weather"
    # p_Traffic_Weather = P(Traffic).given(Weather)
    # p_Traffic_Weather.table([ [Traffic.yes, Weather.rainy,  0.1],
    #                          [Traffic.yes, Weather.cloudy, 0.1],
    #                          [Traffic.yes, Weather.sunny,  0.2],
    #                          [Traffic.no,  Weather.rainy,  0.2],
    #                          [Traffic.no,  Weather.cloudy, 0.3],
    #                          [Traffic.no,  Weather.sunny,  0.1]])
    #
    # print "p_TrafficWeather = p_Traffic_Weather * p_Weather"
    # p_TrafficWeather = p_Traffic_Weather * p_Weather
    #
    # p_joint = p_TrafficWeather * p_Failed * p_Late
    #
    #
    # # # p_TrafficWeather = P(Traffic, Weather)
    # # # p_TrafficWeather.table([ [Traffic.yes, Weather.rainy,  0.1],
    # # #                          [Traffic.yes, Weather.cloudy, 0.1],
    # # #                          [Traffic.yes, Weather.sunny,  0.2],
    # # #                          [Traffic.no,  Weather.rainy,  0.2],
    # # #                          [Traffic.no,  Weather.cloudy, 0.3],
    # # #                          [Traffic.no,  Weather.sunny,  0.1]])
    # #
    # p_FailedLate_TrafficWeather = P(Failed,Late).given(Weather,Traffic)
    # p_FailedLate_TrafficWeather.table([
    #         [Failed.true, Late.yes, Traffic.yes, Weather.rainy,  0.1],
    #         [Failed.true, Late.yes, Traffic.yes, Weather.cloudy, 0.1],
    #         [Failed.true, Late.yes, Traffic.yes, Weather.sunny,  0.2],
    #         [Failed.true, Late.yes, Traffic.no,  Weather.rainy,  0.2],
    #         [Failed.true, Late.yes, Traffic.no,  Weather.cloudy, 0.3],
    #         [Failed.true, Late.yes, Traffic.no,  Weather.sunny,  0.1],
    #         [Failed.true, Late.no,  Traffic.yes, Weather.rainy,  0.1],
    #         [Failed.true, Late.no,  Traffic.yes, Weather.cloudy, 0.1],
    #         [Failed.true, Late.no,  Traffic.yes, Weather.sunny,  0.2],
    #         [Failed.true, Late.no,  Traffic.no,  Weather.rainy,  0.2],
    #         [Failed.true, Late.no,  Traffic.no,  Weather.cloudy, 0.3],
    #         [Failed.true, Late.no,  Traffic.no,  Weather.sunny,  0.1],
    #         [Failed.false, Late.yes, Traffic.yes, Weather.rainy,  0.1],
    #         [Failed.false, Late.yes, Traffic.yes, Weather.cloudy, 0.1],
    #         [Failed.false, Late.yes, Traffic.yes, Weather.sunny,  0.2],
    #         [Failed.false, Late.yes, Traffic.no,  Weather.rainy,  0.2],
    #         [Failed.false, Late.yes, Traffic.no,  Weather.cloudy, 0.3],
    #         [Failed.false, Late.yes, Traffic.no,  Weather.sunny,  0.1],
    #         [Failed.false, Late.no,  Traffic.yes, Weather.rainy,  0.1],
    #         [Failed.false, Late.no,  Traffic.yes, Weather.cloudy, 0.1],
    #         [Failed.false, Late.no,  Traffic.yes, Weather.sunny,  0.2],
    #         [Failed.false, Late.no,  Traffic.no,  Weather.rainy,  0.2],
    #         [Failed.false, Late.no,  Traffic.no,  Weather.cloudy, 0.3],
    #         [Failed.false, Late.no,  Traffic.no,  Weather.sunny,  0.1]
    # ])
    # # p_FailedLateTraffic_Weather.normalize()
    # #
    # # # print p_TrafficWeather[Weather]
    # # # p_FailedLate_Weather = p_FailedLateTraffic_Weather[Failed,Late]
    # # p_Failed_Weather = p_FailedLateTraffic_Weather[Failed]
