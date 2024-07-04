import json

class Production():
    def __init__(self, symbol, derivations):
        self.symbol = symbol
        self.derivations = derivations

class Grammar():
    def __init__(self, grammar_path):
        self.non_terminal_symbols = []
        self.terminal_symbols = []
        self.inittial_symbol = None
        self.productions = []
        self.load_grammar(grammar_path)

    def load_grammar(self, grammar_path):
        with open(grammar_path, 'r') as file:
            grammar_data = json.load(file)
            self.no_terminal_symbols = grammar_data['non_terminal_symbols']
            self.terminal_symbols = grammar_data['terminal_symbols']
            self.initial_symbol = grammar_data['initial_symbol']
            for prod in grammar_data['productions']:
                production = Production(prod['symbol'], prod['derivations'])
                self.productions.append(production)