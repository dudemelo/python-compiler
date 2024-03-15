from enum import Enum

# magia magica do duno
class TokenKind(str, Enum):
    UNKOWN = ''
    OPEN_TAG = '<'
    COMMENT = '#'

class Token:
    def __init__(self, kind : TokenKind):
        self.kind = kind
        self.value : str = ""

    def iskind(self, kind) -> bool:
        return self.kind == kind

