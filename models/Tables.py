# MODELS USED FOR SEMANTIC ANALYSIS

from typing import List
from unicodedata import name

class Var():
    """
    Info about declared variables
    """
    def __init__(self, varid, vartype, line, *v) -> None:
        self._name: str = varid
        self._type: str = vartype
        self._line: int = line
        if v:
            self._value = v[0]
        else:
            self._value = None

    @property
    def typev(self) -> str:
        return self._type
    
    @property
    def line(self) -> int:
        return self._line
    
    @property
    def name(self) -> str:
        return self._name
        
    def __str__(self):
        return f'var {self._name} of type {self._type} at line {self._line} | Value: {self._value}'

    def __repr__(self) -> str:
        return f'<name:{self._name} type:{self._type} line:{self._line} value:{self._value}>'
    

class VarTable():
    """
    Class to store declared variables
    """
    def __init__(self) -> None:
        self._table = list()
    
    def __str__(self) -> str:
        t = ''
        for var in self._table:
            t = t + repr(var) + '\n'
        return t

    @property
    def table(self) -> List:
        return self._table
    
    def getVarIndex(self, var: Var) -> int:
        return self._table.index(var)

    # def updateVar(self, var: Var): # substitui uma variável por outra quando ocorre redeclaração
    #     print(var)
    #     for v in self._table:

    #         if var.name == v.name: # encontrando a variável com o mesmo nome
    #             print('var name ==  v name')
    #             print(self._table[self.getVarIndex(v)])
    #             self._table[self.getVarIndex(v)] = var
    #             break
                

    def addVar(self, vname: str, vtype: str, vline: int, vvalue=None):
        var = Var(vname, vtype, vline, vvalue)
        self._table.append(var)

    def isDeclared(self, name: str) -> Var:
        for v in self._table:
            if name == v.name:
                return v

    def getVarType(self, name):
        for v in self._table:
            if name == v.name:
                return v.typev

    def show(self):
        if self._table:
            print(self._table)
        else: 
            print('Não há variáveis declaradas')


# TABELA DE TIPOS #
# langTypes = ['int', 'float', 'str']

class TypeTable():
    """
    Types table for samantic analysis. 
    In operations between types:  

    1 means OK (operation can be executed)
    2 means CASTING (operation can be executed with implicit casting)
    3 means ERROR (incompatible types)
    """
    def __init__(self) -> None:
        self._table = {
            'int': {
                'int': 1,
                'float': 2,
                'str': 3
            },
            'float': {
                'int': 2,
                'float': 1,
                'str': 3
            },
            'str': {
                'int': 3,
                'float': 3,
                'str': 1
            }
        }
    def check(self, type1: str, type2: str):
        """Check compatibility of types"""
        return self._table[type1][type2]

    def show(self):
        print(self._table)


if __name__ == '__main__':
    pass