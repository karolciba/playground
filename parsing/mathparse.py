"""Simple math parser

expr -> TermRest
rest -> +TermRest | -TermRest | e
term -> 0-9
"""

class MathParser(object):
    def __init__(self, string, logger = False):
        self._string = string + '$'
        self._tree = []
        self._lookahead = None
        self._pos = 0
        self._end = '$'
        self._logger = logger

    def _logging(func):
        def logging(self, *args, **kwargs):
            if self._logger:
                print "Entering", func, args, kwargs
            ret = func(self, *args, **kwargs)
            if self._logger:
                print "Leaving", func, ret
            return ret
        return logging

    def parse(self):
        """ Parses string given during initialization """
        # import pdb; pdb.set_trace()
        self._lookahead = self._string[0]
        self._expr()
        return self._tree

    @_logging
    def _getchar(self):
        self._pos += 1
        return self._string[self._pos]

    @_logging
    def _match(self, token):
        if self._lookahead == token:
            self._lookahead = self._getchar()
        """ Consumes element from string """

    @_logging
    def _push(self, token):
        self._tree.append(token)
        """ Pushes element onto tree """

    @_logging
    def _expr(self):
        """ expr -> term rest """
        self._term()
        self._rest()

    @_logging
    def _rest(self):
        """ rest -> + term rest | - term rest | e """
        if self._lookahead == '+':
            self._match('+')
            self._term()
            self._push('+')
            self._rest()
        elif self._lookahead == '-':
            self._match('-')
            self._term()
            self._push('-')
            self._rest()
        else:
            pass

    @_logging
    def _term(self):
        """ term -> [0-9] """
        if self._lookahead.isdigit():
            self._push(int(self._lookahead))
            self._match(self._lookahead)
        else:
            self._error()

    def _error(self):
        """ Error in parsing """
        raise Exception('Parsing error')

class MathEvaluate(object):
    @staticmethod
    def eval(expr):
        stack = []
        for e in expr:
            if e == '+':
                ret = stack.pop() + stack.pop()
                stack.append(ret)
            elif e == '-':
                ret = stack.pop() - stack.pop()
                stack.append(ret)
            else:
                stack.append(e)
        return stack



if __name__ == '__main__':

    string = '2+3-5+8'

    # import pudb; pu.db

    parser = MathParser(string)
    tree = parser.parse()

    print parser._tree
