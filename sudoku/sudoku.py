#!/usr/bin/env python
import numpy as np
class State:
    def __init__(self, init=True, board=None):
        if init:
            values = range(1,10)
            # self.nodes = [[set(values) for x in range(0,9)] for y in range(0,9)]
            self.nodes = { (x,y): set(values) for x in range (1,10) for y in range(1,10)}
            if board:
                for i in range(1,10):
                    for j in range(1,10):
                        el = board[i-1][j-1]
                        if el >=1 and el <=9:
                            self.assign((i,j), el)
        else:
            self.nodes = {}
    def assign(self, pos, value):
        if value >= 0 and value <= 9:
            self.nodes[pos] = set([value])
    def clone(self):
        s = State(False)
        for key,value in self.nodes.items():
            s.nodes[key] = set(value)
        return s
    def __str__(self):
        string = ""
        left = 9*9
        for i in range(1,10):
            for j in range(1,10):
                values = self.nodes[i,j]
                if len(values) == 1:
                    string += str(list(self.nodes[i,j])[0])
                    left -= 1
                elif len(values) == 0:
                    string += "x"
                else:
                    string += " "
            string += "\n"
        return string + " left " + str(left)

def nonempty(values):
    if len(values) == 0:
        return False
    return True

def different(left, right):
    if len(left) > 1 or len(right) > 1:
        return True
    return left.isdisjoint(right)

def prune(assigment, values):
    values-={assigment}
    if len(values) == 0:
        return False
    return True

class Sudoku:
    def __init__(self):
        self.constraints = []
        self.prunes = {}
        # for pos,value in board.values():
        #     self.state.nodes[pos] = set([value])
        # each node must have value
        for i in range(1,10):
            for j in range(1,10):
                self.add_constraint(nonempty,[(i,j)])
        # no two nodes in row can have same values
        for i in range(1,10):
            for j in range(1,10):
                left = (i,j)
                for k in range(j+1,10):
                    right = (i,k)
                    self.add_constraint(different,[left, right])
                    self.add_prune(prune, left, right)
        # no two nodes in columnt can have same values
        for i in range(1,10):
            for j in range(1,10):
                top = (j,i)
                for k in range(j+1,10):
                    bottom = (k,i)
                    self.add_constraint(different,[top, bottom])
                    self.add_prune(prune, top, bottom)
        for x in range(0,9,3):
            for y in range(0,9,3):
                subs = []
                for i in range(1,4):
                    for j in range(1,4):
                        subs.append((x+i,y+j))
                for i in range(len(subs)):
                    for j in range(i+1, len(subs)):
                        self.add_constraint(different,(subs[i],subs[j]))
                        self.add_prune(prune, subs[i], subs[j])
    def add_constraint(self, constraint, nodes):
        self.constraints.append((constraint, nodes))
    def add_prune(self, constraint, left, right):
        if left in self.prunes:
            self.prunes[left].append( (constraint, right) )
        else:
            self.prunes[left] = [ (constraint, right) ]
        if right in self.prunes:
            self.prunes[right].append( (constraint, left) )
        else:
            self.prunes[right] = [ (constraint, left) ]
    def assign(self, state, pos, value):
        state.assign(pos,value)
        for func,other in self.prunes[pos]:
            func(value, state.nodes[other])
    def check(self, state):
        for con,pos_list in self.constraints:
            values = [ state.nodes[pos] for pos in pos_list ]
            if not con(*values):
                # print "Failed condition on ", con, values, pos_list
                return False
        return True

class Brute:
    def __init__(self, board):
        self.sudoku = Sudoku()
        self.state = State(board=board)
        self.visited = 0

    def solve(self):

        def findavail(state):
            for key,values in state.nodes.items():
                if len(values) > 1:
                    return key, values
            return None, None

        fringe = [ self.state ]
        flen = 1

        while fringe:
            state = fringe.pop()
            flen -= 1
            if self.visited % 1000 == 0:
                print "Checking state %d (len %d)" % (self.visited, flen)
                print state,
                print "\033[11A"
            self.visited += 1
            key, avail = findavail(state)
            # all values set
            if not avail:
                # check if solves sudoku
                # import pdb; pdb.set_trace()
                solved = self.sudoku.check(state)
                if solved:
                    # solves sudoku
                    return state
                else:
                    # doesn't solve, discard
                    continue
            for value in avail:
                clone = state.clone()
                clone.nodes[key] = { value }
                fringe.append(clone)
                flen += 1

        # no solution exists
        return None

def findbestavail(state):
    best_score = 10
    best_match = None, None
    for key,values in state.nodes.items():
        if len(values) < best_score and len(values) > 1:
            best_score = len(values)
            best_match =  key, values
    return best_match

def findavail(state):
    for key,values in state.nodes.items():
        if len(values) > 1:
            return key, values
    return None, None

availstrategy = findbestavail

class Filter:
    def __init__(self, board):
        self.sudoku = Sudoku()
        self.state = State(board=board)
        self.visited = 0

    def solve(self):

        fringe = [ self.state ]
        flen = 1

        while fringe:
            state = fringe.pop()
            flen -= 1

            print "Checking state %d (len %d)" % (self.visited, flen)
            print state,
            print "\033[11A"

            self.visited += 1
            key, avail = availstrategy(state)
            # all values set
            if not avail:
                # check if solves sudoku
                # import pdb; pdb.set_trace()
                solved = self.sudoku.check(state)
                if solved:
                    # solves sudoku
                    return state
                else:
                    # doesn't solve, discard
                    continue
            for value in avail:
                clone = state.clone()
                clone.nodes[key] = { value }
                if self.sudoku.check(clone):
                    fringe.append(clone)
                    flen += 1

        # no solution exists
        return None

