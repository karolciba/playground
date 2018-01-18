from collections import defaultdict
import matplotlib.pyplot as plt
from itertools import product
plt.ion()
# node = (dot,N,NW,W,SW,S,SE,E,NE)
O = 0
N = 1
NW = 2
W = 3
SW = 4
S = 5
SE = 6
E = 7
NE = 8

def dot():
    return [True,None,None,None,None,None,None,None,None]

def empty():
    return [None,None,None,None,None,None,None,None,None]

space = { (0,3): dot(),
          (0,4): dot(),
          (0,5): dot(),
          (0,6): dot(),
          (1,3): dot(),
          (1,6): dot(),
          (2,3): dot(),
          (2,6): dot(),
          (3,0): dot(),
          (3,1): dot(),
          (3,2): dot(),
          (3,3): dot(),
          (3,6): dot(),
          (3,7): dot(),
          (3,8): dot(),
          (3,9): dot(),
          (4,0): dot(),
          (4,9): dot(),
          (5,0): dot(),
          (5,9): dot(),
          (6,0): dot(),
          (6,1): dot(),
          (6,2): dot(),
          (6,3): dot(),
          (6,6): dot(),
          (6,7): dot(),
          (6,8): dot(),
          (6,9): dot(),
          (7,3): dot(),
          (7,6): dot(),
          (8,3): dot(),
          (8,6): dot(),
          (9,3): dot(),
          (9,4): dot(),
          (9,5): dot(),
          (9,6): dot()}

def copy(space):
    cp = { k: v[:] for k,v in space.items() }
    return cp

def visualize(space):
    plt.clf()
    dots = space.keys()
    x = [p[0] for p in dots]
    y = [p[1] for p in dots]

    for key,value in space.items():
        for c in value[1:]:
            if c:
                plt.plot((key[0],c[0]),(key[1],c[1]), 'ro-')

    plt.plot(x,y,'o')


def checkset(DF,DT,points,space):
    p0 = points[0]
    p1 = points[1]
    p2 = points[2]
    p3 = points[3]
    p4 = points[4]
    p5 = points[5]
    p6 = points[6]

    # import pdb; pdb.set_trace()
    if p1 not in space or p2 not in space or p3 not in space or p4 not in space or p5 not in space:
        return False

    if p0 in space:
        if space[p0][DF] or space[p1][DT]:
               return False

    if p6 in space:
        if space[p5][DF] or space[p6][DT]:
                return False

    if space[p1][DF] or space[p2][DT]:
           return False
    if space[p2][DF] or space[p3][DT]:
           return False
    if space[p3][DF] or space[p4][DT]:
           return False
    if space[p4][DF] or space[p5][DT]:
           return False

    space[p1][DF] = p2
    space[p2][DT] = p1
    space[p2][DF] = p3
    space[p3][DT] = p2
    space[p3][DF] = p4
    space[p4][DT] = p3
    space[p4][DF] = p5
    space[p5][DT] = p4

    return True


def valid(coord,space):
    # can input dot?
      # no - not valid
    valids = []
    if coord in space:
        return valids

    # E - W
    for after in range(0,6):
        before = -5 + after
        dots = list(zip(range(before + coord[0],after+2 + coord[0]), [coord[1]]*7))
        cp = copy(space)
        cp[coord] = dot()
        if checkset(E,W,dots,cp):
            valids.append(cp)

    # N - S
    for after in range(0,6):
        before = -5 + after
        dots = list(zip([coord[0]]*7, range(before + coord[1],after+2 + coord[1])))
        cp = copy(space)
        cp[coord] = dot()
        if checkset(N,S,dots,cp):
            valids.append(cp)

    # NE - SW
    for after in range(0,6):
        before = -5 + after
        dots = list(zip(range(before + coord[0],after+2 + coord[0]),range(before + coord[1],after+2 + coord[1])))
        cp = copy(space)
        cp[coord] = dot()
        if checkset(NE,SW,dots,cp):
            valids.append(cp)

    # NW - SE
    for after in range(0,6):
        before = -5 + after
        dots = list(zip(range(before + coord[0],after+2 + coord[0]),range(after+2 + coord[1],before + coord[1],-1)))
        # print(dots)
        cp = copy(space)
        cp[coord] = dot()
        if checkset(NE,SW,dots,cp):
            valids.append(cp)

    # print(valids)

    return valids

def avail(space):
    dots = space.keys()

    neigh = set()
    for dot in dots:
        neigh.add( (dot[0]-1,dot[1]-1) )
        neigh.add( (dot[0]-1,dot[1]) )
        neigh.add( (dot[0]-1,dot[1]+1) )
        neigh.add( (dot[0],dot[1]-1) )
        neigh.add( (dot[0],dot[1]) )
        neigh.add( (dot[0],dot[1]+1) )
        neigh.add( (dot[0]+1,dot[1]-1) )
        neigh.add( (dot[0]+1,dot[1]) )
        neigh.add( (dot[0]+1,dot[1]+1) )

    candidates = set([n for n in neigh if n not in space])

    return candidates

def extend(cand,coord,space):
    neigh = set([n for n in cand if n not in space])

    neigh.add( (coord[0]-1,dot[1]-1) )
    neigh.add( (coord[0]-1,dot[1]) )
    neigh.add( (coord[0]-1,dot[1]+1) )
    neigh.add( (coord[0],dot[1]-1) )
    neigh.add( (coord[0],dot[1]) )
    neigh.add( (coord[0],dot[1]+1) )
    neigh.add( (coord[0]+1,dot[1]-1) )
    neigh.add( (coord[0]+1,dot[1]) )
    neigh.add( (coord[0]+1,dot[1]+1) )

    candidates = set([n for n in neigh if n not in space])
    return candidates

from heapq import *

def prir2(space, depth=0):

    queue = []
    counter = 0
    moves = avail(space)
    heappush(queue, (0, counter, space, moves))

    total_best = 0
    total_space = space

    while queue:
        depth, _, space, moves = heappop(queue)

        options = []
        for move in moves:
            # options.extend(valid(move,space))
            ns = valid(move,space)
            pair = ns, extend(moves,move,ns)
            options.extend(valid(move,space))

        for o,m in options:
            print("Depth {} best {}".format(depth, total_best), end="\r")
            counter += 1
            heappush(queue,(depth+1,counter,o,m))
        if True or depth > total_best:
            total_best = depth
            plt.pause(.0001)
            visualize(o)


def prir(space, depth=0):

    queue = []
    counter = 0
    heappush(queue, (0, counter, space))
    plt.ion()

    total_best = 0
    total_space = space

    while queue:
        depth, _, space = heappop(queue)

        moves = avail(space)
        options = []
        for move in moves:
            options.extend(valid(move,space))

        for o in options:
            print("Depth {} best {}".format(depth, total_best), end="\r")
            counter += 1
            heappush(queue,(depth+1,counter,o))
        if True or depth > total_best:
            total_best = depth
            # plt.pause(.0001)
            visualize(o)


total_best = 0
total_s = None
def solve(space, depth=0):

    global total_best
    moves = avail(space)
    options = []
    for move in moves:
        options.extend(valid(move,space))

    best_d = depth
    best_s = space

    for o in options:
        print("Depth {} iter best {} total best {}".format(depth, best_d, total_best), end="\r")
        s, d = solve(o, depth+1)
        # plt.pause(.0001)
        # visualize(best_s)
        if d > best_d:
            best_d = d
            best_s = s

        if best_d > total_best:
            total_best = best_d
            total_s = best_s
            visualize(best_s)
            plt.pause(.01)

    return best_s, best_d
