from sys import argv
from typing import List

inputfile = argv[1][7:]

# CODE GENERATION #
filepath = 'outputs/' + inputfile + '.out' # out = compiler output

# cria o arquivo se não existir ou limpa se existir
# f = open(filepath, "w");
# f.close()

# registers
class Regs():
    def __init__(self) -> None:
        self._t = [9, 8, 7, 6, 5, 4, 3, 2, 1, 0] # temporary
        self._s = [7, 6, 5, 4, 3, 2, 1, 0] # saved
        self._f = [n for n in range(31, -1, -1)] # float (32 regs [0 - 31])
        self._busy_t = 0
        self._busy_s = 0
        self._busy_f = 0

    def get_t(self) -> str:
        print(self._t)
        t = f'$t{self._t[:(len(self._t) - self._busy_t)][-1]}' # pega o último reg dentre os disponíveis (not busy)
        self._busy_t += 1 
        return t

    def get_s(self) -> str:
        s = f'$s{self._s[:(len(self._s) - self._busy_s)][-1]}' # pega o último reg dentre os disponíveis (not busy)
        self._busy_s += 1
        return s

    def get_f(self) -> str:
        f = f'$f{self._f[:(len(self._f) - self._busy_f)][-1]}' # pega o último reg dentre os disponíveis (not busy)
        self._busy_f += 1
        return f

    def free_t(self):
        self._busy_t -= 1
    
    def free_s(self):
        self._busy_s -= 1    

    def free_f(self):
        self._busy_f -= 1
        
R = Regs() # registradores

class CodeGen():
    def __init__(self) -> None:
        self._code = {'data': [], 'text': []}

    @property
    def code(self):
        return self._code
    
    def generate(self): # método que escreve no arquivo
        to_write = '.data\n'
        for ld in self._code['data']:
            to_write = to_write + '    ' + ld + '\n'

        to_write = to_write + '\n' + '.text\n'
        for lt in self._code['text']:
            to_write = to_write + '    ' + lt + '\n'
        
        print(to_write) # botar saída para aquivo de texto
        
    def _addToData(self, *args):
        for line in args:
            self._code['data'].append(line)

    def _addToText(self, *args):
        for line in args:
            self._code['text'].append(line)
    
    def declarationCode(self, vid: str, vtype: str, value=None):
        if vtype == 'int':
            if value: # se o valor é conhecido
                l = f'{vid}: .word {value}'
            else:
                l = f'{vid}: .space 4' 

        elif vtype == 'float':
            if value: # se o valor é conhecido
                l = f'{vid}: .float {value}'
            else:
                l = f'{vid}: .space 4' # float size = 4bytes

        elif vtype == 'str': 
            if value: # se o valor é conhecido
                l = f'{vid}: .asciiz  "{value}"'
            else:
                l = f'{vid}: .space 256   # buffer = 256 (default)' 
        # write to .data
        self._addToData(l)
        R.free_t()
    
    def atribuitionCode(self, vid: str, vtype: str, value=None, inc=False):
        if vtype == 'int':
            t = R.get_t()
            if value: # atribuição do tipo a = 2
                l1 = f'li {t}, {value}'
                l2 = f'sw {t}, {vid}'
                # write to .text
                self._addToText(l1, l2)
                R.free_t()

            elif inc: # atribuição do tipo a++
                s = R.get_s()
                l1 = f'lw {s}, {vid}'
                l2 = f'addi {s}, {s}, 1'
                l3 = f'sw {s}, {vid}'
                self._addToText(l1, l2, l3)

        elif vtype == 'float':
            print('entra aqui')
            f = R.get_f()
            fpvar = 'float1' # variável criada para guardar o valor literal de float (mips não permite li para float)
            if value: # atribuição do tipo a = 2.5
                d = f'{fpvar}: .float {value}' 
                t1 = f'lwc1 {f}, {fpvar}'
                t2 = f'swc1 {f}, {vid}'
                # write d to data and t1 + t2 to text
                self._addToData(d)
                self._addToText(t1, t2)
                R.free_f() 

        elif vtype == 'str':
            pass        


if __name__ == '__main__':
    g = CodeGen()
    g.declarationCode('a', 'int', value=9)
    g.declarationCode('b', 'float', value=2.9)
    g.declarationCode('d', 'int', value=15)
    g.declarationCode('c', 'int')

    g.atribuitionCode('c', 'int', value=23)
    g.atribuitionCode('d', 'int', vid2='a')
    g.atribuitionCode('b', 'float', value=3.14)

    g.generate()

