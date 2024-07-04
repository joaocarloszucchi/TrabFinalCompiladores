from grammar import Grammar

if __name__ == "__main__":
    print("Starting program")
    grammar = Grammar('grammar.json')
    print(grammar.no_terminal_symbols)
    print(grammar.terminal_symbols)
    print(grammar.initial_symbol)
    for prod in grammar.productions:
        print(prod.symbol, prod.derivations)
    