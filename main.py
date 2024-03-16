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
while t := l.next_token():
    print('TOKEN --->', t.value)