class Forward:
    def __init__(self, board):
        self.sudoku = Sudoku()
        self.state = State()
        if board:
            for i in range(1,10):
                for j in range(1,10):
                    el = board[i-1][j-1]
                    if el != 0:
                        # self.state.assign((i,j), el)
                        self.sudoku.assign(self.state,(i,j), el)

        self.visited = 0

    def solve(self):
        fringe = [ self.state ]
        flen = 1

        print "Start state %d (len %d)" % (self.visited, flen)
        print self.state

        while fringe:
            state = fringe.pop()
            flen -= 1
            # if self.visited % 1000 == 0:

            print "\033[12A"
            print "Checking state %d (len %d)" % (self.visited, flen)
            print state

            self.visited += 1
            key, avail = availstrategy(state)
            # all values set
            if not avail:
                # check if solves sudoku
                # import pdb; pdb.set_trace()
                solved = self.sudoku.check(state)
                if solved:
                    # solves sudoku
                    return state
                else:
                    # doesn't solve, discard
                    continue
            for value in avail:
                clone = state.clone()
                self.sudoku.assign(clone, key, value)
                # clone.nodes[key] = { value }
                if self.sudoku.check(clone):
                    fringe.append(clone)
                    flen += 1

        # no solution exists
        return None

simple = [[5,3,0,0,7,0,0,0,0],
         [6,0,0,1,9,5,0,0,0],
         [0,9,8,0,0,0,0,6,0],
         [8,0,0,0,6,0,0,0,3],
         [4,0,0,8,0,3,0,0,1],
         [7,0,0,0,2,0,0,0,6],
         [0,6,0,0,0,0,2,8,0],
         [0,0,0,4,1,9,0,0,5],
         [0,0,0,0,8,0,0,7,9]]

solved = [[5,3,4,6,7,8,9,1,2],
          [6,7,2,1,9,5,3,4,8],
          [1,9,8,3,4,2,5,6,7],
          [8,5,9,7,6,1,4,2,3],
          [4,2,6,8,5,3,7,9,1],
          [7,1,3,9,2,4,8,5,6],
          [9,6,1,5,3,7,2,8,4],
          [2,8,7,4,1,9,6,3,5],
          [3,4,5,2,8,6,1,7,9]]

test = [[0,0,4,6,7,8,9,1,2],
        [6,7,2,1,0,5,3,4,8],
        [1,9,8,3,4,2,5,6,7],
        [8,5,9,0,6,1,4,2,3],
        [4,2,6,8,5,3,7,9,1],
        [7,0,3,9,2,4,8,5,6],
        [9,6,1,5,3,7,2,8,4],
        [2,8,7,4,1,9,6,3,5],
        [3,4,5,2,8,6,1,7,9]]

hard = [[0,0,8,3,2,0,0,0,4],
        [1,0,0,4,0,0,0,7,0],
        [0,0,0,0,0,0,9,3,0],
        [0,0,6,2,0,0,7,0,3],
        [0,0,0,0,0,0,0,0,0],
        [9,0,1,0,0,3,2,0,0],
        [0,9,7,0,0,0,0,0,0],
        [0,5,0,0,0,8,0,0,9],
        [2,0,0,0,6,5,4,0,0]]

evil = [[7,2,5,0,4,0,0,0,0],
        [0,0,6,9,7,0,0,1,0],
        [0,0,0,0,0,0,0,3,0],
        [0,0,0,0,3,4,0,0,8],
        [0,0,9,0,0,0,4,0,0],
        [8,0,0,6,1,0,0,0,0],
        [0,5,0,0,0,0,0,0,0],
        [0,9,0,0,6,8,5,0,0],
        [0,0,0,0,2,0,6,7,9]]

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print "Provide solver name (brute|filter|forward) [filename] [best|first]"
        sys.exit(1)

    board = simple
    if len(sys.argv) >= 3:
        board = [ [0 for x in range(1,10)] for y in range(1,10) ]
        row = 0
        col = 0
        with open(sys.argv[2]) as f:
            content = f.readlines()
            for line in content:
                for char in line:
                    # print row, char,
                    v = ord(char) - 48
                    if v < 0 or v > 9:
                        v = 0
                    board[col][row] = v
                    row += 1
                    if (row == 9):
                        break
                # print "next"
                col += 1
                row = 0
                if col == 9:
                    break


    if len(sys.argv) == 4:
        if sys.argv[3] == 'best':
            availstrategy = findbestavail
        elif sys.argv[3] == 'first':
            availstrategy = findavail

    if sys.argv[1] == 'brute':
        b = Brute(board)
        solved = b.solve()
        print solved
    elif sys.argv[1] == 'filter':
        f = Filter(board)
        solved = f.solve()
        print solved
    elif sys.argv[1] == 'forward':
        f = Forward(board)
        # import pdb; pdb.set_trace()
        solved = f.solve()
        print solved
    else:
        print "Provide solver name [brute|filter|forward]"
