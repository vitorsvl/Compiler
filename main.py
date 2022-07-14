from os.path import exists
from sys import argv


from analysers import lexical, syntactic

path = argv[1]
if not exists(path):
    print(f'Arquivo {path} não encontrado')
    exit()
# Análise lexica
tokens, errors = lexical.tokenize(path)

try:
    lexical.print_token_table(tokens, errors)
except:
    print('Error building tables. Please check if rich is installed')

# Análise sintática
if not errors:
    p = syntactic.Parser(tokens)
    p.parse(path)
else:
    print("Lexical errors found")