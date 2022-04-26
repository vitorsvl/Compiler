class Token():
    """
    Class that represents a language token
        name: token name
        type: token type (reserved word, identifier, operator...)
        loc: location of the token in file (line, column)
    """
    RegEx = {
        ''
    }
    def __init__(self, name, ttype, loc):
        self.name = name
        self.token_type = ttype
        self.location = loc
    

    def __str__(self) -> str:
        return f'{self.name} {self.token_type} {self.location}'

    def __repr__(self) -> str:
        return f'{self.name} {self.token_type} {self.location[0]} {self.location[1]}'

    def __len__(self) -> int:
        return len(self.name)

class Error(Token):
    pass
