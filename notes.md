# Análise Sintática

### __Gramática Livre de Contexto__ __G=(V, T, P, S)__
T = terminais --> __Tokens__

Entrada: Conjunto de tokens  
Saída: Erro sintático ou árvore de derivação

EXEMPLO:

Entrada: <int> <a> = 45 while ( i < 10) print(a)

_These sets can provide the actual position of any terminal in the derivation_ ~~ First and Follow

### Gramáticas para a linguagem CPy
- Bloco de Código
V = {S, }
T = {}
- Expressões matemáticas  
V = {E, T, F}  
T = {+, -, *, /, (, ), _num_}
    1. E -> E + T
    2. E -> E - T
    3. E -> T
    3. T -> T * F
    4. T -> T / F
    5. T -> F
    6. F -> (E)
    7. F -> _num_   

- Declaração variável   
V = {S, A, B}  
T = {`type`, `=`, `str`, `num`, `id`, `&`}

    1. S -> `type` `id` A
    2. A -> `=`B
    3. A -> `&`
    4. B -> `id`
    5. B -> `num`
    6. B -> `str`

- Declaração função  
V = {S, A}  
T = { `type`, `id`, `&`, `(`, `)`, `{`, `}`, `code` }

    1. S -> `type` `id` `(`A`)` `{` `code` `}`
    2. A -> `&`
    3. A -> `type id` A

- Condição

V = {S}
T = {`if`, `else`, `` }
- Repetição

- Bloco

##########################  
\# DEFINIÇÃO DAS GRAMÁTICAS #   
##########################  
V = {
- BLOCK (bloco de código)  

- ATR (atribuição)

- EXP (expressão)

- DEC (declaração)

- TYPE (tipo)

- REP (repetição)

- COND (condição)  
}

BLOCK := 
    ATR | E

### Notas aula

botar ;

codigo -> atribuição codigo | declaração codigo | ...
codigo' -> atribuição | declaração | repetição | ...
codigo -> $ (EOF)

codigo'' -> atribuição codigo'' | declaração codigo'' | vazio

bloco -> codigo'
bloco -> { codigo'' }
bloco -> ;




## tentativa de implementar first

### FUNCTIONS TO CALCULATE FIRST AND FOLLOW SETS ###

# GRAMMAR  (# == EPSILON == EMPTY STRING)
from typing import Dict, List



# FIRST 
def first(g: Dict) -> Dict:
    """
    Calculates the First set for the non-terminals of the given LL1 grammar
    """
    P = g['P']
    T = g['T']
    V = g['V']
    First = {key: set() for key in V}
    # print(P)
    # print(T)
    # print(First)
    
    for nt in V:
        for p in P.get(nt):
            if p[0] in T: # se o primeiro elemento de alguma produção é terminal
                First[nt].add(p[0])
            else:
                print(f'entrou no else pq o simbolo é {p[0]}')
                First[nt] = First[nt].union(First[p[0]]) # se for um terminal
                i = 1
                
                while (i < len(p)) and (p[i] in V) and (['#'] in P.get(p[i])): # enquanto o simbolo é não terminal e gera vazio
                    First[nt] = First[nt].union(First[p[i]]) # se for um terminal
                    i += 1
                
                ntToCheck = []
                for s in p: # para cada simbolo na produção
                    if s not in T:
                        ntToCheck.append(s)
                    else: # encontrou um terminal
                        # verifica se os não-terminais anteriores geram vazio
                        allGenEmpty = True
                        for ntt in ntToCheck:
                            if ['#'] not in P.get(ntt):
                                allGenEmpty = False
                                break

                        if allGenEmpty: # se todos os não-terminais anteriores ao terminal geram vazio
                            First[nt].add(s) # adiciona o terminal no First do não-terminal atual
                        
        # print(ntToCheck)
        # for ntt in ntToCheck:
        #     First[nt] = First[nt].union(First[ntt]) # A -> Bx : First(A) = First(A) U First(B)
        #     print(f'First({nt}) : {First[nt]}')
        #     print(f'First({ntt}) : {First[ntt]}')
        #     if ['#'] not in P.get(ntt): # se B gera vazio, adiciona o prox não-terminal
        #         break
    return First


# FOLLOW
def follow(g: Dict) -> List:
    """
    Calculates the Follow set for the non-terminals of the given LL1 grammar
    """
    pass

if __name__ == '__main__':
    
    G = {
        # non-terminals
        'V': ['E', 'E_', 'T', 'T_', 'F'],
        # terminals
        'T': ['+', '*', '(', ')', '#', 'a'],
        # productions
        'P': {
            'E': [['T', 'E_']],
            'T': [['F', 'T_']],
            'F': [['(', 'E', ')'], ['a']],
            'E_': [['+', 'T', 'E_'], ['#']],
            'T_': [['*', 'F', 'T_'], ['#']],
        },
        # start symbol
        'S': 'E'
    }
    FIRST = first(G)
    print('### FIRST ###')
    for f in FIRST:
        print(f'First({f}) = {FIRST[f]}')







