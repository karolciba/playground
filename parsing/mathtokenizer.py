import string

logger = True
indent = 0

def logged(func):
    def logger_decorator(self, *args, **kwargs):
        global indent
        if logger and func.__name__ != "__init__":
            print " "*indent, "Entering", self.__class__, func, args, kwargs
            indent += 1
        ret = func(self, *args, **kwargs)
        if logger and func.__name__ != "__init__":
            indent -= 1
            print " "*indent, "Leaving", self.__class__, func, ret
        return ret
    return logger_decorator

class Token(object):
    @logged
    def __init__(self):
        self.lexeme = []
        self.valid = True
        self.finished = False
    @logged
    def consume(self, char):
        pass
    @logged
    def value(self, char):
        return self.lexeme

class IntegerToken(Token):
    token_valid = string.digits
    token_start = "-"
    @logged
    def __init__(self):
        Token.__init__(self)
        self.started = False
    @logged
    def consume(self, char):
        if not self.started:
            self.started = True
            if char in self.token_start:
                self.lexeme.append(char)
            elif char in self.token_valid:
                self.lexeme.append(char)
            else:
                self.finished = True
                return char
        else:
            if char in self.token_valid:
                self.lexeme.append(char)
            else:
                self.finished = True
                return char
    @logged
    def value(self):
        return int("".join(self.lexeme))


class WhitespaceToken(Token):
    token_valid = string.whitespace

class FloatToken(Token):
    @logged
    def consume(self, char):
        pass

class MinusToken(Token):
    @logged
    def __init__(self):
        Token.__init__(self)
    @logged
    def consume(self, char):
        if not self.finished and char == "-":
            self.lexeme = '-'
            self.finished = True
        else:
            return char

class LeftParenToken(Token):
    @logged
    def __init__(self):
        Token.__init__(self)
    @logged
    def consume(self, char):
        pass

class RightParenToken(Token):
    @logged
    def __init__(self):
        Token.__init__(self)
    @logged
    def consume(self, char):
        pass

class EndToken(Token):
    @logged
    def consume(self, char):
        if char == "\n":
            self.finished = True
            return
        return char

class PlusToken(Token):
    @logged
    def consume(self, char):
        if not self.finished and char == "+":
            self.lexeme = '+'
            self.finished = True
        else:
            return char


class Scanner(object):

    def __init__(self, line):
        self.line = line
        self.pos = 0

    def peek(self):
        if self.pos >= len(self.line):
            return None
        return self.line[self.pos]

    def consume(self):
        self.pos += 1

class Tokenizer(object):

    def __init__(self, line):
        from collections import deque
        self.tokens = (IntegerToken, PlusToken, MinusToken, EndToken)
        self.fringe = deque(token() for token in self.tokens)
        self.scanner = Scanner(line + "\n")
        self.tree = []
        self.node = self.fringe.popleft()

    @logged
    def tokenize(self):
        char = self.scanner.peek()
        if not char:
            return

        if self.node.consume(char) == None:
            self.scanner.consume()
        elif self.node.finished:
            self.tree.append(self.node)
            self.fringe.append(self.node.__class__())
            self.node = self.fringe.popleft()
        else:
            self.fringe.append(self.node.__class__())
            self.node = self.fringe.popleft()
        # import pdb; pdb.set_trace()

        # TODO: tail recursion - replace with loop?
        self.tokenize()



if __name__ == "__main__":
    line = "-23-(58-123)+111"
    tokenizer = Tokenizer(line)
    tokenizer.tokenize()

    tree = tokenizer.tree

    print tree
