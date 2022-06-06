from typing import List

from Token import Token


class MissingTokenError(Exception):
    def __init__(self, token, line) -> None:
        message = f"Syntax Error. Missing '{token}' at line {line}"
        super().__init__(message)

class InvalidSyntaxError(Exception):
    def __init__(self, token) -> None:
        message = f"Syntax Error. Unexpected token '{token.name}' at line {token.location[0]}\nInvalid syntax"
        super().__init__(message)


class Parser():
    ct = 0 # current token position
    def __init__(self, tokens) -> None:
        self._tokens: List = tokens
        # self._parsed: bool = self.parse(self._tokens)

    def read_token(self) -> Token:
        try:
            return self._tokens[Parser.ct]
        except IndexError:
           return False 
        
    def parse(self) -> bool: # método geral, começa a partir dele
        if self._tokens:
            if self.Code():
                print('Compiled with no errors')
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
                print('entrou atr')
                self.Atribuition()

            elif self.curr_token in ['int', 'float', 'char']:
                print('entrou dcl')
                self.Declaration()

            elif self.curr_token in ['for', 'while']:
                print('entrou rep')
                self.Repetition()

            elif self.curr_token == 'if':
                print('entrou cond')
                self.Condition()
            
            elif self.curr_token == 'print':
                self.Print()
    
            else:
                if inLoop or inCond:
                    return True # can generate empty when in loop
                else:
                    raise InvalidSyntaxError(self.curr_token_full)
                    # print('Error unexpectedd token:', self.curr_token)
                    # return False
            self.Code(inLoop=inLoop)
        return True
    
    def Block(self, inLoop=False, inCond=False):
        if self.match('{'):
            self.consume()
            self.Code(inLoop=inLoop, inCond=inCond)
            
            if self.match('}'):
                self.consume()
            else:
                print(self.curr_token)
                print('Error Block }', self.curr_token)
        else:
            print('Error Block {', self.curr_token)
    
    def Print(self):
        print('print')
        self.consume()
        if self.match('('):
            self.consume()
            self.Print_()
            if self.match(')'):
                lastToken= self.consume()
                if self.match(';'):
                    lastToken = self.consume()
                else:
                    raise MissingTokenError(';', lastToken.location[0])
                    # print('Error - missing ";"')
            else:
                print('Error - missing ")"')
        else:
            print('Error - expected "("')
    
    def Print_(self):
        if self.match('str'):
            self.consume()
            if self.match(','):
                self.consume()
                if self.match('id'):
                    self.consume()
                else:
                    print('Error - expected id')
            else:
                print('Error - missing token ","')
        else:
            print('Error - print first argument must be string')


    def Declaration(self):
        print('declaration')
        self.Type()
        if self.match('id'):
            self.consume()
            self.Declaration_()
        else:
            print('Error Declaration')

    def Declaration_(self):
        if self.match('='):
            self.consume()
            self.Val()
            if self.match(';'):
                self.consume()
            else:
                print('Error - missing ";"')
        else:
            if not self.match(';'):
                print(f'Error ', self._tokens[0])
            else:
                self.consume()

    def Type(self):
        print('type')
        if self.match('int'):
            self.consume()
            return
        if self.match('char'):
            self.consume()
            return
        if self.match('float'):
            self.consume()
            return
        print(f'Error type')

    def Atribuition(self, inForLoop=False):
        print('atribuition')
        # if self.match('id'): 
        lastToken = self.consume()
        if self.match('='): # atribuições do tipo a = 10
            lastToken = self.consume()
            self.Val()

            if not inForLoop: 
                if self.match(';'):
                    lastToken = self.consume()
                else:
                    raise MissingTokenError(';', lastToken.location[0]) 
        
        elif self.match('++') or self.match('--'): # atribuições do tipo a++
            lastToken = self.consume()
            if not inForLoop: # exigir ; apenas quando não está dentro de um loop for
                if self.match(';'):
                    lastToken = self.consume()
                else:
                    raise MissingTokenError(';', lastToken.location[0])      
        else:
            raise InvalidSyntaxError(lastToken)
        # else:
        #     print(f'Error atribuition id')

    def Val(self):
        print('val')
        if self.match('num'):
            self.consume()
            return
        if self.match('str'):
            self.consume()
            return
        self.Expression()

    def Expression(self):
        print('Expression')
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
            self.consume()
            self.Expression()
            if self.match(')'):
                self.consume()
            else:
                if self.curr_token == ')': return
                print('Error - Missing ")"')
        else:
            print('Error F ', self.curr_token)
    
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
        print('Condition')
        self.consume()
        if self.match('('):
            self.consume()
            self.Expression()
            print('after Expression')
            if self.match(')'):
                self.consume()
                self.Block(inCond=True)
                self.Condition_()
            else:
                print('Error - missing")"')
        else:
            print('Error - expected "("')

    def Condition_(self):
        if self.match('else'):
            self.Block(inCond=True)

    def Repetition(self):
        print('Repetition')
        if self.match('while'):
            self.consume()
            if self.match('('):
                self.consume()
                self.Expression()
                print('saiu de expression')
                if self.match(')'):
                    self.consume()
                    self.Block(inLoop=True)
                else:
                    print('Error - missing "("')
            else:
                print('Error - expected ")"')
        
        elif self.match('for'):
            self.consume()
            if self.match('('):
                self.consume()
                self.Atribuition(inForLoop=True) 
                if self.match(';'):
                    self.consume()
                    self.Expression()
                    if self.match(';'):
                        self.consume()
                        self.Atribuition(inForLoop=True)
                        if self.match(')'):
                            self.consume()
                            self.Block(inLoop=True)
                        else: 
                            print('Error - missing ")"')
                    else:
                        print('Error - missing ";"')    
                else:
                    print('Error - missing ";"')
            else:
                print('Error - expected "("')
        else:
            print('Error - Repetition error')

    
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