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






