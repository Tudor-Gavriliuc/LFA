import re

# Token types
IDENTIFIER = 'IDENTIFIER'
INTEGER = 'INTEGER'
CHAR = 'CHAR'
STRING = 'STRING'
PLUS = 'PLUS'
MINUS = 'MINUS'
MULTIPLY = 'MULTIPLY'
DIVIDE = 'DIVIDE'
ASSIGN = 'ASSIGN'
LPAREN = 'LPAREN'
RPAREN = 'RPAREN'
EQUAL = 'EQUAL'
LESS = 'LESS'
GREATER = 'GREATER'
LESS_EQUAL = 'LESS_EQUAL'
GREATER_EQUAL = 'GREATER_EQUAL'
FOR = 'FOR'
IN = 'IN'
RANGE = 'RANGE'
IF = 'IF'
ELSE = 'ELSE'
PRINT = 'PRINT'
COLON = 'COLON'
INCREMENT = 'INCREMENT'
SPACE = 'SPACE'
NEWLINE = 'NEWLINE'
EOF = 'EOF'
DOT = 'DOT'
COMMA = 'COMMA'

# Regular expressions for token patterns
TOKEN_REGEX = [
    (r'[a-zA-Z][a-zA-Z0-9_]*', IDENTIFIER),  # Identifier regex
    (r'\d+', INTEGER),  # Integer regex
    (r'\'[a-zA-Z\s][a-zA-Z\s]+\'', STRING),  # String regex
    (r'\'[a-zA-Z]\'', CHAR),  # Char regex
    (r'\+=', INCREMENT),  # Increment regex
    (r'\+', PLUS),  # Plus regex
    (r'-', MINUS),  # Minus regex
    (r'\*', MULTIPLY),  # Multiply regex
    (r'/', DIVIDE),  # Divide regex
    (r'\(', LPAREN),  # Left parenthesis regex
    (r'\)', RPAREN),  # Right parenthesis regex
    (r'==', EQUAL),  # Equal regex
    (r'<=', LESS_EQUAL),  # Less than or equal regex
    (r'>=', GREATER_EQUAL),  # Greater than or equal regex
    (r'<', LESS),  # Less than regex
    (r'>', GREATER),  # Greater than regex
    (r'=', ASSIGN),  # Assign regex
    (r':', COLON),  # Colon regex
    (r'\s+', SPACE),  # Space regex
    (r'\n', NEWLINE), # Newline regex
    (r'\.', DOT),       # Dot regex
    (r',', COMMA)      # Comma regex
]

KEY_WORDS = ['for', 'in', 'range', 'if', 'else', 'print', 'while']


class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return f'Token({self.type}, {self.value})'


class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0

    def error(self):
        raise Exception('Invalid character')

    def get_next_token(self):
        while self.pos < len(self.text):
            for pattern, token_type in TOKEN_REGEX:
                regex = re.compile(pattern)
                match = regex.match(self.text, self.pos)
                if match:
                    value = match.group(0)
                    self.pos = match.end()
                    if token_type == SPACE or token_type == NEWLINE:
                        break  # Skip spaces
                    elif value in KEY_WORDS:
                        return Token(value.upper(), value)
                    else:
                        return Token(token_type, value)
            else:
                self.error()

        return Token(EOF, None)


if __name__ == '__main__':
    lexer = Lexer("for i in range(10): print(Number,i)")

    while True:
        token = lexer.get_next_token()
        if token.type == EOF:
            break
        print(token)
