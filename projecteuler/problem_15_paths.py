import euler

rows = 1000
cols = rows

print "Binominal"
def binom():
    return euler.binominal(rows+cols,rows)

print binom()

print "Dynamic"

def dyn():
    grid = {}
    grid[0,1] = 1
    grid[1,0] = 1

    for column in xrange(1,rows+1):
        grid[0,column] = 1
        grid[column,0] = 1

    for row in xrange(1,rows+1):
        for column in xrange(1,rows+1):
            grid[row,column] = grid[row-1,column] + grid[row,column-1]

    return grid[rows,cols]

print dyn()
