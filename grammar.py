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
        print(self.symbol, " -> ", " ".join(self.derivation))

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
        return str(self.symbol) + " -> " + " ".join(self.derivation)


class Grammar():
    def __init__(self, grammar_path):
        self.non_terminal_symbols = []
        self.terminal_symbols = []
        self.initial_symbol = None
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
                    derivation_elements = derivation.split(' ')
                    production = Production(symbol, derivation_elements)
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

    def validate_sentence(self, word):
        """
        inittial validation, before going to computation

        checks if the word contains only terminal symbols that belong to the alphabet
        """ 
        tokens = word.split()
        print("\nlist of tokens:\n\n", tokens, "\n")

        for token in tokens:
            if token not in self.terminal_symbols:
                print("Word can't be recognized because the symbol ", token, " does not belongs to the language")
                return
        
        stack = []
        stack.append(self.initial_symbol)
        result = self.compute(word=tokens, stack=stack)

        if result == 1:
            print("Word belongs to the language!")
        else:
            print("Word doesn't belongs to the language!")

    def compute(self, word, stack):
        print("                     |word: ", word, "|stack:  ", stack)

        if len(stack) == 0 or stack == "e":
            if len(word) == 0:
                return 1
            return -1

        tam = min(len(word), len(stack)) - 1

        if tam == 0:
            if word[0] == stack[0]:
                token = word[0]
                word = word[1:]
                stack = stack[1:]
                print("Recognizing symbol:", token)
                print("                     |word: ", word, "|stack:  ", stack)
            elif stack[0] in self.terminal_symbols:
                print("Word doesn't belong to the language")
                return -1
        else:
            i = 0
            while i < tam:
                if word[i] == stack[i]:
                    token = word[0]
                    word = word[1:]
                    stack = stack[1:]
                    print("Recognizing symbol:", token)
                    print("                     |word: ", word, "|stack:  ", stack)
                    i -= 1
                elif stack[i] in self.terminal_symbols:
                    return -1
                else:
                    break
                i = i + 1

        if len(stack) == 0 or stack == "e":
            if len(word) == 0:
                return 1
            return -1

        productions = self.get_productions(stack[0])

        #this will happend when the symbol is a terminal symbol
        if len(productions) == 0:
            return -1
        
        word_copy = word
        stack_copy = stack

        #looks for a valid production
        for prod in productions:
            deriv = prod.get_derivation()
            if len(word) == 0:
                if deriv == "e":
                    stack = self.derivate_stack(stack, deriv)
                    print("Derivating: ", prod.get_print_string())

                    #if this production flow leads to an error, restore the word and the stack and try another possible production
                    if self.compute(word=word, stack=stack) == -1:
                        stack = stack_copy
                        word = word_copy
                        print("Restoring due to wrong derivation")
                        print("                     |word: ", word, "|stack:  ", stack)
                    else:
                        return 1
            elif deriv[0] == word[0]:
                stack = self.derivate_stack(stack, deriv)
                print("Derivating: ", prod.get_print_string())

                #if this production flow leads to an error, restore the word and the stack and try another possible production
                if self.compute(word=word, stack=stack) == -1:
                    stack = stack_copy
                    word = word_copy
                    print("Restoring due to wrong derivation")
                    print("                     |word: ", word, "|stack:  ", stack)
                else:
                    return 1
        return -1

    def get_productions(self, symbol):
        """
            Returns all the productions of a non terminal symbol
        """
        productions = []
        for prod in self.productions:
            if prod.get_symbol() == symbol:
                productions.append(prod)
        return productions
    
    def derivate_stack(self, stack, deriv):
        """
        Updates the stack with the new production
        """

        stack = stack[1:]
        if deriv == ["e"]:
            return stack
        stack = deriv + stack
        return stack


    