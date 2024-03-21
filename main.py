from dataclasses import dataclass, field

@dataclass
class Token:
    kind: str
    body: str

class Lexer:
    def __init__(self, code: str):
        self.code = code
        self.pos = 0
    def peek(self) -> Token:
        pos = self.pos
        token = self.next_token()
        self.pos = pos
        return token
    def next_token(self) -> Token:
        token = None
        while self.pos < len(self.code) and token ==  None:
            if self.code[self.pos] in '()':
                token = Token('parenthesis', self.code[self.pos])
            elif self.code[self.pos].isdigit():
                start = self.pos
                while self.pos < len(self.code) and self.code[self.pos].isdigit():
                    self.pos += 1
                token  =Token('number', self.code[start:self.pos]) 
            elif self.code[self.pos].isalpha():
                start = self.pos
                while self.pos < len(self.code) and self.code[self.pos].isalpha():
                    self.pos += 1
                token = Token('identifier', self.code[start:self.pos]) 
            self.pos += 1
        return token if token else Token('eof', '')

@dataclass
class Node:
    @property
    def kind(self) -> str:
        return self.__class__.__name__

@dataclass
class Program(Node):
    body: list[Node] = field(default_factory=lambda: [])
    def append(self, node: Node):
        self.body.append(node)

@dataclass
class FunctionCall(Node):
    name: str
    arguments: list[Node] = field(default_factory=lambda: [])
    def append_arguments(self, node: Node):
        self.arguments.append(node)

@dataclass
class NumberLiteral(Node):
    value: int

@dataclass
class Parser:
    lexer: Lexer
    def _parse_number(self, token: Token) -> Node:
        return NumberLiteral(int(token.body))
    def _parse_function_call(self, token: Token) -> Node:
        fn = FunctionCall(token.body)
        fn.append_arguments(self._parse_number(self.expect('number')))
        if self.lexer.peek().kind == 'parenthesis':
            self.expect('parenthesis')
            fn.append_arguments(self._parse_function_call(self.expect('identifier'))) 
            self.expect('parenthesis')
        else:
            fn.append_arguments(self._parse_number(self.expect('number')))
        return fn
    def expect(self, kind: str) -> Token:
        token = self.lexer.next_token()
        if token == None or token.kind != kind:
            raise SyntaxError(f'Expected {kind} but got {token.kind}')
        return token
    def parse(self) -> Node:
        program = Program()
        self.expect('parenthesis')
        program.append(self._parse_function_call(self.expect('identifier')))
        return program

class Visitor:
    def visit(self, node: Node, parent: Node):
        print(node.kind)
        # method = getattr(self, f'visit_{node.kind}', self.generic_visit)
        # return method(node)
    def generic_visit(self, node: Node):
        raise RuntimeError(f'No visit_{node.kind} method')

lexer = Lexer('(add 2 (subtract 4 2))')
parser = Parser(lexer)
print(parser.parse())

