# MODELS USED FOR SEMANTIC ANALYSIS

class Vars():
    """
    Info about declared variables
    """
    # List containing the id of declared vars
    declaredIds = []
    # list containing declared variables (Var objects)
    vTable = []
    # init method gets var info and add the created var to table
    def __init__(self, varid, vartype, line, *v) -> None:
        self._id: str = varid
        self._type: str = vartype
        self._line: int = line
        if v:
            self._value = v[0]
        else:
            self._value = None
        Vars.declaredIds.append(self._id) # add declared var to list
        Vars.vTable.append(self) # add var to table

    @property
    def get_type(self) -> str:
        return self._type
    
    @property
    def get_line(self) -> int:
        return self._line
    
    @property
    def get_id(self) -> str:
        return self._id


    def show(self):
        print(f'var {self._id} of type {self._type} at line {self._line} | Value: {self._value}')

    def show_table(self):
        print('-----------------------')
        for v in Vars.vTable:
            v.show()
        print('-----------------------')



v = Vars('a', 'int', 12)
u = Vars('b', 'int', 15)
v.show_table()
    
