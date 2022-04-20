import re
from typing import List, Tuple

from Types import TypesRE

from Token import Token

NON_TOKENS = r'[ \t]+|\n'

def read_file(path: str) -> str:
    """
    Gets a text file and returns it's content in a string
    """
    with open(path, "r") as file:
        s = file.read()
        return s



def verify_token_type(c: str) -> Tuple:
    """
    Verify the token type by the first character and returns the possible types
    """
    # interar sobre as expressões regulares de cada tipo ??

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
        if re.fullmatch(regex, s): # se a expressão regular reconhece o token 
            tokentype = TypesRE.get_token_type(t)
            return Token(s, tokentype, pos) # instancia e retorna o objeto Token
        
    print(f'token {s} não reconhecido') # TODO criar uma exception pra isso
    return None
            

    
def identify_tokens(text: str) -> List:
    """
    Returns a list of the successfully identified tokens found in the  text
    """
    tokens_list = []
    line_pos = 0
    col_pos = 0

    sentinel = 0 # pointer that starts at the begining of the text
    look_ahead = 0 # pointer to look ahead of sentinel
    
    while sentinel < len(text):
        print(sentinel)
        print(f'at sentinel: {text[sentinel]}')
        if text[sentinel] in NON_TOKENS:
            print('entrou')
            sentinel += 1
            col_pos += 1
            if text[sentinel] == '\n': # quando quebra a linha
                col_pos = 0 # index da coluna volta pra zero
                line_pos += 1 # incrementa em 1 o index da linha 
        else:
            print('entrou else')
            while text[look_ahead] not in NON_TOKENS:
                look_ahead += 1 # olhar adiante
            # tenho um possível token de [sentinel até look_ahead]
            print(f'token: {text[sentinel:look_ahead+1]}')
            t = verify_token(text[sentinel:look_ahead+1])
            if t:
                #adiciona na lista de tokens
                tokens_list.append(t)
                print(t)
        # TODO testar essa função: retorna lista vazia
    return tokens_list 

        

if __name__ == '__main__':        
    t = verify_token('', (1, 2))

    print(t)

    tokens = identify_tokens('this is a int text; a + ')
    print(tokens)