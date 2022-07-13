from typing import List
from rich.console import Console
from analysers.semantic import CodeGen

from models.Token import Token
from models.Tables import TypeTable, VarTable
from models.Exceptions import *
from models.Warnings import *

rc = Console()
# COLOR VARIABLES #
MAINCOLOR = '#85aaff i'
SUCCESS = '#42ff88 b'

# VARIABLE TABLE #
VAR_TABLE = VarTable() # inicializando a tabela de variáveis

# TYPE TABLE #
TYPE_TABLE = TypeTable()

# WARNINGS #
WARNING_QUEUE = []

# CODE GENERATION #
CODE_GEN = CodeGen()
expCache = [] # guarda os tipos do valores usados na expressão

class Parser():
    def __init__(self, tokens) -> None:
        self._tokens: List = tokens
        
    def parse(self, path_to_file: str) -> bool: # método geral, começa a partir dele
        global path
        path = path_to_file
        if self._tokens:
            if self.Code() and not WARNING_QUEUE:
                rc.print('Compiled with no errors', style=SUCCESS)
                
            else:
                for w in WARNING_QUEUE:
                    w.show()
            CODE_GEN.generate()
        else:
            print('Nothing to compile')

    def match(self, expected, matchnext=False) -> bool:
        try:
            if matchnext:
                t = self._tokens[1]
            else:
                t = self._tokens[0]
        except IndexError:
            return False
        
        if expected == 'id':
            if t.token_type == 'Identifier':
                return True

        elif expected == 'numi':
            if t.token_type == 'IntNumber':
                return True

        elif expected == 'numf':
            if t.token_type == 'FloatNumber':
                return True

        elif expected == 'string': # string = value (literal)  str = type
            if t.token_type == 'String':
                return True
        else:
            if t.name == expected:
                return True
        # if current token doesn't match expected:
        return False
   
    @property
    def curr_token(self) -> str:
        return self._tokens[0].name

    @property
    def curr_token_full(self) -> Token:
        return self._tokens[0]

    def consume(self) -> Token:
        print(f'Token consumed: {self._tokens[0]}')
        return self._tokens.pop(0)

    def evaluate_exp(self, exp: List, line: int):
        VAR_TABLE.show()
        for v in VAR_TABLE.table:
            while v.name in exp:
                if v.value:
                    exp[exp.index(v.name)] = v.value # substitui id pelo valor
                else: # variável sem valor (não inicializada)
                    WARNING_QUEUE.append(NotInitializedWarning(v.name, line, path))
                    if v.type == 'str':
                        exp[exp.index(v.name)] = ''
                    elif v.type == 'float':
                        exp[exp.index(v.name)] = 0  
                    elif v.type == 'int':
                        exp[exp.index(v.name)] = 0.0
        # casos possíveis: exp contém valores de apenas um tipo (int, float ou str) ou mistura int e float
        # print('exp: ',exp)
        exps = ''.join(exp) # converte exp para string
        try:
            val = eval(exps) # calcula o valor da expressão. Se há int e float realiza conversão de alargamento e retorna o valor em float automaticamente
            return val

        except TypeError as e: # resulta em TypeError quando o operador é inválido para strings (o único aceito é +, que concatena)
            se = str(e)
            if '-' in se:
                op = '-'
            elif '/' in se:
                op = '/'
            elif 'multiply':
                op = '*'
            else:
                op = '%'
            raise IncompatibleTypeError('str', '', line, opr=op)
        

    def Code(self, inLoop=False, inCond=False):
        while self._tokens:
            if self.match('id'):
                self.Atribuition()

            elif self.curr_token in ['int', 'float', 'str']:
                self.Declaration()

            elif self.curr_token in ['for', 'while']:
                self.Repetition()

            elif self.curr_token == 'if':
                self.Condition()
            
            elif self.curr_token == 'print':
                self.Print()
    
            else:
                if inLoop or inCond:
                    return True # can generate empty when in loop
                else:
                    raise InvalidSyntaxError(self.curr_token_full)
          
            self.Code(inLoop=inLoop, inCond=inCond)
        return True
    
    def Block(self, inLoop=False, inCond=False):
        rc.print('Block', style=MAINCOLOR)
        if self.match('{'):
            self.consume()
            self.Code(inLoop=inLoop, inCond=inCond)
            
            if self.match('}'):
                self.consume()
            else:
                raise MissingTokenError('}')
        else:
            raise MissingTokenError('{')
    
    def Print(self):
        rc.print('Print', style=MAINCOLOR)
        lastToken = self.consume()
        if self.match('('):
            lastToken = self.consume()
            self.Print_(lastToken)
            if self.match(')'):
                lastToken = self.consume()
                if self.match(';'):
                    lastToken = self.consume()
                else:
                    raise MissingTokenError(';', line=lastToken.location[0])
            else:
                raise MissingTokenError(')', line=lastToken.location[0])
        else:
            raise MissingTokenError('(', line=lastToken.location[0])
    
    def Print_(self, lt):
        lastToken = lt
        if self.match('string'):
            lastToken = self.consume()
            if self.match(','):
                lastToken = self.consume()
                if self.match('id'):
                    self.consume()
            else:
                raise SyntacticError(lastToken.location[0], customMessage="Expected ','")
        else:
            raise SyntacticError(lastToken.location[0], 'print first argument must be string')

    def Declaration(self):
        VAR_TABLE.show()
        rc.print('Declaration', style=MAINCOLOR)
        t = self.Type()
        if self.match('id'):
            lastToken = self.consume() 
            v = VAR_TABLE.isDeclared(lastToken.name)
            if v: # variável já declarada, criar warning
                WARNING_QUEUE.append(RedeclarationWarning(v.name, lastToken.location[0], v.line, path)) # adiciona warning na fila
                
            val = self.Declaration_()
            # adicionar na tabela se esta não estiver declarada
            if not v:
                print('declara')
                VAR_TABLE.addVar(lastToken.name, t, lastToken.location[0], vvalue=val)
                v = VAR_TABLE.isDeclared(lastToken.name)
            else:
                pass # a variável redeclarada não substitui o valor da original
        else:
            raise SyntacticError(lastToken.location[0], 'Expected <id>')
        # GENERATE CODE #
        # tenho o tipo (t) tenho o id (v.name) e tenho o valor (val) (quando houver)
        print('vname ', v.name)
        CODE_GEN.declarationCode(v.name, t, value=val)
        

    def Declaration_(self):
        if self.match('='):
            lastToken = self.consume()
            val = self.Val()
            
            if self.match(';'):
                self.consume()
                return val[0] # retorna apenas o valor, não o tipo
            else:
                raise MissingTokenError(';', line=lastToken.location[0])
        else:
            if self.match(';'):
                self.consume()
                return None
            else:
                raise MissingTokenError(';', line=lastToken.location[0])

    def Type(self) -> str:
        if self.match('int'):
            t = self.consume()
            return t.name
        if self.match('str'):
            t = self.consume()
            return t.name
        if self.match('float'):
            t = self.consume()
            return t.name
        else:
            raise SyntacticError(self.curr_token_full, customMessage=f'{self.curr_token} is not a valid type')

    def Atribuition(self, inForLoop=False):
        rc.print('Atribuition', style=MAINCOLOR) 
        lastToken = self.consume()
        v = VAR_TABLE.isDeclared(lastToken.name)
        val = None;
        if not v:
            raise UndeclaredIdError(lastToken.name, lastToken.location[0])
        
        if self.match('='): # atribuições do tipo a = <value> ou a = <exp>
            self.consume()
            val, typ = self.Val() # retorna valor e tipo
            if not inForLoop: 
                if self.match(';'):
                    lastToken = self.consume()
                else:
                    raise MissingTokenError(';', line=lastToken.location[0]) 
            isInc = False
        elif self.match('++') or self.match('--'): # atribuições do tipo a++
            if v.typev != 'int':
                raise IncompatibleTypeError(v.typev, '', lastToken.location[0], opr={self.curr_token})
            isInc = True
            lastToken = self.consume()
            if not inForLoop: # exigir ; apenas quando não está dentro de um loop for
                if self.match(';'):
                    lastToken = self.consume()
                else:
                    raise MissingTokenError(';', line=lastToken.location[0])
        else:
            raise InvalidSyntaxError(lastToken)
        # CODE GENERATION #
        if isInc:
            CODE_GEN.atribuitionCode(v.name, v.typev, inc=True)
        elif v.typev == typ: # se o tipo da variável é igual ao tipo do valor atribuido
            CODE_GEN.atribuitionCode(v.name, v.typev, value=val)
        elif v.typev != typ: # tipos diferentes
            # CONVERSÃO IMPLÍCITA
            if v.typev == 'int':
                print('coerção float -> int')
                val = int(val)
            elif v.typev == 'float':
                print('coerção int -> float')
                val = float(val)
            else: # erro de atribuição
                raise AtribuitionError(val, v.typev)

            CODE_GEN.atribuitionCode(v.name, v.typev, value=val)
        

    def Val(self): # retorna o valor e o tipo
        isExp = False
        if self.match('numi') and self.match(';', matchnext=True):
            lt = self.consume()
            return lt.name, 'int'

        elif self.match('numf') and self.match(';', matchnext=True):
            lt = self.consume()
            return lt.name, 'float'

        elif self.match('string') and self.match(';', matchnext=True):
            lt = self.consume()
            return lt.name, 'str'
        else:
            value, type = self.Expression() # a expressão é evaluada e o valor retornado
            return value, type

    def Expression(self, exp=None, fromF=False):
        if not exp: 
            exp = [] # salva a expressão na forma de lista
        rc.print('Expression', style=MAINCOLOR)
        self.Term(exp)
        self.Expression_(exp)
        # print('exp:' exp)
        # CODE GENERATION #
        if not fromF: # se é uma sub-expressão não gera código
            exp_value = self.evaluate_exp(exp, self.curr_token_full.location[0])
            print('Valor da expressão: ', exp_value)
            typee = 'int' if isinstance(exp_value, int) else 'float' if isinstance(exp_value, float) else 'str'
            print('tipo: ', typee)
            return exp_value, typee # retorna o valor calculado e o tipo da expressão
        
    def Term(self, exp: List) -> bool:
        t = self.F(exp)
        # Verificar se há variáveis na fila expCache, 
        if t.token_type == 'Identifier':
            varType = VAR_TABLE.getVarType(t.name)
        else:
            if t.token_type == "IntNumber":
                varType = 'int'
            elif t.token_type == "FloatNumber":
                varType = 'float'
            elif t.token_type == "String":
                varType = 'str'
        if t.token_type != 'Separator':  
            expCache.append((t.name, varType)) # adiciona o nome(valor) e o tipo da variável lida em F no final do cache da expressão
        if len(expCache) >= 2:
            typeCheck = TYPE_TABLE.check(expCache[0][1], expCache[1][1])
            if typeCheck == 1: # OK
                expCache.pop() 
            elif typeCheck == 2: # CAST (int - float) -> sempre converte para float
                pass # casting é feito em evaluate exp   
            else: # == 3 # ERROR
                raise IncompatibleTypeError(expCache[0][1], expCache[1][1], t.location[0])
        self.Term_(exp)
     

    def F(self, exp: List):
        
        if any([self.match('id'), self.match('numi'), self.match('numf'), self.match('string')]):
            lt = self.consume()
            exp.append(lt.name)
            return lt

        elif self.match('('):
            lt = self.consume()
            exp.append(lt.name)
            self.Expression(exp=exp, fromF=True)

            if self.match(')'):
                print('chegou no )')
                lt = self.consume()
                exp.append(lt.name)
                return lt
            else:
                raise MissingTokenError(')', line=lt.location[0])
        else:
            raise SyntacticError(self.curr_token_full.location[0], customMessage=f'{self.curr_token_full.name} is not a valid operand for expression')
    
    def Term_(self, exp: List):
        if any([self.match('*'), self.match('/'), self.match('%')]):
            lt = self.consume()
            exp.append(lt.name)
            self.F(exp)
            self.Term_(exp)
        elif any([
            self.match('=='),
            self.match('!='),
            self.match('>'),
            self.match('<'),
            self.match('>='),
            self.match('<=')
            ]): 
            lt = self.consume()
            exp.append(lt.name)
            self.F(exp)
            self.Term_(exp)
        # pode gerar vazio

    def Expression_(self, exp: List):
        if self.match('+') or self.match('-'):
            lt = self.consume()
            exp.append(lt.name)
            self.Term(exp)
            self.Expression_(exp)
        elif any([
            self.match('=='),
            self.match('!='),
            self.match('>'),
            self.match('<'),
            self.match('>='),
            self.match('<=')
            ]): 
            lt = self.consume()
            exp.append(lt.name)
            self.Term(exp)
            self.Expression_(exp)
        # pode gerar vazio
    
    def Condition(self):
        rc.print('Condition', style=MAINCOLOR)
        lastToken = self.consume()
        if self.match('('):
            lastToken = self.consume()
            self.Expression()
            if self.match(')'):
                self.consume()
                self.Block(inCond=True)
                self.Condition_()
            else:
                raise MissingTokenError(')', line=lastToken.location[0])
        else:
            raise MissingTokenError('(', line=lastToken.location[0])

    def Condition_(self):
        if self.match('else'):
            self.consume()
            self.Block(inCond=True)

    def Repetition(self):
        rc.print('Repetition', style=MAINCOLOR)
        if self.match('while'):
            lastToken = self.consume()
            if self.match('('):
                lastToken = self.consume()
                self.Expression()
                if self.match(')'):
                    self.consume()
                    self.Block(inLoop=True)
                else:
                    raise MissingTokenError(')', line=lastToken.location[0])
            else:
                raise MissingTokenError(')', line=lastToken.location[0])
        
        elif self.match('for'):
            lastToken = self.consume()
            if self.match('('):
                lastToken = self.consume()
                self.Atribuition(inForLoop=True) 
                if self.match(';'):
                    lastToken = self.consume()
                    self.Expression()
                    if self.match(';'):
                        lastToken = self.consume()
                        self.Atribuition(inForLoop=True)
                        if self.match(')'):
                            self.consume()
                            self.Block(inLoop=True)
                        else: 
                            raise MissingTokenError(')', line=lastToken.location[0])
                    else:
                        raise MissingTokenError(';', line=lastToken.location[0])
                else:
                    raise MissingTokenError(';', line=lastToken.location[0])
            else:
                raise MissingTokenError('(', line=lastToken.location[0])
        else:
            raise SyntacticError(self.curr_token_full.location[0], customMessage='Expected loop keyword')

    
if __name__ == '__main__':
    from analysers.lexical import tokenize, print_token_table

    tokens, errors = tokenize("inputs/example")
    print_token_table(tokens, errors)

    print(tokens)
    p = Parser(tokens)
    p.parse()
    
    
