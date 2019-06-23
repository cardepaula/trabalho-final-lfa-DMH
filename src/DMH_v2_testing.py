# -*- coding: utf-8 -*-

'''
    Classe responsável por realizar o parser tree(AST) e evaluation tree da expressão/código 
    passada como entrada seguindo as regras definidas pela gramática da linguagem DMH 
'''

import sys, math
from lark import Lark, Tree, Transformer, v_args

_DMHGRAMMAR_EARLEY: str = """
    start: expr ";"

    expr: assignment
         | ifexpr
         | whileexpr
         | block
         | orexpr

    ifexpr: "if" expr "do" expr ["else" "do" expr] -> ifexpr

    whileexpr: "while" expr "do" expr -> whileexpr

    block: "{" start* "}"

    assignment: "var" VARNAME "=" aexpr -> assign_var
               | VARNAME "=" aexpr -> reassign_var

    orexpr: andexpr ("||" andexpr)* -> orexpr

    andexpr: comp ("&&" comp)* -> andexpr

    comp: aexpr
        | aexpr OP_COMP aexpr

    aexpr: term
         | aexpr OP_TERM term -> term_operation

    term: factor
        | term OP_FACTOR factor -> factor_operation

    factor: trig
          | trig "^" factor -> pow

    trig: base
        | TRIG base -> trig_operation

    base: OP_LEFT base -> left_operation
        | NUMBER -> number
        | VARNAME -> getvar
        | "(" expr ")"

    OP_TERM: "+" | "-"
    OP_FACTOR: "*" | "/" | "//" | "%"
    OP_LEFT: "+" | "-"
    OP_COMP: "==" | "!=" | ">" | ">=" | "<" | "<="
    TRIG: "sen" | "cos" | "tang" | "arcsen" | "arccos" | "arctang"

    %import common.CNAME -> VARNAME
    %import common.SIGNED_NUMBER -> NUMBER
    %import common.WS_INLINE
    %ignore WS_INLINE
"""

# Constante com a mesma de _DMHGRAMMAR entretanto usando a notação de ?rule para
# realizar a evalutation tree da expressão passada como argumento e retornar seu valor
_DMHGRAMMAR_EVALTREE: str = """
    ?start: expr ";"

    ?expr: assignment
         | ifexpr
         | whileexpr
         | block
         | orexpr

    ?assignment: "var" VARNAME "=" aexpr -> assign_var
               | VARNAME "=" aexpr -> reassign_var

    ?ifexpr: "if" expr "do" expr ["else" "do" expr] -> ifexpr

    ?whileexpr: "while" expr "do" expr -> whileexpr

    ?block: "{" start* "}"

    ?orexpr: andexpr ("||" andexpr)* -> orexpr

    ?andexpr: comp ("&&" comp)* -> andexpr

    ?comp: aexpr
         | aexpr "==" aexpr -> igualdade
         | aexpr "!=" aexpr -> diferenca
         | aexpr ">" aexpr -> maior_q
         | aexpr ">=" aexpr -> maior_igual_q
         | aexpr "<" aexpr -> menor_q
         | aexpr "<=" aexpr -> menor_iqual_q

    ?aexpr: term
          | aexpr "+" term -> add
          | aexpr "-" term -> sub

    ?term: factor
         | term "*" factor -> mul
         | term "/" factor -> div
         | term "//" factor -> floordiv
         | term "%" factor -> mod

    ?factor: trig
           | trig "^" factor -> pow

    ?trig: base
         | "sen" base -> sen
         | "cos" base -> cos
         | "tang" base -> tang
         | "arcsen" base -> arcsen
         | "arccos" base -> arccos
         | "arctang" base -> arctang

    ?base: "-" base -> neg
         | "+" base -> pos
         | NUMBER -> number
         | VARNAME -> getvar
         | "(" expr ")"
    
    %import common.CNAME -> VARNAME
    %import common.SIGNED_NUMBER -> NUMBER
    %import common.WS_INLINE
    %ignore WS_INLINE
"""

# Constante do módulo definindo a gramática a ser utilizada com sintaxe EBNF
_DMHGRAMMAR: str = _DMHGRAMMAR_EVALTREE.replace('?', '')

class DMHParser:
    def __init__(self):
        self._inputExpr: str = ""
        self._tree: Tree = None
        self._parser: Lark = Lark(_DMHGRAMMAR, parser='lalr', start='start')
        self._parserEval: Lark = Lark(_DMHGRAMMAR_EVALTREE, parser='lalr', start='start', transformer=EvaluateTree(), debug=True)

    @property
    def expression(self) -> str:
        return self._inputExpr

    @property
    def tree(self) -> Tree:
        return self._tree

    def checkExpression(self, inputExpr: str) -> bool:
        '''Checa se a expressão de entrada é válida seguindo as regras da gramática da linguagem'''
        
        self._inputExpr = inputExpr

        isValidExpr: bool = True
        try:
            self._parser.parse(inputExpr)
        except Exception:
            isValidExpr = False
        finally:
            return isValidExpr

    def parseTree(self, inputExpr: str = None) -> Tree:
        '''Faz o parse da árvore da expressão de entrada'''

        if inputExpr != None: self._inputExpr = inputExpr
        self._tree = self._parser.parse(self._inputExpr)

        return self._tree

    def calcResult(self, inputExpr: str = None) -> float:
        '''Faz o cálculo da expressão de entrada e retorna o valor da árvore de avaliação'''

        if inputExpr != None: self._inputExpr = inputExpr

        return self._parserEval.parse(self._inputExpr)

