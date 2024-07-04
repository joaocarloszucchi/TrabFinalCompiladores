import json

class Production():
    def __init__(self, symbol, derivation):
        self.symbol = symbol
        self.derivation = derivation

    def print(self):
        """
        Prints the production rules

        (Symbol -> Derivation)
        """
        print(self.symbol, " -> ", self.derivation)

    def is_prod_valid_gld(self, non_terminal_symbols, terminal_symbols):
        """
        Returns true if the production can belong to a GLD

        Rule 0: Allow empty derivation

        Rule 1: At least 1 terminal symbol

        Rule 2: Maximum of 1 non terminal symbol

        Rule 3: Terminal symbol always comes after the non terminal symbol
        """
        if self.gld_rule0():
            return True
        return self.gld_rule1(terminal_symbols) and self.gld_rule2(non_terminal_symbols) and self.gld_rule3(non_terminal_symbols, terminal_symbols)
    
    def gld_rule0(self):
        """
        Allow empty derivation
        """
        return self.derivation == 'e'

    def gld_rule1(self, terminal_symbols):
        """
        At least 1 non terminal symbol
        """
        count = 0
        for char in self.derivation:
            if char in terminal_symbols:
                count += 1
        return count > 0

    def gld_rule2(self, non_terminal_symbols):
        """
        Maximum of 1 non terminal symbol
        """
        count = 0
        for char in self.derivation:
            if char in non_terminal_symbols:
                count += 1
        return count < 2
    
    def gld_rule3(self, non_terminal_symbols, terminal_symbols):
        """
        Terminal symbol always comes after the non terminal symbol
        """
        count_non_terminal = 0
        for char in self.derivation:
            if char in non_terminal_symbols:
                count_non_terminal += 1
            elif char in terminal_symbols:
                if(count_non_terminal > 0):
                    return False     
        return True

class Grammar():
    def __init__(self, grammar_path):
        self.non_terminal_symbols = []
        self.terminal_symbols = []
        self.inittial_symbol = None
        self.productions = []
        self.load_grammar(grammar_path)

    def load_grammar(self, grammar_path):
        """
        Extracts the grammar info from the json file
        """
        with open(grammar_path, 'r') as file:
            grammar_data = json.load(file)
            self.non_terminal_symbols = grammar_data['non_terminal_symbols']
            self.terminal_symbols = grammar_data['terminal_symbols']
            self.initial_symbol = grammar_data['initial_symbol']
            for prod in grammar_data['productions']:
                symbol = prod['symbol']
                derivations = prod['derivations']
                for derivation in derivations:
                    production = Production(symbol, derivation)
                    self.productions.append(production)
    
    def print(self):
        """
        Prints the grammar variables:

        (Non Terminal Symbols)

        (Terminal Symbols)

        (Inittial Symbol)

        (Productions)
        """
        print("Non Terminal Symbols: ", self.non_terminal_symbols)
        print("Terminal Symbols: ", self.terminal_symbols)
        print("Inittial Symbol: ", self.initial_symbol)
        print("Productions: ")
        for prod in self.productions:
            prod.print()

    def validate_grammar(self):
        """
        Returns true if the grammar have no inconsistency

        Rule 1: All non terminal symbol have at least 1 production

        Rule 2: All terminal symbol appear in at least 1 production
        """
        for prod in self.productions:
            if not prod.is_prod_valid_gld(self.non_terminal_symbols, self.terminal_symbols):
                return False

    def validate_grammar_gld(self):
        """
        Returns true if the grammar is GLD
        """
        for prod in self.productions:
            if not prod.is_prod_valid_gld(self.non_terminal_symbols, self.terminal_symbols):
                return False
