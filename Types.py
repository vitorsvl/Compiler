
class TypesRE():
    """
    Class to represent the all types(tokens) recognized by the language 
    and it's regular expressions
    """
    # lista com os nomes dos tokens ordenados por prioridade
    prior_tokens = [
        'INT','FLOAT','CHAR','IF','ELSE','WHILE','TRUE','FALSE','PRINT',
        'OP','CP','OSB','CSB','OBR','CBR','SMC','CMM','LB','COM',
        'EQUAL','DIF','GT','LT','GTE','LTE',
        'INC','DEC','ATR','PLUS','MINUS','MUL','DIV','MOD',
        'NUM','STR','ID', 'ILL', 'ILLN'
        ]
    errors = ['ILL', 'ILLN']
    
    # Reserved words
    INT   = r'int'
    FLOAT = r'float'
    CHAR = r'char'
    IF    = r'if'
    ELSE  = r'else'
    WHILE = r'while'
    TRUE  = r'True'
    FALSE = r'False'
    PRINT = r'print'
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
    NUM = r'\d+|\d+\.\d+' # FLOAT e INT
    STR = r'".*"|\'.*\''
    # Identifiers
    ID = r'\b[a-zA-Z]\w*|\b_\w*'
    OP  = r'\(' # open parentheses
    CP  = r'\)' # close parentheses
    OSB = r'\[' # open square brackets
    CSB = r'\]' # close square brackets
    OBR = r'{' # open braces
    CBR = r'}' # close braces
    SMC = r';' # semicolon
    CMM = r',' # comma
    # SPACE = r'\s+' # blank space
    LB = r'\n' # line break
    COM = r'//.*$\n' # comment
    # unknown
    ILL = r'\S' # (Ilegal) anything that was not recognized by the other expressions (but whitespace)
    ILLN = r'^(?!_).+|^(?![a-zA-Z]).+' # Illegal name
    
    def __init__(self) -> None:
        pass
    
    def all_types(self) -> str:
        return '|'.join([getattr(TypesRE, t) for t in TypesRE.prior_tokens])

    def get_token_type(self, token: str) -> str:
        
        if token not in TypesRE.prior_tokens:
            print('Invalid token')
            return
        else:
            if token in ['IF', 'ELSE', 'TRUE', 'FALSE', 'WHILE', 'FOR', 'INT', 'FLOAT','CHAR','PRINT']:
                return 'ReservedWord'
            if token == 'ID':
                return 'Identifier'
            elif token in ['OP','CP','OSB','CSB','OBR','CBR','SMC','CMM']:
                return 'Separator'
            elif token in ['INC','DEC','ATR','PLUS','MINUS','MUL','DIV','MOD']:
                return 'ArithmeticOp'
            elif token in ['EQUAL','DIF','GT','LT','GTE','LTE']:
                return 'LogicalOp'
            elif token == 'STR' or token == 'NUM':
                return 'Literal'
            elif token == 'ILL':
                return 'IllegalChar'
            elif token == 'ILLN':
                return 'IllegalName'


if __name__ == "__main__":
    print()
   
