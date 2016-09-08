#!/usr/bin/env python

class State:
    def __init__(self, board = None, init = True):
        if init:
            import random
            self.nodes = [[random.randint(1,9) for x in range(0,10)] for y in range(0,10)]
            self.locked = [[False for x in range(0,10)] for y in range(0,10)]
            self.free = [(x,y) for x in range(1,10) for y in range(1,10)]
            if board:
                for i in range(1,10):
                    for j in range(1,10):
                        el = board[i-1][j-1]
                        if el >= 1 and el <= 9:
                            self.nodes[i][j] = el
                            self.locked[i][j] = True
                            self.free.remove((i,j))
        else:
            self.nodes = None
            self.locked = None
            self.free = None

    def error(self):
        error = 0
        for i in range(1,10):
            values = set()
            for j in range(1,10):
                v = self.nodes[i][j]
                values.add(v)
            error += 9 - len(values)
        for i in range(1,10):
            values = set()
            for j in range(1,10):
                v = self.nodes[j][i]
                values.add(v)
            error += 9 - len(values)
        for x in range(0,9,3):
            for y in range(0,9,3):
                values = set()
                for i in range(1,4):
                    for j in range(1,4):
                        row = x + i
                        col = y + j
                        v = self.nodes[row][col]
                        values.add(v)
                error += 9 - len(values)
        return error

    def clone(self):
        s = State(None, None)
        s.free = self.free
        s.locked = self.locked
        s.nodes = []
        for i in range(len(self.nodes)):
            s.nodes.append(list(self.nodes[i]))
        return s

    def __str__(self):
        string = ""
        for i in range(1,10):
            for j in range(1,10):
                value = self.nodes[i][j]
                if self.locked[i][j]:
                    string += "\033[1m"
                if value in range(1,10):
                    string += str(value)
                else:
                    string += " "
                if self.locked[i][j]:
                    string += "\033[0m"
                # if len(values) == 1:
                #     string += self.nodes[i,j])
                #     left -= 1
                # elif len(values) == 0:
                #     string += "x"
                # else:
                #     string += " "
            string += "\n"
        return string + " error " + str(self.error())


class Gradient:
    def __init__(self, start):
        self.start = start
    def solve(self):
        from random import randint as randint
        for y in range(10**6):
            state = self.start
            error = 99999
            best = state
            for i in range(0,1000):
                improved = False
                for free in state.free:
                    clone = state.clone()
                    row = free[0]
                    col = free[1]
                    clone.nodes[row][col] = randint(1,9)
                    err = clone.error()
                    if err < error:
                        improved = True
                        error = err
                        best = clone
                state = best
                if error == 0:
                    return state
                # print "\033[11A"
                if improved:
                    print state
                    print ""

if __name__ == "__main__":
    import sys

    board = [[0 for x in range(0,10)] for y in range(0,10)]



    col = 0
    row = 0
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

    state = State(board)

    if sys.argv[1] == 'gradient':
        g = Gradient(state)

        solved = g.solve()

    elif sys.argv[2] == 'genetic':
        g = Genetic(state)

        solved = g.solve()

    print "SOLVED!!!!"
    print solved
