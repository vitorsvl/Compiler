"""
Definition of the types used by the language

"""
import re

# Non-Tokens
# Reserved words
rw = ['int', 'for', 'while', 'if', 'else', 'elif', 'True', 'False']

# Identifiers

class TypesRE():
    """
    Class to represent the all types(tokens) recognized by the language 
    and it's regular expressions
    """
    # lista com os nomes dos tokens ordenados por prioridade
    prior_tokens = ['INT','FLOAT','IF','ELSE','WHILE','TRUE','FALSE','OP','CP','OSB','CSB','OC','CC','DV','CM','COM','EQUAL','DIF','GT','LT','GTE','LTE','INC','DEC','ATR','PLUS','MINUS','MUL','DIV','MOD','NUM','STR','ID']
    
    # Reserved words
    INT   = r'int'
    FLOAT = r'float'
    IF    = r'if'
    ELSE  = r'else'
    WHILE = r'while'
    TRUE  = r'True'
    FALSE = r'False'
    # Logical Operators
    EQUAL = r'==' 
    DIF   = r'!='
    GT    = r'>' 
    LT    = r'<'
    GTE   = r'>='
    LTE   = r'<='
    # Arithmetical Operators
    ATR   = r'='
    PLUS  = r'\+' 
    MINUS = r'-'
    INC   = r'\++'
    DEC   = r'--' 
    MUL   = r'\*'
    DIV   = r'/'
    MOD   = r'%'
    # Literals
    NUM = r'\d' # melhorar essa expressão
    STR = r'".*"|\'.*\''
    # Identifiers
    ID = r'\b[a-zA-Z]\w*|\b_\w*'
    # Separators (conferir os nomes !!!)
    OP  = r'\(' 
    CP  = r'\)'
    OSB = r'\['
    CSB = r'\]'
    OC  = r'{'
    CC  = r'}'
    DV  = r';'
    CM  = r','
    # Coments
    COM = r'//.*\n' # ???

    def __init__(self) -> None:
        pass
    
    def get_token_type(token: str) -> str:
        print(token)
        if token not in TypesRE.prior_tokens:
            print('Invalid token')
            return
        else:
            if token in ['IF', 'ELSE', 'TRUE', 'FALSE', 'WHILE', 'FOR', 'INT', 'FLOAT']:
                return 'ReservedWord'
            if token == 'ID':
                return 'Identifier'
            elif token in ['(', ')', '[', ']', '{', '}', ';', ',']:
                return 'Separator'
            elif token in ['=', '+', '-', '++', '--', '/', '*', '%']:
                return 'ArithmeticOp'
            elif token in ['==', '!=', '>=', '<=', '<', '>']:
                return 'LogicalOp'
            elif token == 'STR' or token == 'NUM':
                return 'Literal'

if __name__ == "__main__":
    
    
    print(re.fullmatch(TypesRE.STR, '"hsjfsdhfjsdh"'))
