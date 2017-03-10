"""Simple math parser

expr -> TermRest
rest -> +TermRest | -TermRest | e
term -> 0-9
"""

logger = True
indent = 0
def _logging(func):
    def logging(self, *args, **kwargs):
        global indent
        if logger and func.__name__ != "__init__":
            print " "*indent, "Entering", self.__class__, func, args, kwargs
            indent += 1
        ret = func(self, *args, **kwargs)
        if logger and func.__name__ != "__init__":
            indent -= 1
            print " "*indent, "Leaving", self.__class__, func, ret
        return ret
    return logging

class SyntaxToken(object):
    @_logging
    def consume(self, *args):
        return False
    @_logging
    def syntax(self):
        return ()

    def parse(self, string]):
        # create object
        node = syntax[0]()
        # try to consume input
        for idx, char in enumerate(string):
            print "Consuming input", idx, char
            if not node.consume(char):
                break

        substring = string[idx:]
        # get possible grammars
        grammars = node.syntax()
        print "Checking grammars", grammars, "substr", substring
        # descent into each grammar
        for grammar in grammars:
            leaf = self.parse(substring, grammar)
            if leaf:
                node._children = leaf
                break

        return node

class NumberToken(SyntaxToken):
    @_logging
    def __init__(self):
        self._lexeme = []
        self._started = False
        self._begin = '+-'

    @_logging
    def consume(self, char):
        if not self._started:
            self._started = True
            if char in self._begin:
                self._lexeme.append(char)
            elif char.isdigit():
                self._lexeme.append(char)
            else:
                return False
        elif char.isdigit():
            self._lexeme.append(char)
        else:
            return False

        return True

    @_logging
    def value(self):
        return int("".join(self._lexeme))

class WhiteSpaceToken(SyntaxToken):
    @_logging
    def __init__(self):
        import string
        self._lexeme = []
        self._started = False
        self._valid = string.whitespace

    @_logging
    def consume(self, char):
        if char in self._valid:
            self._lexeme.append(char)
        else:
            return False

    @_logging
    def value(self):
        return "".join(self._lexeme)

    @_logging
    def syntax(self):
        return ()

class PlusToken(SyntaxToken):
    @_logging
    def __init__(self):
        self._lexeme = '+'
        self._children = []

    @_logging
    def consume(self, char):
        if char == '+':
            return True
        else:
            return False

    @_logging
    def value(self):
        return self._children[0].value() + self._children[1].value()

class MinusToken(SyntaxToken):
    @_logging
    def __init__(self):
        self._lexeme = '-'
        self._children = []

    @_logging
    def consume(self, char):
        if char == '-':
            pass
        else:
            return False

    @_logging
    def value(self):
        return self._children[0].value() - self._children[1].value()

class ErrorSyntax(SyntaxToken):
    @_logging
    def __init__(self):
        pass

    @_logging
    def consume(self, char):
        raise Exception("Syntax error!")

class EndToken(SyntaxToken):
    @_logging
    def __init__(self):
        pass

    @_logging
    def consume(self, char):
        if char == '$':
            return True

        return False

class TermSyntax(SyntaxToken):
    @_logging
    def __init__(self):
        self._syntax = (NumberToken,
                        ErrorSyntax)
        self._children = []

class RestSyntax(SyntaxToken):
    @_logging
    def __init__(self):
        self._syntax = (PlusToken,
                        MinuxToken,
                        EndToken,
                        ErrorSyntax)
        self._children = []

class ExprSyntax(SyntaxToken):
    @_logging
    def __init__(self):
        self._syntax = (TermSyntax,
                        ErrorSyntax)
        self._children = []

    def consume(self, char):
        return True

    @_logging
    def syntax(self):
        return self._syntax

    def parse(self, string):
        for idx, char in enumerate(string):
            ret = self.consume(char)
            if ret == False:
                break

        substring = string[idx:]

        grammar = None
        for option in self.syntax():
            grammar = option()
            grammar.parse(substring)

        return grammar


class TempSyntax(SyntaxToken):
    @_logging
    def __init__(self):
        self._syntax = ((NumberToken, WhiteSpaceToken, NumberToken),
                        (WhiteSpaceToken, NumberToken),
                        (ErrorSyntax))
        self._children = []

    def consume(self, char):
        return False

    def syntax(self):
        return self._syntax


class Parser(object):
    def __init__(self, logger = True):
        self._logger = logger
        pass

    @_logging
    def parse(self, string, syntax = [TempSyntax]):
        # create object
        node = syntax[0]()
        # try to consume input
        for idx, char in enumerate(string):
            print "Consuming input", idx, char
            if not node.consume(char):
                break

        substring = string[idx:]
        # get possible grammars
        grammars = node.syntax()
        print "Checking grammars", grammars, "substr", substring
        # descent into each grammar
        for grammar in grammars:
            leaf = self.parse(substring, grammar)
            if leaf:
                node._children = leaf
                break

        return node

if __name__ == '__main__':

    string = '2+3-5+8-11+256+123-67'

    # import pudb; pu.db

    parser = Parser()
    tree = parser.parse(string)

    print "Tree"
    print tree
