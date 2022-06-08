## Compiler - Léxico e Sintático

Implementação dos analizadores léxico e sintático de um compilador desenvolvido para a disciplina de Compiladores do curso de Ciência da Computação da UFSJ

## Tecnologia utilizada

O programa foi inteiramente desenvolvido utilizando a linguagem de programação Python. Nenhuma dependência externa foi utilizada para a implementação, apenas a biblioteca __rich__ para vizualização.

## Linguagem
A linguagem utilizada pelo compilador é uma espécie de miniC, contendo as principais estruturas da linguagem C e alguns elementos da linguagem python (exemplos de código podem ser encontrados na pasta __/inputs__)

## Input e output
O arquivo de entrada contendo o código a ser analisado (input) é passado por parâmetro via linha de comando. A saída será mostrada no terminal, com os tokens identificados pelo analizador léxico e os passos da análise sintática, além dos possíveis erros encontrados.

## Instruções de uso

#### Instalando dependências
* Instalando a biblioteca rich:
    `pip install rich`  

#### Execução
* Rodando o programa:
    `python3 main.py nome_do_arquivo`
      
    ou  
    `python main.py nome_do_arquivo`

## Licença

GNU GENERAL PUBLIC LICENSE 3






