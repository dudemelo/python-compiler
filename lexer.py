from io import TextIOWrapper

from mytoken import Token, TokenKind

class Lexer:
    file : TextIOWrapper 

    def __init__(self, file_path) -> None:
        self.file = open(file_path, "r")

    def get_next_token(self) -> Token:
        token = Token(TokenKind.UNKOWN)

        for c in self.file.read():
            # nao encontrou nenhum token e o char atual nao
            # e um espaco
            if token.iskind(TokenKind.UNKOWN) and not c.isspace():
                token = Token(TokenKind(c))

            if token.iskind(TokenKind.OPEN_TAG):
                if c.isspace() or c == "\n":
                    token = Token(TokenKind.UNKOWN)
                    break
                token.value += c

        return token

