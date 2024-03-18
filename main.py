import pprint

class BlockExpression:
    def __init__(self, children) -> None:
        self.children = children

    def push(self, child):
        self.children.append(child)

class ProgramExpression(BlockExpression):
    def __init__(self) -> None:
        super().__init__([])

class FunctionExpression(BlockExpression):
    def __init__(self, name, arguments, children) -> None:
        super().__init__(children)
        self.name = name
        self.arguments = arguments

class OperationExpression:
    def __init__(self, left, right, operator) -> None:
        self.left = left
        self.right = right
        self.operator = operator

class Parser():
    def __init__(self, lexer) -> None:
        self.lexer = lexer
        self.root = ProgramExpression()

    def expect(self, token, kind):
        if not token.iskind(kind):
            raise Exception(f'{token.location.file}{token.value} expected {kind}')

    def parse_operation(self) -> OperationExpression:
        left = self.lexer.next_token()
        self.expect(left, TokenKind.IDENTIFIER)
        operator = self.lexer.next_token()
        self.expect(operator, TokenKind.OPERATOR)
        right = self.lexer.next_token()
        self.expect(right, TokenKind.IDENTIFIER)
        return OperationExpression(left, right, operator)

    def parse(self):
        self.expect(self.lexer.next_token(), TokenKind.OPEN_TAG)
        while token := self.lexer.next_token():
            if token.iskind(TokenKind.IDENTIFIER) and token.value == 'function':
                name = self.lexer.next_token()
                arguments = []
                return_expression = None
                self.expect(name, TokenKind.IDENTIFIER)
                self.expect(self.lexer.next_token(), TokenKind.OPEN_PARENTHESIS)
                while arg := self.lexer.next_token():
                    if arg.iskind(TokenKind.CLOSE_PARENTHESIS):
                        break
                    arguments.append(arg)
                self.expect(self.lexer.next_token(), TokenKind.OPEN_CURLY)
                while token := self.lexer.next_token():
                    if token.iskind(TokenKind.CLOSE_CURLY):
                        break
                    elif token.iskind(TokenKind.IDENTIFIER) and token.value == 'return':
                        return_expression = self.parse_operation()
                        break
                self.root.push(FunctionExpression(name, arguments, return_expression))
            else:
                if token.iskind(TokenKind.IDENTIFIER) and token.value == '$':
                    self.root.push(self.parse_operation())

        for i in self.root.children:
            pprint.pprint(i.__dict__)

class Location:
    def __init__(self, file:str) -> None:
        self.file:str = file
        self.row:int = 0
        self.col:int = 0

class TokenKind:
    IDENTIFIER: int = 1
    OPEN_TAG: int = 2
    COMMENT: int = 3
    OPEN_PARENTHESIS: int = 4
    CLOSE_PARENTHESIS: int = 5
    OPEN_CURLY: int = 6
    CLOSE_CURLY: int = 7
    COMMA: int = 8
    OPERATOR: int = 9

    def __init__(self, kind: int) -> None:
        self.kind: int = kind

    @staticmethod
    def fromChar(char: str):
        return TokenKind(TokenKind.kinds()[char])

    @staticmethod
    def kinds():
        return {
            '<': TokenKind.OPEN_TAG,
            '#': TokenKind.COMMENT,
            '(': TokenKind.OPEN_PARENTHESIS,
            ')': TokenKind.CLOSE_PARENTHESIS,
            '{': TokenKind.OPEN_CURLY,
            '}': TokenKind.CLOSE_CURLY,
            ',': TokenKind.COMMA,
            '+': TokenKind.OPERATOR,
            '=': TokenKind.OPERATOR,
        }

    @staticmethod
    def exists(char: str) -> bool:
        return True if char in TokenKind.kinds() else False

    def issinglechar(self) -> bool:
        return True if self.kind in [
            TokenKind.OPEN_PARENTHESIS,
            TokenKind.CLOSE_PARENTHESIS,
            TokenKind.OPEN_CURLY,
            TokenKind.CLOSE_CURLY,
            TokenKind.COMMA,
            TokenKind.OPERATOR,
        ] else False

class Token:
    def __init__(self, char: str) -> None:
        self.kind: TokenKind = TokenKind.fromChar(char) if TokenKind.exists(char) else TokenKind(TokenKind.IDENTIFIER)
        self.value: str = char
    def iskind(self, *kinds):
        return True if self.kind.kind in kinds else False
    def issinglechar(self) -> bool:
        return self.kind.issinglechar()

class Lexer:
    def __init__(self,file) -> None:
        self.location = Location(file)
        self.file = open(file, 'r')

    def move_col(self):
        self.location.col += 1

    def move_row(self):
        self.location.row += 1
        self.location.col = 0

    def next_token(self):
        token = None
        while char := self.file.read(1):
            if token == None:
                if char.isspace() or char in ["\n", "\t"]:
                    continue
                token = Token(char)
                if token.issinglechar():
                    break
            else:
                self.move_row() if char == "\n" else self.move_col()
                if token.iskind(TokenKind.COMMENT, TokenKind.OPEN_TAG) and char == "\n":
                    break;
                if token.iskind(TokenKind.IDENTIFIER) and not char.isalpha():
                    self.file.seek(self.file.tell() - 1)
                    break;
                token.value += char
        return token

l = Lexer('./examples/program.php')
p = Parser(l)
p.parse()
