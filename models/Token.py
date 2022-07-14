class Token():
    """
    Class that represents a language token
        name: token name
        token_type: token type (reserved word, identifier, operator...)
        location: location of the token in file (line, column)
    """
   
    def __init__(self, name, ttype, loc):
        self._name = name # value for literal tokens 
        self._token_type = ttype
        self._location = loc
    
    @property
    def name(self):
        return self._name

    @property
    def token_type(self):
        return self._token_type
    
    @property
    def location(self):
        return self._location

    @name.setter
    def set_name(self, value):
        self._name = value
    
    @token_type.setter
    def set_name(self, type):
        self._token_type = type

    def __str__(self) -> str:
        return f'{self.name} {self.token_type} {self.location}'

    def __repr__(self) -> str:
        return f'{self.name} {self.token_type} {self.location[0]} {self.location[1]}'

    def __len__(self) -> int:
        return len(self.name)
    

class Error(Token):
    pass
