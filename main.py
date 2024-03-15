from lexer import Lexer
from mytoken import TokenKind

lexer = Lexer("examples/program.php")

while True:
    t = lexer.get_next_token()
    if t.iskind(TokenKind.UNKOWN):
        break
    print(t)


