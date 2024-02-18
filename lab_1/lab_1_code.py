# Variant 13

import random

class Grammar:
    def __init__(self, VN, VT, S, productions):
        self.VN = VN  # Set of non-terminal symbols
        self.VT = VT  # Set of terminal symbols
        self.S = S    # Start symbol
        self.P = productions  # Set of production rules


    def generate_valid_string(self, symbol, max_depth=5):
        if max_depth == 0:
            return ''

        if symbol not in self.P:
            return symbol

        production_rule_key = random.choice(self.P[symbol])

        result = ''
        for char in production_rule_key:
            result += self.generate_valid_string(char, max_depth - 1)
        return result

    def generate_5_valid_strings(self):
        final_strings = []
        for _ in range(5):
            final_strings.append(self.generate_valid_string('S'))
        return final_strings



    def toFiniteAutomaton(self):
        Q = self.VN.union({'X'})  # States of the FA are the non-terminals of the grammar plus an additional state X
        Sigma = self.VT  # Alphabet of the FA is the set of terminals of the grammar
        Delta = {}  # Transition function
        q0 = {self.S}  # Initial state is the start symbol of the grammar
        F = {'X'}  # Set of final states

        # Initialize Delta with empty sets for all state-symbol pairs
        for state in Q:
            for symbol in Sigma:
                Delta[(state, symbol)] = set()

        # Construct transition function Delta
        for non_terminal, productions in self.P.items():
            for production in productions:
                if len(production) == 1 and production[0] in self.VT:  # Non-terminal to terminal transition
                    Delta[(non_terminal, production[0])].add('X')
                elif len(production) == 2 and production[0] in self.VT:  # Non-terminal to non-terminal transition
                    Delta[(non_terminal, production[0])].add(production[1])
                elif len(production) == 1 and production[0] in self.VN:  # Non-terminal to terminal transition
                    Delta[(non_terminal, '')].add(production[0])
                    F.add(production[0])  # Production is a final state

        return FiniteAutomaton(Q, Sigma, Delta, q0, F)

class FiniteAutomaton:
    def __init__(self, Q, Sigma, Delta, q0, F):
        self.Q = Q
        self.Sigma = Sigma
        self.Delta = Delta
        self.q0 = q0
        self.F = F

    def follow_rules(self, w):
        currentStates = self.q0
        for letter in w:
            nextStates = set()
            for state in currentStates:
                if (state, letter) in self.Delta:
                    nextStates.update(self.Delta[(state, letter)])
            currentStates = nextStates
        return any(state in self.F for state in currentStates)

productions = {
    'S': ['aB'],
    'B': ['aD', 'bB', 'cS'],
    'D': ['aD', 'bS', 'c']
}
VN = {'S', 'B', 'D'}
VT = {'a', 'b', 'c'}
S = 'S'


grammar = Grammar(VN, VT, S, productions)

valid_strings = grammar.generate_5_valid_strings()
print("Generated strings:")
for _ in valid_strings:
    print(_)

finiteAutomaton = grammar.toFiniteAutomaton()
listOfStrings = ["bbb", "abac", "acafffffffffffffffffffffffaaabb", "aaac", "ffffffffffffffffffffffffffffff"]
for word in listOfStrings:
    print({True: f'{word} _____can be obtained', False: f'{word} _____ can not be obtained'} [finiteAutomaton.follow_rules(word)])
