from graphviz import Digraph

class StateMachine:
    def __init__(self, state_set, symbols, transitions, initial, finals):
        self.state_set = state_set
        self.symbols = symbols
        self.transitions = transitions
        self.initial = initial
        self.finals = finals

    def to_grammar(self):
        grammar_rules = {}
        for state in self.state_set:
            grammar_rules[state] = set()
            for symbol in self.symbols:
                if (state, symbol) in self.transitions:
                    destination = self.transitions[(state, symbol)]
                    grammar_rules[state].add(symbol + destination)
            if state in self.finals:
                grammar_rules[state].add('ε')  # ε represents an empty string (epsilon)
        return grammar_rules

    def draw(self):
        graph = Digraph()
        graph.attr(rankdir='LR', size='8,5')

        # Non-final states
        for state in self.state_set - self.finals:
            graph.node(state, shape='circle')
        # Final states
        for state in self.finals:
            graph.node(state, shape='doublecircle')

        # Invisible start node
        graph.node('', shape='none')
        graph.edge('', self.initial)

        # Edges for transitions
        for (source, symbol), destination in self.transitions.items():
            graph.edge(source, destination, label=symbol)

        return graph

# Define the state machine
state_set = {'q0', 'q1', 'q2', 'q3'}
symbols = {'a', 'b'}
transitions = {
    ('q0', 'a'): 'q0',
    ('q0', 'b'): 'q1',
    ('q1', 'a'): 'q1',
    ('q1', 'a'): 'q2',
    ('q1', 'b'): 'q3',
    ('q2', 'a'): 'q2',
    ('q2', 'b'): 'q3'
}
initial = 'q0'
finals = {'q3'}


def check_determinism(machine):
    for state in machine.state_set:
        observed_symbols = set()
        for symbol in machine.symbols:
            if (state, symbol) in machine.transitions:
                if symbol in observed_symbols:
                    return False  # Duplicate transition for a state and symbol
                observed_symbols.add(symbol)
            else:
                return False  # Missing transition for a state and symbol
    return True


def ndfa_to_dfa(ndfa):
    dfa_states = set(['q0'])  # Start with the initial state
    dfa_finals = set()
    dfa_transitions = {}
    pending_states = [{'q0'}]  # States to process

    while pending_states:
        current_state = pending_states.pop()
        for symbol in ndfa.symbols:
            new_state_set = set()
            for state in current_state:
                if (state, symbol) in ndfa.transitions:
                    new_state_set.add(ndfa.transitions[(state, symbol)])
            if new_state_set:
                new_state_id = ''.join(sorted(new_state_set))
                dfa_transitions[(''.join(sorted(current_state)), symbol)] = new_state_id
                if new_state_id not in dfa_states:
                    dfa_states.add(new_state_id)
                    pending_states.append(new_state_set)
                if new_state_set & ndfa.finals:
                    dfa_finals.add(new_state_id)

    return StateMachine(dfa_states, ndfa.symbols, dfa_transitions, 'q0', dfa_finals)


sm = StateMachine(state_set, symbols, transitions, initial, finals)
grammar = sm.to_grammar()
print("Regular Grammar:")
for left_side, production_set in grammar.items():
    for production in production_set:
        print(f"{left_side} -> {production}")

determinism_check = "deterministic" if check_determinism(sm) else "non-deterministic"
print("is", determinism_check)

converted_dfa = ndfa_to_dfa(sm)
# Display the converted DFA
print("Converted DFA:")
for state in converted_dfa.state_set:
    print(f"State: {state}")
    for symbol in converted_dfa.symbols:
        if (state, symbol) in converted_dfa.transitions:
            print(f" δ({state}, {symbol}) = {converted_dfa.transitions[(state, symbol)]}")

sm_graph = sm.draw()

# Render the graph to a file and view it
output_path = 'state_machine_variant_13'
sm_graph.render(output_path, view=True, format='png')