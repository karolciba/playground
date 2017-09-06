"""Regular expression compilater allowing smallest functional subset
of expressions, i.e.:
  [-]+(0|[1-9][0-9]*)
"""

import automata

from enum import Enum

def crange(fro, to):
    """Character range (in ASCII) starting "fro" ending in "to"
    """
    return [chr(c) for c in xrange(ord(fro),ord(to)+1)]

# EXPR   ::= CONCAT | UNION | GROUP
# CONCAT ::= char CONCAT | char
# UNION  ::= EXPR "|" EXPR
# GROUP  ::= [EXPR]
# RANGE  ::= char-char
# CLOUS  :: = EXPR *
# char   ::= a..z A..Z 0..9

class Expr(object):
    def __init__(self):
        self._children = []

class BaseExpr(object):
    def __init__(self):
        self.chars = []
    def append(self,char):
        self.chars.append(char)

class Concat(object):
    def __init__(self):
        self._list = []
    def concatenate(self, char):
        self._list.append(char)

class Group(object):
    def __init__(self):
        self._list = []
    def concatenate(self, char):
        self._list.append(char)

class Closure(object):
    def __init__(self,expr):
        self._expr = expr

class Range(object):
    def __init__(self):
        self._from = None
        self._to = None

class Union(object):
    def __init__(self, left):
        self._left = left
    def right(self, right):
        self._right = right

stack = []
stack.append(Group())
def parse(re):
    i = 0
    while i < len(re):
        if re[i] == '|':
            top = stack[-1]
            union = Union(top)
            stack.push(union)
        elif re[i] == '(':
            stack.append(Expr())
        elif re[i] == ')':
            while True:
                top = stack.pop()
                if isinstance(stack[-1], Union):
                    Union.right(top)

        # character no in special set, default
        else:
            if isinstance(stack[-1],BaseExpr):
            else:
                stack.push(BaseExpr())
                stack[-1].append(re[i])

        if False:
            if re[i] == '(':
                stack.append(Expr())
            elif re[i] == '|':
                top = stack.pop()
                stack.append(Union(top))
            elif re[i] == ')':
                if isinstance(stack[-2],Union):
                    top = stack.pop()
                    union = stack.pop()
                    union.right(top)
                    stack.append(union)
            elif re[i] == '*':
                top = stack.pop()
                stack.append(Closure(top))
            else:
                if isinstance(stack[-1],Group):
                    stack[-1].concatenate(re[i])
                else:
                    top = stack.pop()
                    concat = Concat()
                    concat.concatenate(top)
                    concat.concatenate(re[i])
                    stack.append(concat)

        i += 1

    if len(stack) == 2:
        if isinstance(stack[-2],Union):
            top = stack.pop()
            union = stack.pop()
            union.right(top)
            stack.append(union)
        else:
            raise Exception("Syntax Error")

    return stack.pop()


if __name__ == "__main__":
    re = 'abc'
