from typing import List
from rich.console import Console
from analysers.semantic import CodeGen, handle_casting

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
        
        # print('curr token type:',t.token_type)
        # print('curr token:',t.name)
        if expected == 'id':
            if t.token_type == 'Identifier':
                return True

        elif expected == 'num':
            if t.token_type in ('IntNumber', 'FloatNumber'):
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


    def Code(self, inLoop=False, inCond=False):
        while self._tokens:
            if self.match('id'):
                # print('entrou atr')
                self.Atribuition()

            elif self.curr_token in ['int', 'float', 'str']:
                # print('entrou dcl')
                self.Declaration()

            elif self.curr_token in ['for', 'while']:
                # print('entrou rep')
                self.Repetition()

            elif self.curr_token == 'if':
                # print('entrou cond')
                self.Condition()
            
            elif self.curr_token == 'print':
                # print('entrou print')
                self.Print()
    
            else:
                if inLoop or inCond:
                    return True # can generate empty when in loop
                else:
                    raise InvalidSyntaxError(self.curr_token_full)
                    # print('Error unexpectedd token:', self.curr_token)
                    # return False
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
                return val
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
        
        if self.match('='): # atribuições do tipo a = 10
            self.consume()
            val = self.Val()
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
        # CODE GENERATION
        CODE_GEN.atribuitionCode(v.name, v.typev, value=val, inc=isInc)
        

    def Val(self):
        # print('val com token', self.curr_token_full.token_type)
        if self.match('num') and self.match(';', matchnext=True):
            lt = self.consume()
            return lt.name

        if self.match('string') and self.match(';', matchnext=True):
            # print('entrou match str')
            lt = self.consume()
            return lt.name     
        self.Expression() 

    def Expression(self):
        rc.print('Expression', style=MAINCOLOR)
        self.Term()
        self.Expression_()
      
    def Term(self):
        t = self.F()
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
        expCache.append((t.name, varType)) # adiciona o nome(valor) e o tipo da variável lida em F no final do cache da expressão
        if len(expCache) >= 2:
            typeCheck = TYPE_TABLE.check(expCache[0][1], expCache[1][1])
            if typeCheck == 1: # OK
                expCache.pop() 
            elif typeCheck == 2: # CAST 
                print('casting')
                handle_casting(varType, t) # ??????
                
            else: # == 3 # ERROR
                raise IncompatibleTypeError(expCache[0][1], expCache[1][1], t.location[0])
        self.Term_()

    def F(self):
        
        if self.match('id'): 
            lt = self.consume()
            return lt # F retorna o token da direita para Term ou Term_ (atribuição)
            
        elif self.match('num'): 
            lt = self.consume()
            return lt

        elif self.match('string'): 
            lt = self.consume()
            return lt

        elif self.match('('):
            lastToken = self.consume()
            self.Expression()
            if self.match(')'):
                lastToken = self.consume()
            else:
                if self.curr_token == ')': 
                    return
                else:
                    raise MissingTokenError(')', line=lastToken.location[0])
            return
        else:
            raise SyntacticError(self.curr_token_full.location[0], customMessage=f'{self.curr_token_full.name} is not a valid operand for expression')
    
    def Term_(self):
        if any([self.match('*'), self.match('/'), self.match('%')]):
            self.consume()
            self.F()
            self.Term_()
        elif any([
            self.match('=='),
            self.match('!='),
            self.match('>'),
            self.match('<'),
            self.match('>='),
            self.match('<=')
            ]): 
            self.consume()
            self.F()
            self.Term_()
        # pode gerar vazio

    def Expression_(self):
        if self.match('+') or self.match('-'):
            self.consume()
            self.Term()
            self.Expression_()
        elif any([
            self.match('=='),
            self.match('!='),
            self.match('>'),
            self.match('<'),
            self.match('>='),
            self.match('<=')
            ]): 
            self.consume()
            self.Term()
            self.Expression_()
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
    
    