@v_args(inline=True)
class EvaluateTree(Transformer):
    '''Classe que herda do Transformer responsável por visitar cada nó da árvore e 
       executando o método de acordo com o nome da regra definida na gramática'''

    def __init__(self):
        self.vars = {}

    # Métodos chamados pelo Transformer #
    number = float
    from operator import add, sub, mul, truediv as div, floordiv, mod, pos, neg, pow

    def teste(self, *args):
        return "Testing"

    def assign_var(self, name, value):
        if (name not in self.vars):
            self.vars[name] = value
            return value
        
        raise Exception("Error: Variable '{0}' is already defined".format(name))

    def reassign_var(self, name, value):
        if (name in self.vars):
            self.vars[name] = value
            return value
        
        raise Exception("Error: Variable '{0}' is not defined".format(name))

    def getvar(self, name):
        if (name in self.vars):
            return self.vars[name]
        
        raise Exception("Error: Variable {0} does not exist".format(name))

    def sen(self, deg_value):
        radian = math.radians(deg_value)
        return round(math.sin(radian), 10)

    def cos(self, deg_value):
        radian = math.radians(deg_value)
        return round(math.cos(radian), 10)

    def tang(self, deg_value):
        radian = math.radians(deg_value)
        return round(math.tan(radian), 10)

    def arcsen(self, deg_value):
        radian = math.radians(deg_value)
        return round(math.asin(radian), 10)

    def arccos(self, deg_value):
        radian = math.radians(deg_value)
        return round(math.acos(radian), 10)

    def arctang(self, deg_value):
        radian = math.radians(deg_value)
        return round(math.atan(radian), 10)

    def igualdade(self, value1, value2):
        if (value1 == value2):
            return True
        else:
            return False
    
    def diferenca(self, value1, value2):
        if (value1 != value2):
            return True
        else:
            return False
    
    def maior_q(self, value1, value2):
        if (value1 > value2):
            return True
        else:
            return False

    def maior_igual_q(self, value1, value2):
        if (value1 >= value2):
            return True
        else:
            return False
    
    def menor_q(self, value1, value2):
        if (value1 < value2):
            return True
        else:
            return False

    def menor_iqual_q(self, value1, value2):
        if (value1 <= value2):
            return True
        else:
            return False

    def orexpr(self, value1, value2 = None):
        if (value2 == None):
            return value1

    def andexpr(self, value1, value2 = None):
        if (value2 == None):
            return value1

    def whileexpr(self, value1, value2):
        pass

    def ifexpr(self, value1, value2, value3):
        pass
        
# TESTANDO O CÓDIGO #
def main():
    parser: DMHParser = DMHParser()

    while True:
        try:
            expr = input('>>> ').strip()
            if (expr == ":q"):
                break
            
            result: object = parser.calcResult(expr)
            tree: Tree = parser.parseTree(expr)
            print("Resultado: {0}\n".format(result))
            print("Parse Tree:\n {0}".format(tree.pretty()))
        except EOFError:
            print("Invalid Data Input")
        except Exception as err:
            print("{0}\n".format(err))


def test():
    parser: DMHParser = DMHParser()
    expressions: list = ["2 + 2;",
                         "3 * 23;",
                         "3 - 2 * 7;",
                         "2 // 20;",
                         "+2 - 4.0 / ----1.;",
                         "34 + 213 + 2.12 / 21;",
                         "10 * 5 + 100 / 10 - 5 + 7 % 2;",
                         "(10) * 5 + (100 // 10) - 5 + (7 % 2);",
                         "-((2+2)*2)-((2-0)+2);",
                         "(2.*(2.0+2.))-(2.0+(2.-0));",
                         "-(100) + 21 / (43 % 2);",
                         "3^4+5*(2-5);",
                         "3^2+5//(2-5);",
                         "2^2^2^-2;",
                         "0.02e2 + 0.02e-2;",
                         "8^-2 + 2E1 * 2e-1 + 3e+3 / 2.012;",
                         "8^2 + 2E1 * 2e-1 + 3e+3 // 2.;",
                         "(-2.3)^2 + 2.2E1 * 2e-12 + 1e+3;"]

    for expr in expressions:
        print("Expression: {0} = {1}".format(expr, parser.calcResult(expr)))

# Para testes unitários
if __name__ == '__main__':
    #test()
    main()