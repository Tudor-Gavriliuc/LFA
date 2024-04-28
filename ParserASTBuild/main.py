import re
from enum import Enum, auto

from anytree import Node, RenderTree


class TokenType(Enum):
    OPEN_PARENTHESIS = auto()
    CLOSE_PARENTHESIS = auto()
    MATH_OPERATION = auto()
    NUMBERS = auto()
    START = auto()

# Define the allowed transitions between token types
transitions = {
    TokenType.OPEN_PARENTHESIS: [TokenType.NUMBERS, TokenType.OPEN_PARENTHESIS],
    TokenType.MATH_OPERATION: [TokenType.NUMBERS, TokenType.OPEN_PARENTHESIS],
    TokenType.CLOSE_PARENTHESIS: [TokenType.MATH_OPERATION, TokenType.CLOSE_PARENTHESIS],
    TokenType.NUMBERS: [TokenType.NUMBERS, TokenType.CLOSE_PARENTHESIS, TokenType.MATH_OPERATION],
    TokenType.START: [TokenType.OPEN_PARENTHESIS, TokenType.NUMBERS]
}

# Define regular expressions for token categorization
data = {
    TokenType.OPEN_PARENTHESIS: [r"\(", r"\["],
    TokenType.CLOSE_PARENTHESIS: [r"\)", r"\]"],
    TokenType.MATH_OPERATION: [r"[+\-*/%^]"],
    TokenType.NUMBERS: [r"\d+"]
}

class Lexer:
    def __init__(self, equation):
        self.equation = equation

    def lexer(self):
        self.equation = self.equation.replace(" ", "")
        seq_parenthesis = []  # Stack to keep track of open parentheses
        category_mapping = [TokenType.START]  # Start with START category
        failed_on = ""
        valid_tokens = []

        for symbol in self.equation:
            # Parenthesis handling
            if symbol in data[TokenType.OPEN_PARENTHESIS]:
                seq_parenthesis.append(symbol)
            elif symbol in data[TokenType.CLOSE_PARENTHESIS]:
                if not seq_parenthesis:
                    print(f"ERROR: Extra closing parenthesis found.")
                    print(f"Failed on symbol {failed_on}")
                    return False
                else:
                    last_open = seq_parenthesis.pop()
                    if (symbol == ')' and last_open != '(') or (symbol == ']' and last_open != '['):
                        print(f"ERROR: Mismatched closing parenthesis found.")
                        print(f"Failed on symbol {failed_on}")
                        return False

            # Token categorization using regular expressions
            found_category = False
            for category, patterns in data.items():
                for pattern in patterns:
                    if re.match(pattern, symbol):
                        current_category = category
                        found_category = True
                        break
                if found_category:
                    break
            if not found_category:
                print(f"ERROR: Symbol '{symbol}' does not belong to any known category.")
                print(f"Failed on symbol {failed_on}")
                return False

            # Transition checking
            if current_category not in transitions[category_mapping[-1]]:
                print(f"ERROR: Transition not allowed from '{category_mapping[-1]}' to '{current_category}'.")
                print(f"Failed on symbol {failed_on}")
                return False

            # Update mappings and tokens
            category_mapping.append(current_category)
            valid_tokens.append(symbol)
            failed_on += symbol

        # Check for remaining open parentheses
        if seq_parenthesis:
            print(f"ERROR: Not all parentheses were closed.")
            print(f"Failed on symbol {failed_on}")
            return False
        return category_mapping, valid_tokens

class Parser:
    def __init__(self, category_mapping, valid_tokens):
        self.category_mapping = category_mapping
        self.valid_tokens = valid_tokens

    # Construct the abstract syntax tree (AST) and print it
    def parse(self):
        root = Node(self.category_mapping[0].name)
        parent = root
        for token, category in zip(self.valid_tokens, self.category_mapping[1:]):
            node = Node(token, parent=parent)
            parent = Node(category.name, parent=parent)

        for pre, _, node in RenderTree(root):
            print("%s%s" % (pre, node.name))

# Test equation
test_equation = "8+(7+4)*5"

lexer = Lexer(test_equation)
category_mapping, valid_tokens = lexer.lexer()
print(category_mapping)
print(valid_tokens)
Parser(category_mapping, valid_tokens).parse()
