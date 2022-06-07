from re import finditer, fullmatch
from sys import argv
from typing import List, Tuple
from os.path import exists

from rich.table import Table
from rich.console import Console

from Types import TypesRE
from Token import Token, Error

console = Console()

def read_file(path: str) -> str:
    """
    Gets a text file and returns it's content in a string
    """
    with open(path, "r") as file:
        s = file.read()
        return s


def verify_token(s: str, pos: Tuple):
    """
    Verify if the given string is a token, if yes the token will have it's type verified.  
    Returns a Token or Error object, or None if it's not a token or an error 
    
    Params:
        s - possible token
        pos - position of s in the text (line, col)
    """
    # types = [a for a in dir(TypesRE) if not a.startswith('__')] # pegando os nomes dos atributos da classe 
    types = TypesRE.prior_tokens
    for t in types:
        regex = getattr(TypesRE, t)
        if fullmatch(regex, s): # se a expressão regular reconhece o token
            
            tokentype = TypesRE().get_token_type(t)

            if t in TypesRE.errors:
                return Error(s, tokentype, pos) # retorna um objeto Erro
            else:
                return Token(s, tokentype, pos) # instancia e retorna o objeto Token
        
    print(f'token >{s}< não reconhecido') 
    return None
            

def identify_tokens(text: str) -> Tuple:
    """
    Return a tuple containing a list of the successfully identified tokens found in the input text
    and a list of errors found
    """
    tokens = []
    errors = []
    lex_list = []

    line = 1
    col = 1

    fullRegEx = TypesRE().all_types()
    # usando o método finditer para encontrar no texto as ocorrências dos padrões definidos
    lx = finditer(fullRegEx, text)
    # agrupando os lexends e sua posição de inicio no texto em uma lista
    isCom = False
    for l in lx:
        if l.group() == '/*': # se achar um comentário
            isCom = True

        if isCom:
            if l.group() == '*/': 
                isCom = False
            continue
        lex_list.append((l.group(), l.span()[0]))

    # indentificando os tokens
    prev = ('', 0)
    for lex in lex_list: # lex[0]: lexend, lex[1]: posição
        if lex[0] == '\n':
            col = 0
            line += 1
        else:
            col += (lex[1] - prev[1])
            t = verify_token(lex[0], (line, col))
            if isinstance(t, Error):
                errors.append(t)
            else:
                tokens.append(t)
        prev = lex

    return tokens, errors


def generate_output(tokens: List, errors: List, file_name: str):
    """
    Gets a list of tokens and create a text file containing those tokens and possible errors
        tokens: list of Token objects (output of identify_tokens function)

    In the generated file each line will represent a token (or an error) as the following pattern : token type line col
    """
    
    file = 'outputs/' + file_name[:-2] + 'cplex'
    with open(file, 'w') as out:    
        out.writelines([(repr(t) + '\n') for t in tokens])
        out.write('\n')
        out.writelines([(repr(e) + '\n') for e in errors])
    try:
        console.print(f'output generated at {file}', style='#12AA57')
    except:
        print(f'output generated at {file}')


def print_token_table(tokens: List, errors: List) -> None:
    table_t = Table(title="Tokens")
    cols = ['token', 'type', 'line', 'col']
    for c in cols:
        table_t.add_column(c)

    for t in tokens:
        table_t.add_row(t.name, t.token_type, str(t.location[0]), str(t.location[1]))
    
    table_e = Table(title="Errors")
    cols = ['error', 'type', 'line', 'col']
    for c in cols:
        table_e.add_column(c)

    for e in errors:
        table_e.add_row(e.name, e.token_type, str(e.location[0]), str(e.location[1]))
    
    console.print(table_t)
    print()
    console.print(table_e)


def tokenize(path_to_file: str) -> None:
    """
    Tokenize the code in the given file. The output is saved in a file at /outputs and also shown in the console
    """
    code = read_file(path_to_file)
    tokens, errors = identify_tokens(code)

    # uncomment to generate a output file with identified tokens and errors    
    # generate_output(tokens, errors, path_to_file)
    
    return tokens, errors


if __name__ == '__main__':

    path = argv[1]
    print(path)
    if exists(path):
        tokens, errors = tokenize(path) # returns a list of tokens
        try:
            print_token_table(tokens, errors)
        except:
            print('Error building tables. Please check if rich is installed')
    else:
        print(f'Arquivo {path} não encontrado')