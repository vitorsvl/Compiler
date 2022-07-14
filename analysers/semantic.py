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
        if self._busy_t >= 10: # se todos estão ocupados
            self.free_t()
        t = f'$t{self._t[:(len(self._t) - self._busy_t)][-1]}' # pega o último reg dentre os disponíveis (not busy)
        self._busy_t += 1 
        return t

    def get_s(self) -> str:
        if self._busy_s >= 8: # se todos estão ocupados
            self.free_s()
        s = f'$s{self._s[:(len(self._s) - self._busy_s)][-1]}' # pega o último reg dentre os disponíveis (not busy)
        self._busy_s += 1
        return s

    def get_f(self) -> str:
        if self._busy_f >= 32: # se todos estão ocupados
            self.free_f()
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
        self._labelCount = 1
        self._floatCount = 1
        self._tab = False

    @property
    def code(self):
        return self._code
    
    @property
    def data(self):
        return self._code.get('data')
    
    @property
    def text(self):
        return self._code.get('text')
    
    @property
    def tab(self):
        return self._tab

    @tab.setter
    def tab(self, b):
        self._tab = b

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

    def _addToText(self, tab, *args):
        if tab:
            t = ' '*4
        else: t = ''
        for line in args:
            self._code['text'].append(t + line)
   

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
        
    
    def atribuitionCode(self, vid: str, vtype: str, value=None, inc=False):
        if vtype == 'int':
            t = R.get_t()
            if value: # atribuição do tipo a = 2
                l1 = f'li {t}, {value}'
                l2 = f'sw {t}, {vid}'
                # write to .text
                self._addToText(self._tab, l1, l2)
                

            elif inc: # atribuição do tipo a++
                s = R.get_s()
                l1 = f'lw {s}, {vid}'
                l2 = f'addi {s}, {s}, 1'
                l3 = f'sw {s}, {vid}'
                self._addToText(self._tab, l1, l2, l3)

        elif vtype == 'float':
            f = R.get_f()
            fpvar = f'float{self._floatCount}' # variável criada para guardar o valor literal de float (mips não permite li para float)
            self._floatCount += 1
            if value: # atribuição do tipo a = 2.5
                d = f'{fpvar}: .float {value}' 
                t1 = f'lwc1 {f}, {fpvar}'
                t2 = f'swc1 {f}, {vid}'
                # write d to data and t1 + t2 to text
                self._addToData(d)
                self._addToText(self._tab, t1, t2)
                 

        elif vtype == 'str':
            for l in self.data:
                if l.split(':')[0] == vid:
                    # substitui o valor da variável no .data
                    self.data[self.data.index(l)] = f'{vid}: .asciiz "{value}"'
                    break
                    
    def printCode(self, s: str):
        self._addToData(f'out_string: .asciiz  "{s}"')
        t1 = f'li $v0, 4 # system call code for printing string = 4'
        t2 = f'la $a0, out_string'
        t3 = f'syscall'
        self._addToText(self._tab, t1, t2, t3)

    def conditionCode(self, expVal=None, expType=None, inIf=False, inElse=False):
        print('condition code')
        print(expType)
        if inIf:
            if expType == 'int':
                print('entrou int')
                t = R.get_t()
                l1 = f'li {t}, {expVal}'
                l2 = f'beq {t}, $0, elseLabel{self._labelCount}'
                self._addToText(self._tab, l1, l2)

            elif expType == 'float':
                print('entrou float')
                f = R.get_f()
                fpvar = f'float{self._floatCount}' 
                self._floatCount += 1
                d = f'{fpvar}: .float {expVal}' 
                t1 = f'lwc1 {f}, {fpvar}'
                t2 = f'beq {f}, $0, elseLabel{self._labelCount}'
                self._addToData(d)
                self._addToText(self._tab, t1, t2)

        elif inElse:
            self._addToText(self._tab, f'elseLabel {self._labelCount}:')
            self._labelCount += 1
            self._tab = True
        
    def repetitionCode(self):
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

