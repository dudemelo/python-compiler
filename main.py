from lexer import Lexer
from mytoken import Token, TokenKind

lexer = Lexer("examples/program.php")

while True:
    t = lexer.get_next_token()
    if t.iskind(TokenKind.UNKOWN):
        break
    print(t.value)


