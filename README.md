# LFA-MEL-parser com a biblioteca Lark
Implementação de um parser descendente recursivo para uma Linguagem Livre de Contexto, chamada de MEL utilizando a ferramenta voltada para o parse de qualquer gramática livre de contexto chamada [**Lark**](https://lark-parser.readthedocs.io/en/latest/).

### Informações gerais
- **Autor**: Harã Heique dos Santos
- **Linguagem de programação**: Python (versão 3.6.7)
- **Ferramentas de suporte**: Lark Library (versão 0.7.1)
- **Ambiente de desenvolvimento**: Visual Studio Code (versão 1.33.1)

### Lark
Lark é uma biblioteca do python capaz realizar o parse de qualquer linguagem livre de contexto, sendo ela de fácil entendimento podendo ser utilizada desde iniciantes até experts do assunto. Dentre suas features estão:
- Linguagem de gramática avançada, baseado em ***EBNF***;
- Criação automática da árvore, inferida pela gramática fornecida;
- Realiza o handle de ambiguidades no parse da gramática;
- Roda em qualquer interpretador python, dado que ela é feita puramente em python;

Além dessas features existem muitas outras, porém o importante a ressaltar é que o intuito é poupar tempo e ser mais fácil na construção de parsers. Os principais links sobre ela estão logo abaixo:
- [Documentação](https://lark-parser.readthedocs.io/en/latest/)
- [Github](https://github.com/lark-parser/lark)

### Gramática
As regras de produção da gramática da linguagem livre de contexto(MEL) é definida da seguinte maneira:

```html
<expr>   ::= <term> ((‘+’ | ‘-’) <term>)*
<term>   ::= <factor> ((‘*’ | ‘/’ | ‘//’ | ‘%’) <factor>)*
<factor> ::= <base> (‘^’ <factor>)?
<base>   ::= (‘+’ | ‘-’) <base>
           | <number>
           | ‘(’ <expr> ‘)’
<number> ::= <digit>+ ‘.’? <digit>* ((‘E’ | ‘e’) (‘+’ | ‘-’)? <digit>+)?
<digit>  ::= ‘0’ | ‘1’ | ‘2’ | ‘3’ | ‘4’ | ‘5’ | ‘6’ | ‘7’ | ‘8’ | ‘9’
```

### Descrição geral do código fonte
O código fonte está estruturado da seguinte maneira:

```
source
  |_ models
    |_ LarkParserMEL.py
  |_ build.py
  |_ trab2.sh
```

##### LarkParserMEL.py
É o módulo que contém uma classe única chamada `LarkParserMEL`, o qual representa o parser em si que é responsável por manipular as expressões matemáticas da gramática MEL.

```python
from lark import Lark

# Constante do módulo definindo a gramática a ser utilizada utilizando a sintaxe Lark + EBNF
_MELGRAMMAR: str = """
    expr: term (("+" | "-") term)*
    term: factor (("*" | "/" | "//" | "%") factor)*
    factor: base ("^" factor)?
    base: ("+" | "-") base | NUMBER | "(" expr ")"

    %import common.SIGNED_NUMBER -> NUMBER
    %import common.WS_INLINE
    %ignore WS_INLINE
"""

class LarkParserMEL:
    def __init__(self):
        self._inputExpr: str = ""
        self._parser: Lark = Lark(_MELGRAMMAR, start='expr')

    @property
    def expression(self) -> str:
        return self._inputExpr

    def checkExpression(self, inputExpr: str) -> bool:
        '''Checa se a expressão de entrada é válida de acordo com a gramática MEL definida'''
        
        self._inputExpr = inputExpr

        # Usa a instancia do parser e cria a sua árvore parser de execução
        isValidExpr: bool = True
        try:
            self._parser.parse(inputExpr)
        except Exception:
            isValidExpr = False
        finally:
            return isValidExpr
```
O trecho código acima representa cerca de 90% do código do módulo, onde quando um objeto `LarkParserMEL` é instanciado também é instanciado um objeto da classe `Lark` proveniente da biblioteca importada. No construtor dessa classe é passada a gramática definida com suas regras de produção além de qual é sua regra/não-terminal inicial. Com isso é possível chamar o método `parse(expression)` capaz de criar uma tree parse caso a expressão passada como argumento seja válida, onde é utilizada na chamada do método `checkExpression`.

##### build.py
É o módulo que é buildado e que contém a execução principal do programa. Nele é utilizada a instancia do objeto da classe `LarkParserMEL`. Basicamente o usuário fornece a expressão matemática desejada e o programa retorna se a expressão digitada é válida ou inválida.

```python
from models.LarkParserMEL import LarkParserMEL

def main():
    parserMEL: LarkParserMEL = LarkParserMEL()

    while True:
        inputExpression: str = input("\nEnter your math expression: ")
        isValidExpr: bool = parserMEL.checkExpression(inputExpression)
        strIsValidExpr: str = "valid" if isValidExpr else "invalid"
        
        print("Expression {0} is {1}.".format(inputExpression, strIsValidExpr))

    return 0

if __name__ == '__main__' :
    main()
```

### Como executar?
Para buildar/executar o app no ambiente Linux basta abrir o CLI (Command Line Interface) no diretório __/source__ e digitar o seguinte comando:
    
    sh trab2.sh

Outro comando que também pode ser usado é o seguinte:

    ./trab2.sh

__OBS.:__ *Geralmente a primeira execução do programa demora um pouco mais pois necessita atualizar o gerenciador de pacotes para checar dependências e fazer o download, caso necessário, do pip (gerenciador de pacotes do Python) assim como a biblioteca Lark que necessita do pip para ser instalada.*
    
### Informações adicionais
Todo o código fonte está hospedado no [GitHub](https://github.com/cardepaula/trabalho-final-lfa-DMH).