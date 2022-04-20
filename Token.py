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
    

    def __str__(self):
        return f'{self.name} {self.token_type} {self.location}'

    