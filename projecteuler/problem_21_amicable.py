import euler

facts = [ euler.propfactors(x) for x in xrange(0,10001) ]

sums = [ sum(f) for f in facts ]


amicable = 0
for i,s in enumerate(sums,0):
    if i == 0:
        continue
    if s < len(sums):
        print i,s,sums[s]
        if sums[s] == s:
            amicable += 1


print amicable
