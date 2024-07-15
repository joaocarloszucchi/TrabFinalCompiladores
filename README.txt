compilação pelo comand: python main.py;

os 2 pacotes utilizados(json e sys) fazem parte da biblioteca padrão do python;

a gramática definida pela especificação de um arquivo em formato json, a qual deve contar com as seguintes variáveis:

"non_terminal_symbols": uma lista de tokens
"terminal_symbols": uma lista de tokens
"initial_symbol": um token
"productions": uma lista de regras de produção, sendo que cada regra é composta por:
    "symbol": um token
    "derivations": uma lista sendo que cada elemento pode conter vários tokens

Por convenção, definiu-se o caractere "e" como o símbolo de vazio;

Não há restrição relacionada à caracteres maiúsculos ou minúsculos em relação aos tokens, estes apenas
devem estar previamente definidos em seus respectivos conjuntos.