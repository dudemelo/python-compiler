from dataclasses import dataclass
from io import TextIOWrapper

from mytoken import Token, TokenKind

@dataclass
class Location:
    file: str
    row: int
    col: int

class Lexer:
    file : TextIOWrapper
    location: Location

    def __init__(self, file_path) -> None:
        self.file = open(file_path, "r")
        self.location = Location(file_path, 0, 0)

    def get_next_token(self) -> Token:
        token = Token(TokenKind.UNKOWN)

        while (c := self.file.read(1)):

            if c == "\n":
                self.location.row += 1
                self.location.col = 0

            if token.iskind(TokenKind.UNKOWN) and not c.isspace():
                if hasattr(TokenKind, c):
                    token = Token(TokenKind(c))
                else:
                    token = Token(TokenKind('IDENTIFIER'))

            if token.iskind(TokenKind.OPEN_TAG):
                if c.isspace() or c == "\n":
                    break
                token.value += c
                print('achou o opentag perdido', token)

            if token.iskind(TokenKind.COMMENT):
                if c == "\n":
                    break
                token.value += c
                print('achou o comentario perdido', token)

        return token

    def raiseException(self):
        print(f'./{self.location.file}:{self.location.row}:{self.location.col}')

