from euler import *

count = 0
for r in pengen([0,1,2,3,4]):

    for i,p in enumerate(r):
        if i == p:
            count += 1
            break

print count

