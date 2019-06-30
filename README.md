# Trabalho Final de LFA 2019/1 - Implementação de uma Linguagem de Domínio Específico (DSL)

Implementação de uma Linguagem de Domínio Específico (DSL), chamada ***DMH***, utilizando a ferramenta voltada para o parse de qualquer gramática livre de contexto chamada [**Lark**](https://lark-parser.readthedocs.io/en/latest/).

O trabalho em questão foi passado na disciplina de *LFA (Linguagens Formais e Automatos)*, do curso de graduação de Bacharelado de Sistema de Informação do IFES - Serra, pelo docente Dr. Jefferson Oliveira Andrade.

A liguagem ***DMH***, nome proveniente das inicias dos nomes dos autores, é voltada exclusivamente no desenvolvimento de aplicações para cálculos matemáticos aritméticos e trigonométricos. Podendo utilizar mecanismos de construção sintática para seleção (*if:else*) e repetição (*while*), além de mecanismos de nomeação (manipulação de variáveis) e abstração (funções), muito comumente utlizados nas linguagens de programação.

### Informações gerais
- **Autores**: Douglas Bolis Lima, Harã Heique dos Santos, Marcos Antonio Carneiro de Paula
- **Linguagem de programação**: Python (versão 3.6.8+)
- **Ferramentas de suporte**: Lark Library (versão 0.7.1)
- **Ambiente de desenvolvimento**: Visual Studio Code (versão 1.35.1) e PyCharm Community (versão 2018.3)

### Lark
Lark é uma biblioteca do python capaz realizar o parse de qualquer linguagem livre de contexto, sendo ela de fácil entendimento podendo ser utilizada desde iniciantes até experts do assunto. Dentre suas features estão:
- Linguagem de gramática avançada, baseado em [***EBNF***](https://en.wikipedia.org/wiki/Extended_Backus%E2%80%93Naur_form);
- Criação automática da árvore, inferida pela gramática fornecida;
- Realiza o handle de ambiguidades no parse da gramática;
- Roda em qualquer interpretador python, dado que ela é feita puramente em python;

Além dessas features existem muitas outras, porém o importante a ressaltar é que o intuito é poupar tempo e ser mais fácil na construção de parsers. Os principais links sobre ela estão logo abaixo:
- [Documentação](https://lark-parser.readthedocs.io/en/latest/)
- [Github](https://github.com/lark-parser/lark)

### Gramática
As regras de produção da gramática da DSL está escrita no formato *EBNF* e é definida da seguinte maneira:

```html
start: expr ";" (expr ";")*

expr: assignment
    | ifexpr
    | whileexpr
    | funct
    | aexpr
    | print

assignment: "var" NAME "=" aexpr
          | NAME "=" aexpr

ifexpr: "if" comp "do" block ["else" "do" block]

whileexpr: "while" comp "do" block

block: "{" start "}"

funct: "defun" NAME "(" ")" "do" functblock

functblock: "{" start* functreturn "}"

functreturn: "returns" aexpr ";"

functcall: NAME "(" ")"

print: "show" "(" aexpr ")"

comp: aexpr OP_COMP aexpr
    | "(" aexpr OP_COMP aexpr ")"

aexpr: term
     | aexpr OP_TERM term

term: factor
    | term OP_FACTOR factor

factor: trig
      | factor OP_POW trig

trig: base
    | TRIG base

base: leftoperation
    | number 
    | getvar
    | functcall
    | TRIG base
    | "(" aexpr ")"

leftoperation: OP_LEFT base

number: NUMBER

getvar: NAME

OP_TERM: "+" | "-"
OP_FACTOR: "//" | "*" | "/" | "%"
OP_POW: "^"
OP_LEFT: "+" | "-"
OP_COMP: "==" | "!=" | ">=" | "<=" | ">" | "<"
TRIG: "sen" | "cos" | "tang" | "arcsen" | "arccos" | "arctang"
COMMENT: /(\#\#.+\#\#)/
LCASE_LETTER: "a".."z"
UCASE_LETTER: "A".."Z"
LETTER: UCASE_LETTER | LCASE_LETTER
NAME: ("_"|LETTER) ("_"|LETTER|DIGIT)*
NUMBER: /-?\d+(\.\d+)?([eE][+-]?\d+)?/
           
```

### Descrição geral
O código fonte está estruturado da seguinte maneira:

```
trabalho-final-lfa-DHM
|_ Readme.md
|_ relatório.pdf
|_ ast_outfiles
  |_ *imagens_ast*.png
|_ source
  |_ grammar
    |_ grammar.lark
  |_ models
    |_ DMHEvaluateTree.py
    |_ DHMParser.py
  |_ build.py
  |_ trabFinal.sh
|_ testes
  |_ *arquivos para testes*.dmh
```
#### Descrição geral dos arquivos

Descrição geral dos arquivos contidos nesta aplicação:

Arquivo|Path|Descrição
---|---|---
**grammar.lark**|source/grammar/grammar.lark|Arquivo contendo a gramática em *EBNF* da linguagem.
**DMHParser.py**|source/models/DMHParser.py|Classe responsável por realizar o parser tree (AST) da expressão/código passada como entrada seguindo as regras definidas pela gramática da linguagem DMH.
**DMHEvaluateTree.py**|source/models/DMHEvaluateTree.py|Classe responsável por realizar o *evaluation* da árvore (AST) da expressão/código.
**build.py**|source/build.py|É o módulo que é buildado e que contém a execução principal do programa. É nele que são instanciados os objetos da classes que manipulam as expressões provenientes tanto de arquivos do formato .dmh quanto do console interativo com o usuário, o quais ambos são possibilidades que o usuário possui ao utilizar a aplicação.
**arquivos de testes.dmh**|testes/*arquivos de testes.dmh*|Diretório que contém os arquivos na extensão *.dmh* contendo o código que segue a gramática da linguagem estabelecida, com proposito de serem utilizados para testar a linguagem.
**imagens_ast.png**|ast_outifiles/*imagens_ast.png*|Diretório onde são salvos as imagens dos diagramas que representam as árvores dos *arquivos.dmh*. 

**OBS:** As imagens contida no diretório *ast_outifiles/* são geradas quando se executa a aplicação passando um *arquivo.dmh* como argumento.  

### Como executar?
Para executar o programa existe duas formas:

- **Executar o *source/trabalhoFinal.sh*:** 

    - Execução do script:
    ```bash
    $ sh ./source/trabalhoFinal.sh
    ou caso tenha problema entre no diretório source/ e digite:
    $ sh trabalhoFinal.sh
    ```
- O script verifica se existe [virtual env](https://pythonacademy.com.br/blog/python-e-virtualenv-como-programar-em-ambientes-virtuais), se não existir ele tenta criar um, e executa o *build.py*;
- **Executar manualmente:**
    - Se existir não virtual env (diretório *source/env* ) execute os comandos (de preferencia no diretório *source/* ):
    
        - Atualizando os repositórios do sistema
        ```bash
        $ sudo apt-get update (debian based)
        ou
        $ sudo pacman -Sy (arch linux based)
        ```
        - Instalando o pip (se não estiver instalado):
        ```bash
        $ sudo apt install python3-pip (debian based)
        ou
        $ sudo pacman -S python-pip (arch linux based)
        ```
        - Talvez seja necessário instalar também o pacote *python3-venv* :
        ```bash
        $ sudo apt install python3-venv
        ```
        - Criando o virtual env
        ```bash
        $ sudo apt install graphviz
        ```
        - Instalando o virtual env:
        ```bash
        $ sudo pip3 install virtualenv
        ```
        - Criando o virtual env
        ```bash
        $ python3 -m venv ./env
        ```
        - Ativando o virtual env:
        ```bash
        $ source ./env/bin/activate 
        ou
        $ . ./env/bin/activate
        ```
        - Instalando o Lark
        ```bash
        pip install lark-parser
        ```
        - Instalando o argparse
        ```bash
        pip install argparse
        ```
        - Instalando o pydot
        ```bash
        pip install pydot
        ```
        
    - Se já exitir virtual env (diretório *source/env* ), dentro do doretório *source*, execute o seguinte comando:
        - Ativando o virtual env:
        ```bash
        $ source ./env/bin/activate 
        ou
        $ . ./env/bin/activate
        ```
    - E, finalmente, execute o build.py:
        ```bash
        $ python3 ./build.py --file nome_arquivo.dmh
        ou 
        $ python ./build.py --file nome_arquivo.dmh
        ```
    **OBS:** Para desativar o virtual env:
    ```bash
    $ deactivate
    ```
    
### Informações adicionais
Todo o código fonte está hospedado no [GitHub](https://github.com/cardepaula/trabalho-final-lfa-DMH).
