# MODELS USED FOR SEMANTIC ANALYSIS

from typing import List

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
    
    def addVar(self, vname: str, vtype: str, vline: int, *vvalue):
        if vvalue: 
            value = vvalue[0]
        else: 
            value = None
        var = Var(vname, vtype, vline, value)
        self._table.append(var)

    def isDeclared(self, name: str) -> Var:
        for v in self._table:
            if v.name == name:
                return v
            return    

    def show(self):
        if self._table:
            print(self)
        else: 
            print('Não há variáveis declaradas')
        

T = VarTable()
T.show()
T.addVar('a', 'int', 12, 125)
T.addVar('b', 'str', 14, 'qweqwrf')
T.addVar('c', 'int', 190)

T.show()
