from grammar import Grammar

if __name__ == "__main__":
    print("Starting program")
    #grammar = Grammar('grammar.json')
    #grammar.print()
    #grammar.validate_grammar()
    #grammar.validate_sentence("111010101")

    grammar = Grammar('grammar_exp.json')
    grammar.print()
    grammar.validate_grammar()
    grammar.validate_sentence("n-n*n/n+n")