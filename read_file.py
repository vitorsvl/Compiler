from re import finditer, fullmatch
from typing import List, Tuple

from Types import TypesRE
from Token import Token


def read_file(path: str) -> str:
    """
    Gets a text file and returns it's content in a string
    """
    with open(path, "r") as file:
        s = file.read()
        return s


def verify_token(s: str, pos: Tuple) -> Token:
    """
    Verify if the given string is a token, if yes the token will have it's type verified.  
    Returns a Token object or None if it's not a token  
    
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
            return Token(s, tokentype, pos) # instancia e retorna o objeto Token
        
    print(f'token >{s}< não reconhecido') # TODO criar uma exception pra isso
    return None
            

def identify_tokens(text: str) -> List:
    """
    Return a list of the successfully identified tokens found in the input text
    """
    tokens = []
    lex_list = []

    line = 1
    col = 1

    fullRegEx = TypesRE().all_types()
    # usando o método finditer para encontrar no texto as ocorrências dos padrões definidos
    lx = finditer(fullRegEx, text)
    # agrupando os lexends e sua posição de inicio no texto em uma lista
    for l in lx:
        lex_list.append((l.group(), l.span()[0]))
    
    # indentificando os tokens
    prev = ('', 0)
    for lex in lex_list: # lex[0]: lexend, lex[1]: posição
        
        if lex[0] == '\n':
            col = 0
            line += 1

        else:
            print('else')
            col += (lex[1] - prev[1]) 

            t = verify_token(lex[0], (line, col))
            print('token:', t)
            tokens.append(t)
        prev = lex

    return tokens


if __name__ == '__main__':
    # txt = 'this is a int text; a + b\nvariável; exp = 12 + 3; float b; a = [1, 2, 3]'
    test = read_file('input.cp')
    print(test)
    tokens = identify_tokens(test)
    print(tokens)
    for tt in tokens:
        print(tt)



"""
O ; finaliza uma sentença. Então:
    Se exite um ; depois de um token, ou seja, um ; na posição look_ahead o token é o que está antes.
    E depois tem que ter obrigatóriamente um NON_TOKEN, se não é erro.
    TODO: repensar o nome NON_TOKEN para separadores
    Eu tenho que retornar os separadores como tokens ? [espaço e \n]? ou só o ; ?


    Quando achar um ; criar um token com oq está antes* e um com o ; # IMPLEMENTAR


    O que fazer quando não há non_tokens separando os tokens ????  a=23   [11,22,33]   b = 5;

    Quando encontrar um non-token ou um separador:
        O que está antes será verificado como token 
        caso o 'break' encontrado seja um sep:
            criar um token com este sep
        caso contrário:
            pass
    TODO consertar a posição (line, col)


    TEST 1: file=input

    não anda com a coluna quando acha um sep
    a coluna n volta pra 1 quando acha um \n

    b++ não reconhecido !!! TODO
"""