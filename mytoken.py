from enum import Enum
from dataclasses import dataclass

# magia magica do duno
class TokenKind(str, Enum):
    UNKOWN = ''
    OPEN_TAG = '<'
    COMMENT = '#'
    IDENTIFIER = ''

@dataclass
class Token:
    kind: TokenKind
    value: str = ""

    def iskind(self, kind) -> bool:
        return self.kind == kind

