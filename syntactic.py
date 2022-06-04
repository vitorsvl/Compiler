# DEFINITION OF THE GRAMAR FUNCTIONS TO PROCESS TOKENS

## Declaration

# NOTE IDEA colocar em uma classe Parser, as funções são os métodos da classe


from ast import Expression
from typing import List

from Token import Token


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
            self.Code()
        else:
            print('Nothing to compile')

    def match(self, expected) -> bool:
        t = self._tokens[0]
        if expected == 'id':
            if t.token_type == 'Identifier':
                return True

        elif expected == 'num':
            if t.token_type == 'Number':
                print('match number')
                return True

        elif expected == 'str':
            if t.token_type == 'String':
                print('match number')
                return True
        else:
            if t.name == expected:
                return True
        # if current token doesn't match expected:
        return False

    def consume(self) -> Token:
        print(f'Token consumed: {self._tokens[0]}')
        return self._tokens.pop(0)

    @property
    def curr_token(self) -> str:
        return self._tokens[0].name

    def Code(self):
        while self._tokens:
            if self.match('id'):
                print('entrou atr')
                self.Atribuition()
                self.Code()

            elif self.curr_token in ['int', 'float', 'char']:
                print('entrou dcl')
                self.Declaration()
                self.Code()

            elif self.curr_token in ['for', 'while']:
                print('entrou rep')
                self.Repetition()
                self.Code()

            elif self.curr_token == 'if':
                print('entrou cond')
                self.Condition()
                self.Code()
            
            elif self.curr_token == 'print':
                self.Print()
                self.Code()

            else:
                print('Error ', self.curr_token)
                return False
                # TODO entrado aqui quando chamado a partir de loop->block 

        print('No errors encountered')
        return True
    
    def Block(self):
        if self.match('{'):
            self.consume()
            self.Code()
            print('saiu do code')
            if self.match('}'):
                self.consume()
            else:
                print('Error Block }')
        else:
            print('Error Block {', self.curr_token)
    
    def Print(self):
        print('print')
        self.consume()
        if self.match('('):
            self.consume()
            self.Print_()
            if self.match(')'):
                self.consume()
                if self.match(';'):
                    self.consume()
                else:
                    print('Error - missing ";"')
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


    def Atribuition(self):
        print('atribuition')
        if self.match('id'):
            self.consume()
            if self.match('='):
                self.consume()
                self.Val()
                if self.match(';'):
                    self.consume()
                else:
                    print('Error: missing ;')
            # else: seria uma expressão? (F -> id)
            elif self.match('++') or self.match('--'):
                self.consume()
                # if self.match(';'):
                #     self.consume()
                # else:
                #     print('Error - got unexpected token ', self.curr_token)
            else:
                print(f'Error atribuition = ')
        else:
            print(f'Error atribuition id')

    def Val(self):
        print('val')
        if self.match('num'):
            self.consume()
            return
        if self.match('str'):
            self.consume()
            return
        self.ArtmExpression()

    def ArtmExpression(self):
        print('Arithmetic expression')
        self.Term()
        self.ArtmExpression_()
        
    def Term(self):
        self.F()
        self.Term_()

    def F(self):
        if self.match('id'): self.consume()
        elif self.match('num'): self.consume()
        elif self.match('str'): self.consume()

        elif self.match('('):
            self.consume()
            self.ArtmExpression()
            if self.match(')'):
                self.consume()
            else:
                print('Error - Missing ")"')
        else:
            print('Error F')
    
    def Term_(self):
        mul, div, mod = self.match('*'), self.match('/'), self.match('%')
        if mul or div or mod:
            self.consume()
            self.F()
            self.Term_
        # pode gerar vazio 

    def ArtmExpression_(self):
        p, m = self.match('+'), self.match('-')
        if p or m:
            self.consume()
            self.Term()
            self.ArtmExpression_()
        # pode gerar vazio
    
    def Condition(self):
        if self.match('if'):
            self.consume()
            if self.match('('):
                self.consume()
                self.ArtmExpression()
                print('after Expression')
                if self.match(')'):
                    self.consume()
                    self.Block()
                    self.Condition_()
                else:
                    print('Error - missing")"')
            else:
                print('Error - expected "("')
        else:
            print('Error Condition')

    def Condition_(self):
        if self.match('else'):
            self.Block()

    def Repetition(self):
        if self.match('while'):
            self.consume()
            if self.match('('):
                self.consume()
                self.ArtmExpression()
                if self.match(')'):
                    self.Block()
                else:
                    print('Error - missing "("')
            else:
                print('Error - expected ")"')
        
        elif self.match('for'):
            self.consume()
            if self.match('('):
                self.consume()
                self.Atribuition() 
            
                self.ArtmExpression()
                if self.match(';'):
                    self.consume()
                    self.Atribuition()
                    if self.match(')'):
                        self.consume()
                        self.Block()
                    else: 
                        print('Error - missing ")"')
                else:
                    print('Error - missing ";"')
            
            else:
                print('Error - expected "("')
        else:
            print('Error - Repetition error')

    
if __name__ == '__main__':
    from lexical import tokenize, print_token_table

    tokens, errors = tokenize("inputs/example")
    print_token_table(tokens, errors)

    print(tokens)
    p = Parser(tokens)
    p.parse()


### TODO RESOLVER
# print na saída várias vezes
# Error do code 
