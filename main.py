from grammar import Grammar

if __name__ == "__main__":
    print("Starting program")

    grammar = Grammar('grammar_libre.json')
    grammar.print()
    grammar.validate_grammar()

    keep = True
    while keep:
        word = input("Type a sentence for validation(or exit to leave): ")
        if word == "exit":
            keep = False
        else:
            grammar.validate_sentence(str(word))