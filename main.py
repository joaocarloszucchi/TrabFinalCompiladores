from grammar import Grammar

if __name__ == "__main__":
    print("Starting program")
    grammar = Grammar('grammar.json')
    grammar.print()

    grammar.validate_grammar()
    
    grammar.validate_sentence("101010")