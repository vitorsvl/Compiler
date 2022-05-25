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
                    for ntt in ntToCheck:
                        First[nt] = First[nt].union(First[ntt]) # A -> Bx : First(A) = First(A) U First(B)
                        print(First[nt])
                        print(First[ntt])
                        if ['#'] not in P.get(ntt): # se B gera vazio, adiciona o prox não-terminal
                            break 

                        if allGenEmpty: # se todos os não-terminais anteriores ao terminal geram vazio
                            First[nt].add(s) # adiciona o terminal no First do não-terminal atual
                        
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
    for f in FIRST:
        print(f'First({f}) = {FIRST[f]}')