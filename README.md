## Compiler

Implementação dos analizadores léxico, sintático e semântico de um compilador desenvolvido para a disciplina de Compiladores do curso de Ciência da Computação da UFSJ.

## Tecnologia utilizada

O programa foi inteiramente desenvolvido utilizando a linguagem de programação Python. Nenhuma dependência externa foi utilizada para a implementação, apenas a biblioteca __rich__ para vizualização.

## Linguagem
A linguagem utilizada pelo compilador é uma espécie de miniC, contendo as principais estruturas da linguagem C e alguns elementos da linguagem python (exemplos de código podem ser encontrados na pasta __/inputs__)

## Input e output
O arquivo de entrada contendo o código a ser analisado (input) é passado por parâmetro via linha de comando. A saída será mostrada no terminal, com os tokens identificados pelo analizador léxico e os passos da análise sintática, além dos possíveis erros encontrados. Também é mostrada a tabela de variáveis gerada na compilação e o código assembly gerado, o qual também é salvo em um arquivo .out na pasta outputs.

## Instruções de uso

#### Instalando dependências
* Instalando a biblioteca rich:
    `pip install rich`  

#### Execução
* Rodando o programa:
    `python3 main.py inputs/nome_do_arquivo`
      
    ou  
    `python main.py inputs/nome_do_arquivo` 
    
NOTA: Colocar os arquivos de input na pasta /inputs ou passar o caminho completo: `python3 main.py caminho_para_arquivo`

## Licença

GNU GENERAL PUBLIC LICENSE 3






