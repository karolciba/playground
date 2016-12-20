squresum = sum(range(1,101))**2
print squresum

sumsquares = sum( x**2 for x in xrange(1,101))
print sumsquares

print  squresum - sumsquares
