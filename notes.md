# Léxico do Compilador

Construir a parte léxica de um compilador

## Linguagem
Nome da linguagem: ???

#### Grupos de tokens

__palavra reservada__ : int, float, char, double, str, for, bool, while, print... 
__identificador__: qualquer coisa começando com [A - Z] ou _  
* `re: "\b[a-zA-Z]\w+|\b_\w+"` 
__operador lógico__: >, <, >=, <=, !=, == ...
__operador aritmético__: +, ++, -, --, +=, -=, =, *, /, ^, % 
__separador__: {}, (), [],  (espaço)
__literal__
____
## Módulos

__read_file__ : lê um arquivo de texto passado por argumento no console, a função retorna o texto contido no arquivo

__scanner__ : percorre o texto identificando os tokens.  
O scanner deve receber o texto do arquivo e retornar:
* Lista de tokens e valores
* lista de símbolos
* erros (linha e coluna)

Funcionamento:

* Identificar o tipo do token com base no primeiro caractere (definir os grupos ou tipos)
* Descobrindo o tipo, encontrar o separador para aquele tipo
* Dois ponteiros: Sentinel e lookAhead
  * Sentinel: para em um caractere
  * lookAhead: olha os próximos caracteres para identificar o token
  * Sempre salvando a linha e coluna



## FONTE

[https://github.com/Rabrg/jlex/blob/master/jlex/]


