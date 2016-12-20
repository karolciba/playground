import inflect
import string

p = inflect.engine()


strs = [ p.number_to_words(n) for n in xrange(1,1001) ]

filtered = []
for s in strs:
    f = [ c for c in s if c in string.ascii_letters ]
    # print f
    filtered.extend(f)

print len(filtered)


