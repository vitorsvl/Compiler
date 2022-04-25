
class TypesRE():
    """
    Class to represent the all types(tokens) recognized by the language 
    and it's regular expressions
    """
    # lista com os nomes dos tokens ordenados por prioridade
    prior_tokens = [
        'INT','FLOAT','IF','ELSE','WHILE','TRUE','FALSE','PRINT',
        'OP','CP','OSB','CSB','OBR','CBR','SMC','CMM','LB','COM',
        'EQUAL','DIF','GT','LT','GTE','LTE',
        'INC','DEC','ATR','PLUS','MINUS','MUL','DIV','MOD',
        'NUM','STR','ID'
        ]
    
    # Reserved words
    INT   = r'int'
    FLOAT = r'float'
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
    # Separators (conferir os nomes !!!)
    OP  = r'\(' # open parentheses
    CP  = r'\)' # close parentheses
    OSB = r'\[' # open square brackets
    CSB = r'\]' # close square brackets
    OBR = r'{' # open braces
    CBR = r'}' # close braces
    SMC = r';' # semicolon
    CMM = r',' # comma
    # Coments
    LB = r'\n' # line break
    COM = r'//.*\n' # ???

    def __init__(self) -> None:
        pass
    
    def all_types(self) -> str:
        return '|'.join([getattr(TypesRE, t) for t in TypesRE.prior_tokens])

    def get_token_type(self, token: str) -> str:
        
        if token not in TypesRE.prior_tokens:
            print('Invalid token')
            return
        else:
            if token in ['IF', 'ELSE', 'TRUE', 'FALSE', 'WHILE', 'FOR', 'INT', 'FLOAT', 'PRINT']:
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

if __name__ == "__main__":
    
    import re
    
    at = TypesRE().all_types()
    print(at)
    print()
    test = 'int a = 5;\nprint("helloworld");'

    l = test.split('\n')
    ll = [a.split() for a in l]

    print(ll)

    i = re.finditer(at, ll[1][0])
    for ii in i:
        print(ii.group())
        print(ii.span())

    lexList = [l.group() for l in i]
    print(lexList)

    print('#####################################')
    test = 'int a = 2;\nint b = 3;\n\nprint(a);\n\nc = [11, 22, 33];\n\nwhile (a < b) {\n    b++;\n}'
    u = re.finditer(at, test)
    lis = list()
    for ii in u:
        lis.append((ii.group(), ii.span()[0]))

    print(lis)
   
