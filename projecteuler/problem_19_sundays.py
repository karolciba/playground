def datesgen(day_of_week, day, month, year):
    """ 1 Jan 1900 was a Monday.
    Thirty days has September,
    April, June and November.
    All the rest have thirty-one,
    Saving February alone,
    Which has twenty-eight, rain or shine.
    And on leap years, twenty-nine.
    A leap year occurs on any year evenly divisible by 4, but not on a century unless it is divisible by 400.
    [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
      1   2   3   4   5   6   7   8   9  10  11  12
    """
    from itertools import count
    from collections import namedtuple
    date = namedtuple('Date', ['day_of_week', 'day', 'month', 'year' ])
    yield date(day_of_week, day, month, year)
    for x in count():
        day_of_week = (day_of_week + 1) % 7
        day += 1
        if month in [1, 3, 5, 7, 8, 10, 12] and day == 32:
            day = 1
            month += 1
            if month == 13:
                month = 1
                year += 1
        elif month in [4, 6, 9, 11] and day == 31:
            day = 1
            month += 1
        elif month == 2:
            if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0) and day == 30:
                print "yes"
                day = 1
                month += 1
            elif year % 4 != 0 and day == 29:
                print "no"
                day = 1
                month += 1
        yield date(day_of_week, day, month, year)


def test():
    import datetime

    g = datesgen(0,1,1,1900)
    d = datetime.datetime(1900,1,1)

    end = datetime.datetime(2000, 12, 31)

    day = datetime.timedelta(1)

    while d <= end:
        tup = g.next()
        if tup.day_of_week != d.weekday() or tup.day != d.day or tup.month != d.month or tup.year != d.year:
            raise BaseException("Times differ expected %s got %s " % (d, tup))
        d += day

import datetime

sundays = 0
g = datesgen(0,1,1,1900)
d = datetime.datetime(1901,1,1)
day = datetime.timedelta(1)

while True:
    d += day
    if d.weekday() == 6 and d.day == 1:
        sundays += 1
    if d.day == 31 and d.month == 12 and d.year == 2000:
        break

print sundays

sundays = 0
for year in range(1901,2001):
    for month in range(1, 13):
        d = datetime.date(year,month,1)
        if d.weekday() == 6:
            sundays += 1

print sundays
