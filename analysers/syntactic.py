from typing import List
from rich.console import Console
from models.Token import Token

rc = Console()
# COLOR VARIABLES
MAINCOLOR = '#85aaff i'
SUCCESS = '#42ff88 b'

# EXCEPTIONS 
class SyntacticError(Exception):
    def __init__(self, line, customMessage='') -> None:
        message = f"Syntax error at line {line}. " + customMessage
        super().__init__(message)

class MissingTokenError(Exception):
    def __init__(self, token, line=None) -> None:
        if not line:
            message = f"Syntax Error. Missing '{token}'"
        else:
            message = f"Syntax Error. Missing '{token}' at line {line}"
        super().__init__(message)

class InvalidSyntaxError(Exception):
    def __init__(self, token) -> None:
        message = f"Syntax Error. Unexpected token '{token.name}' at line {token.location[0]}\nInvalid syntax"
        super().__init__(message)


class Parser():
    def __init__(self, tokens) -> None:
        self._tokens: List = tokens
        
    def parse(self) -> bool: # método geral, começa a partir dele
        if self._tokens:
            if self.Code():
                rc.print('Compiled with no errors', style=SUCCESS)
        else:
            print('Nothing to compile')

    def match(self, expected) -> bool:
        try:
            t = self._tokens[0]
        except IndexError:
            return False   
        # print(self._tokens)
        if expected == 'id':
            if t.token_type == 'Identifier':
                return True

        elif expected == 'num':
            if t.token_type == 'Number':
                return True

        elif expected == 'str':
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

            elif self.curr_token in ['int', 'float', 'char']:
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
            self.Print_()
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
    
    def Print_(self):
        if self.match('str'):
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
        rc.print('Declaration', style=MAINCOLOR)
        self.Type()
        if self.match('id'):
            # verificar id na tabela
            lastToken = self.consume() # o que eu consumo é o nome da variável
            self.Declaration_()
            # variavel declarada, adicionar na tabela 
        else:
            raise SyntacticError(lastToken.location[0], 'Expected <id>')

    def Declaration_(self):
        if self.match('='):
            lastToken = self.consume()
            self.Val()
            if self.match(';'):
                self.consume()
            else:
                raise MissingTokenError(';', line=lastToken.location[0])
        else:
            if self.match(';'):
                self.consume()
            else:
                raise MissingTokenError(';', line=lastToken.location[0])

    def Type(self):
        if self.match('int'):
            self.consume()
            return
        if self.match('char'):
            self.consume()
            return
        if self.match('float'):
            self.consume()
            return
        else:
            raise SyntacticError(self.curr_token_full, customMessage=f'{self.curr_token} is not a valid type')

    def Atribuition(self, inForLoop=False):
        rc.print('Atribuition', style=MAINCOLOR) 
        lastToken = self.consume()
        if self.match('='): # atribuições do tipo a = 10
            lastToken = self.consume()
            self.Val()

            if not inForLoop: 
                if self.match(';'):
                    lastToken = self.consume()
                else:
                    raise MissingTokenError(';', line=lastToken.location[0]) 
        
        elif self.match('++') or self.match('--'): # atribuições do tipo a++
            lastToken = self.consume()
            if not inForLoop: # exigir ; apenas quando não está dentro de um loop for
                if self.match(';'):
                    lastToken = self.consume()
                else:
                    raise MissingTokenError(';', line=lastToken.location[0])      
        else:
            raise InvalidSyntaxError(lastToken)

    def Val(self):
        if self.match('num'):
            self.consume()
            return
        if self.match('str'):
            self.consume()
            return
        self.Expression()

    def Expression(self):
        rc.print('Expression', style=MAINCOLOR)
        self.Term()
        self.Expression_()
        
    def Term(self):
        self.F()
        self.Term_()

    def F(self):
        if self.match('id'): self.consume()
        elif self.match('num'): self.consume()
        elif self.match('str'): self.consume()

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
        else:
            raise SyntacticError(lastToken.location[0], customMessage=f'{lastToken.name} is not a valid operand for expression')
    
    def Term_(self):
        if any([self.match('*'), self.match('/'), self.match('%')]):
            self.consume()
            self.F()
            self.Term_
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
            self.Term_
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
    
### TODO RESOLVER
# ++ e -- pede um ; mas não quando aparece no for
# terminar a parte dos erros