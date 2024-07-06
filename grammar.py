import json
import sys

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
        At least 1 terminal symbol
        """
        count = 0
        for char in self.derivation:
            if char in terminal_symbols:
                count += 1
        if count == 0:
            print("Error in GLD Validation, rule1. The derivation ", self.get_print_string(), " don't have a terminal symbol")
            return False
        return True

    def gld_rule2(self, non_terminal_symbols):
        """
        Maximum of 1 non terminal symbol
        """
        count = 0
        for char in self.derivation:
            if char in non_terminal_symbols:
                count += 1
        if count >= 2:
            print("Error in GLD Validation, rule2. The derivation ", self.get_print_string(), " have more than 1 non terminal symbols")
            return False
        return True
    
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
                    print("Error in GLD Validation, rule3. The derivation ", self.get_print_string(), " has a non terminal symbol before a terminal symbol")
                    return False     
        return True

    def get_symbol(self):
        return self.symbol
    
    def get_derivation(self):
        return self.derivation

    def get_print_string(self):
        return str(self.symbol) + " -> " + str(self.derivation)

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

        Rule 3: The production symbol is always a terminal symbol previously defined

        Rule 4: All derivation symbols are included in the grammar
        """
        if not (self.rule1() and self.rule2() and self.rule3() and self.rule4()):
            sys.exit("The grammar have inconsistencies")
        print("The grammar have no inconsistency!")

        if not self.validate_grammar_gld():
            sys.exit("The grammar is not GLD")
        
        print("The grammar is OK!")
        return
        
    def rule1(self):
        """
        All non terminal symbol have at least 1 production
        """
        for non_term in self.non_terminal_symbols:
            count = 0
            for prod in self.productions:
                if non_term == prod.get_symbol():
                    count += 1
            if count == 0:
                print("Error in Grammar Validation, rule1. The non terminal symbol: ", non_term, " have 0 productions")
                return False
        return True

    def rule2(self):
        """
        All terminal symbol appear in at least 1 production
        """
        for term in self.terminal_symbols:
            count = 0
            for prod in self.productions:
                if term in prod.get_derivation():
                    count += 1
            if count == 0:
                print("Error in Grammar Validation, rule2. The terminal symbol: ", term, " is not being used in any derivation")
                return False
        return True
    
    def rule3(self):
        """
        The production symbol is always a terminal symbol previously defined
        """
        for prod in self.productions:
            if prod.get_symbol() not in self.non_terminal_symbols:
                print("Error in Grammar Validation, rule3. The terminal symbol: ", prod.get_symbol(), " can't derivate a production")
                return False
        return True
    
    def rule4(self):
        """
        All derivation symbols are included in the grammar
        """
        for prod in self.productions:
            deriv = prod.get_derivation()
            for char in deriv:
                if not (char in self.non_terminal_symbols or char in self.terminal_symbols) and char != "e":
                    print("Error in Grammar Validation, rule4. The symbol: ", char, " is not defined")
                    return False
        return True

    def validate_grammar_gld(self):
        """
        Returns true if the grammar is GLD
        """
        for prod in self.productions:
            if not prod.is_prod_valid_gld(self.non_terminal_symbols, self.terminal_symbols):
                return False
        return True
